# Name: Historic Binance Crypto Data Obtainer
# Author: Robert Ciborowski
# Date: 13/04/2020
# Description: Keeps track of stock prices to the minute.

# from __future__ import annotations
import csv
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import pandas as pd
import re
import pytz
import time

from stock_data.StockDataObtainer import StockDataObtainer

class HistoricalBinanceDataObtainer(StockDataObtainer):
    dateOfStart: datetime
    dateOfEnd: datetime
    filePathPrefix: str

    _startTime: datetime
    _data: Dict[str, pd.DataFrame]
    _obtained: bool
    timezone: str

    def __init__(self, dateOfStart: datetime, dateOfEnd: datetime, filePathPrefix=""):
        self._startTime = datetime.now()
        self.endOfMarket = (4, 0)
        self._data = {}
        self._obtained = False
        self.filePathPrefix = filePathPrefix
        self.timezone = "Etc/GMT-0"
        timezone = pytz.timezone(self.timezone)
        self.dateOfStart = timezone.localize(dateOfStart)
        self.dateOfEnd = timezone.localize(dateOfEnd)

    def trackStocks(self, tickers: List[str]):
        if self._obtained:
            return

        for ticker in tickers:
            self._readTickerData(ticker)

        self._obtained = True

    def stopTrackingStocks(self, tickers: List[str]):
        if not self._obtained:
            return

        for ticker in tickers:
            self._data.pop(ticker)

    def _readTickerData(self, ticker: str):
        path = self.filePathPrefix + ticker + "-1m-data.csv"
        # df = pd.DataFrame([], columns=["Price", "Volume"])
        df = pd.DataFrame([], columns=["Timestamp", "Open", "High", "Low", "Close", "Volume"])
        count = 0
        # minuteCount = 0

        try:
            with open(path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # if count > 428576:
                    #     break
                    # count += 1
                    #
                    # if count < 425697:
                    #     continue

                    # minuteCount += 1
                    #
                    # if minuteCount == 60:
                    #     minuteCount = 0
                    #
                    # if minuteCount != 1:
                    #     continue

                    # print(count)

                    timestamp = row["timestamp"]
                    times = re.split(r'[-/:\s]\s*', timestamp)

                    try:
                        if "-" in timestamp:
                            timing = datetime(int(times[0]), int(times[1]),
                                            int(times[2]), int(times[3]),
                                            int(times[4]))
                        else:
                            timing = datetime(int(times[2]), int(times[1]),
                                            int(times[0]), int(times[3]),
                                            int(times[4]))
                    except ValueError as e:
                        print(timestamp)
                        print(e)
                        time.sleep(1000)

                    timezone = pytz.timezone(self.timezone)
                    timing = timezone.localize(timing)

                    if timing < self.dateOfStart:
                        continue

                    if timing > self.dateOfEnd:
                        break

                    price = float(row["open"])
                    price2 = float(row["high"])
                    price3 = float(row["low"])
                    price4 = float(row["close"])
                    volume = int(row["trades"])
                    # row = pd.DataFrame([[price, volume]], index=[time], columns=["Price", "Volume"])
                    row = pd.DataFrame([[timing, price, price2, price3, price4, volume]], index=[timing], columns=["Timestamp", "Open", "High", "Low", "Close", "Volume"])
                    df = pd.concat([df, row])
            vRA = '24m Volume RA'
            self._addRA(df, 24, 'Volume', vRA)
            pRA = '24m Close Price RA'
            self._addRA(df, 24, 'Close', pRA)
            self._data[ticker] = df
            print(df)

        except IOError as e:
            print("Could not read " + path + "!")

    def obtainPrice(self, ticker: str) -> float:
        return 0.0

    """
    - data: in the form {"Ticker": []}
    """

    def obtainPrices(self, ticker: str, numberOfPrices=-1) -> List[float]:
        return []

    def _addRA(self, df, windowSize, col, name):
        df[name] = pd.Series.rolling(df[col], window=windowSize,
                                     center=False).mean()


