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

from stock_data.StockDataObtainer import StockDataObtainer

class HistoricalBinanceDataObtainer(StockDataObtainer):
    dateOfStart: datetime
    dateOfEnd: datetime
    timezone: str
    filePathPrefix: str

    _startTime: datetime
    _data: Dict[str, pd.DataFrame]
    _obtained: bool
    _timezone: str

    def __init__(self, dateOfStart: datetime, dateOfEnd: datetime, filePathPrefix=""):
        self.dateOfStart = dateOfStart
        self.dateOfEnd = dateOfEnd
        self._startTime = datetime.now()
        self.endOfMarket = (4, 0)
        self._data = {}
        self._obtained = False
        self.filePathPrefix = filePathPrefix
        self._timezone ="Etc/GMT-0"

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
        df = pd.DataFrame([], columns=["Price", "Volume"])

        try:
            with open(path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    timestamp = row["timestamp"]
                    times = re.split(r'[/:\s]\s*', timestamp)

                    time = datetime(int(times[2]), int(times[1]),
                                                 int(times[0]), int(times[3]),
                                                 int(times[4]))
                    timezone = pytz.timezone(self._timezone)
                    time = timezone.localize(time)
                    price = float(row["open"])
                    volume = int(row["trades"])
                    row = pd.DataFrame([[price, volume]], index=[time], columns=["Price", "Volume"])
                    df = pd.concat([row, df])
                    self._data[ticker] = df

        except IOError as e:
            print("Could not read " + path + "!")

    def obtainPrice(self, ticker: str) -> float:
        return 0.0

    """
    - data: in the form {"Ticker": []}
    """

    def obtainPrices(self, ticker: str, numberOfPrices=-1) -> List[float]:
        return []


