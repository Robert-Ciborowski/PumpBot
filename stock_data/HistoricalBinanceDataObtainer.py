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
    data: Dict[str, pd.DataFrame]
    timezone: str

    _startTime: datetime
    _obtained: bool
    _fastForwardAmount: float

    def __init__(self, dateOfStart: datetime, dateOfEnd: datetime, filePathPrefix="", fastForwardAmount=1):
        self._startTime = datetime.now()
        self.endOfMarket = (4, 0)
        self.data = {}
        self._obtained = False
        self.filePathPrefix = filePathPrefix
        self.timezone = "Etc/GMT-0"
        self._fastForwardAmount = fastForwardAmount
        timezone = pytz.timezone(self.timezone)
        self.dateOfStart = timezone.localize(dateOfStart)
        self.dateOfEnd = timezone.localize(dateOfEnd)

    def setStartTimeToNow(self):
        self._startTime = datetime.now()

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
            self.data.pop(ticker)

    def _readTickerData(self, ticker: str):
        path = self.filePathPrefix + ticker + "-1m-data.csv"
        # df = pd.DataFrame([], columns=["Price", "Volume"])
        df = pd.DataFrame([], columns=["Timestamp", "Open", "High", "Low", "Close", "Volume"])
        count = 0
        timezone = pytz.timezone(self.timezone)
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

                    if len(times) < 5:
                        continue

                    try:
                        if "-" in timestamp:
                            timing = datetime(int(times[0]), int(times[1]),
                                            int(times[2]), int(times[3]),
                                            int(times[4]))
                        else:
                            timing = datetime(int(times[2]), int(times[1]),
                                            int(times[0]), int(times[3]),
                                            int(times[4]))
                    except:
                        print("Error:")
                        print(timestamp)
                        continue
                        # time.sleep(1)

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

                    count += 1

                    if count == 10000:
                        print("Read " + ticker + " data up to " + str(timing))
                        count = 0

            # vRA = '24m Volume RA'
            # self._addRA(df, 24, 'Volume', vRA)
            # pRA = '24m Close Price RA'
            # self._addRA(df, 24, 'Close', pRA)
            # self.data[ticker] = df[["Volume", "Close"]]
            self.data[ticker] = df

        except IOError as e:
            print("Could not read " + path + "!")

    def obtainPrice(self, ticker: str) -> float:
        now = datetime.now()
        diff = (now - self._startTime) * self._fastForwardAmount
        date = self.dateOfStart + diff
        start_date_to_use = datetime(date.year, date.month, date.day,
                                     hour=date.hour, minute=date.minute)
        timezone = pytz.timezone(self.timezone)
        d_aware = timezone.localize(start_date_to_use)
        return self._getValueFromDataframe(self.data[ticker], "Close", d_aware)

    def obtainPrices(self, ticker: str, numberOfPrices=1) -> List[float]:
        now = datetime.now()
        diff = (now - self._startTime) * self._fastForwardAmount
        date = self.dateOfStart + diff
        start_date_to_use = datetime(date.year, date.month, date.day,
                                     hour=date.hour, minute=date.minute)
        timezone = pytz.timezone(self.timezone)
        d_aware = timezone.localize(start_date_to_use)
        return self._getValuesFromDataframe(self.data[ticker], "Close",
                                              d_aware)

    def obtainPricesAndVolumes(self, ticker: str, numberOfPrices=1):
        now = datetime.now()
        diff = (now - self._startTime) * self._fastForwardAmount
        date = self.dateOfStart + diff
        start_date_to_use = datetime(date.year, date.month, date.day,
                                     hour=date.hour, minute=date.minute)
        timezone = pytz.timezone(self.timezone)
        d_aware = timezone.localize(start_date_to_use)
        prices = self._getValuesFromDataframe(self.data[ticker], "Close", d_aware)
        volumes = self._getValuesFromDataframe(self.data[ticker], "Volume", d_aware)
        return prices, volumes

    def _getValueFromDataframe(self, df: pd.DataFrame, value: str, time: datetime) -> float:
        keys = df.index.tolist()

        if len(keys) == 0:
            return 0.0

        lastKey = keys[0]

        for key in keys:
            if key.to_pydatetime() > time:
                break
            lastKey = key

        return df.iloc[lastKey][value]

    def _getValuesFromDataframe(self, df: pd.DataFrame, value: str, time: datetime, pricesToObtain=-1) -> List[float]:
        keys = df.index.tolist()

        if len(keys) == 0:
            return []

        lastIndex = 0

        for i in range(len(keys)):
            if keys[i].to_pydatetime() > time:
                lastIndex = i
                break

        startIndex = 0
        endIndex = lastIndex
        lst = []

        if not (pricesToObtain < 0 or pricesToObtain >= lastIndex):
            startIndex = lastIndex-pricesToObtain

        for i in range(startIndex, endIndex):
            lst.append(df.iloc[i][value])

        return lst

    def _addRA(self, df, windowSize, col, name):
        df[name] = pd.Series.rolling(df[col], window=windowSize,
                                     center=False).mean()


