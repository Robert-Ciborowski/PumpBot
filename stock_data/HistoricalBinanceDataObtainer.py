# Name: Historic Binance Crypto Data Obtainer
# Author: Robert Ciborowski
# Date: 13/04/2020
# Description: Keeps track of stock prices to the minute.

# from __future__ import annotations
import csv
from datetime import datetime, timedelta
from typing import Dict, List
import pandas as pd
import re
import pytz

from stock_data.StockDataObtainer import StockDataObtainer
from util.Constants import MINUTES_OF_DATA_TO_LOOK_AT, \
    SAMPLES_OF_DATA_TO_LOOK_AT, SAMPLES_PER_MINUTE, SECONDS_BETWEEN_SAMPLES


class HistoricalBinanceDataObtainer(StockDataObtainer):
    dateOfStart: datetime
    dateOfEnd: datetime
    filePathPrefix: str
    timezone: str

    # Pandas makes life easy but is very slow, so we use both Pandas and a
    # list of dicts. :clown:
    _dataAsDataFrames: Dict[str, pd.DataFrame]
    _dataAsListOfDicts: Dict[str, List[Dict]]

    _startTime: datetime
    _obtained: bool
    _fastForwardAmount: float

    def __init__(self, dateOfStart: datetime, dateOfEnd: datetime, filePathPrefix="", fastForwardAmount=1):
        self._startTime = datetime.now()
        self.endOfMarket = (4, 0)
        self._dataAsDataFrames = {}
        self._dataAsListOfDicts = {}
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
            self._dataAsDataFrames.pop(ticker)
            self._dataAsListOfDicts.pop(ticker)

    """
    Reads ticker data into both self._dataAsDataFrames and self._dataAsListOfDicts
    """
    def _readTickerData(self, ticker: str):
        listOfDicts = []
        index = []
        entries = []

        path = self.filePathPrefix + ticker + "-1m-data.csv"
        count = 0
        timezone = pytz.timezone(self.timezone)

        try:
            with open(path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
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
                        print("Error reading historical timestamp " + str(timestamp) + " for " + ticker + ".")
                        continue

                    timing = timezone.localize(timing)

                    if timing < self.dateOfStart:
                        continue

                    if timing > self.dateOfEnd:
                        break

                    price1 = float(row["open"])
                    price3 = (float(row["high"]) + float(row["close"])) / 2
                    price5 = float(row["close"])
                    price2 = (price1 + price3) / 2
                    price4 = (price3 + price5) / 2

                    entry1 = {
                        "Timestamp": timing,
                        "Close": price1,
                        "Volume": int(row["trades"])
                    }

                    entry2 = {
                        "Timestamp": timing + timedelta(seconds=10),
                        "Close": price2,
                        "Volume": int(row["trades"])
                    }

                    entry3 = {
                        "Timestamp": timing + timedelta(seconds=20),
                        "Close": price3,
                        "Volume": int(row["trades"])
                    }

                    entry4 = {
                        "Timestamp": timing + timedelta(seconds=30),
                        "Close": price3,
                        "Volume": int(row["trades"])
                    }

                    entry5 = {
                        "Timestamp": timing + timedelta(seconds=40),
                        "Close": price4,
                        "Volume": int(row["trades"])
                    }

                    entry6 = {
                        "Timestamp": timing + timedelta(seconds=50),
                        "Close": price5,
                        "Volume": int(row["trades"])
                    }

                    listOfDicts.append(entry1)
                    listOfDicts.append(entry2)
                    listOfDicts.append(entry3)
                    listOfDicts.append(entry4)
                    listOfDicts.append(entry5)
                    listOfDicts.append(entry6)
                    index.append(timing)
                    index.append(timing + timedelta(seconds=10))
                    index.append(timing + timedelta(seconds=20))
                    index.append(timing + timedelta(seconds=30))
                    index.append(timing + timedelta(seconds=40))
                    index.append(timing + timedelta(seconds=50))
                    entries.append([timing, price1, int(row["trades"])])
                    entries.append([timing + timedelta(seconds=10),
                                    price2, int(row["trades"])])
                    entries.append([timing + timedelta(seconds=20),
                                    price3, int(row["trades"])])
                    entries.append([timing + timedelta(seconds=30),
                                    price3, int(row["trades"])])
                    entries.append([timing + timedelta(seconds=40),
                                    price4, int(row["trades"])])
                    entries.append([timing + timedelta(seconds=50),
                                    price5, int(row["trades"])])
                    count += 1

                    if count == 10000:
                        print("Read " + ticker + " data up to " + str(timing))
                        count = 0

            # self.data[ticker] = df[["Volume", "Close"]]
            # df = pd.DataFrame(entries, index=index, columns=["Timestamp", "Open", "High", "Low", "Close", "Volume"])
            df = pd.DataFrame(entries, index=index, columns=["Timestamp", "Close", "Volume"])
            self._dataAsDataFrames[ticker] = df
            self._dataAsListOfDicts[ticker] = listOfDicts
            print("Done reading " + ticker + " historical data.")

        except IOError as e:
            print("Could not read " + path + "!")

    def obtainPrice(self, ticker: str) -> float:
        date = self._getCurrentHistoricalDate()
        start_date_to_use = datetime(date.year, date.month, date.day,
                                     hour=date.hour, minute=date.minute,
                                     second=date.second)
        timezone = pytz.timezone(self.timezone)
        d_aware = timezone.localize(start_date_to_use)
        return self._getValues(ticker, ["Close"], d_aware, pricesToObtain=1)[0]["Close"]

    def obtainPrices(self, ticker: str, numberOfPrices=SAMPLES_OF_DATA_TO_LOOK_AT) -> List[float]:
        now = datetime.now()
        diff = (now - self._startTime) * self._fastForwardAmount
        date = self.dateOfStart + diff
        start_date_to_use = datetime(date.year, date.month, date.day,
                                     hour=date.hour, minute=date.minute,
                                     second=date.second)
        timezone = pytz.timezone(self.timezone)
        d_aware = timezone.localize(start_date_to_use)
        return self._getValues(ticker, ["Close"], d_aware, pricesToObtain=numberOfPrices)["Close"]

    def obtainPricesAndVolumes(self, ticker: str, numberOfPrices=SAMPLES_OF_DATA_TO_LOOK_AT):
        now = datetime.now()
        diff = (now - self._startTime) * self._fastForwardAmount
        date = self.dateOfStart + diff
        start_date_to_use = datetime(date.year, date.month, date.day,
                                     hour=date.hour, minute=date.minute,
                                     second=date.second)
        timezone = pytz.timezone(self.timezone)
        d_aware = timezone.localize(start_date_to_use)
        print("Obtaining price and volume data of " + ticker + " at " + str(d_aware) + ".")
        values = self._getValues(ticker, ["Close", "Volume"], d_aware, numberOfPrices * SECONDS_BETWEEN_SAMPLES)
        # values = self._getValuesFromDataframe(self._dataAsDataFrames[ticker], ["High", "Volume"], d_aware)

        if len(values["Close"]) != 0:
            print("Price of " + ticker + ": " + str(values["Close"][-1]))
        else:
            print("Price of " + ticker + ": 0 prices!")

        time2 = datetime.now()
        # print("obtainPricesAndVolumes took " + str(time2 - now) + ".")
        return values["Close"], values["Volume"]

    def getHistoricalDataAsDataframe(self, symbol: str) -> pd.DataFrame:
        return self._dataAsDataFrames[symbol]

    def getCurrentDate(self) -> datetime:
        return self._getCurrentHistoricalDate()

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

    def _getValues(self, symbol: str, values: List, endTime: datetime, seconds=-1) -> Dict:
        if seconds < 0:
            seconds = SAMPLES_OF_DATA_TO_LOOK_AT * SECONDS_BETWEEN_SAMPLES

        startTime = endTime - timedelta(seconds=seconds)
        lst = {}

        for v in values:
            lst[v] = []

        for d in self._dataAsListOfDicts[symbol]:
            if d["Timestamp"] > endTime:
                break

            if d["Timestamp"] <= startTime:
                continue

            for v in values:
                lst[v].append(d[v])

        return lst

    def _addRA(self, df, windowSize, col, name):
        df[name] = pd.Series.rolling(df[col], window=windowSize,
                                     center=False).mean()

    def _getCurrentHistoricalDate(self):
        now = datetime.now()
        diff = (now - self._startTime) * self._fastForwardAmount
        return self.dateOfStart + diff


