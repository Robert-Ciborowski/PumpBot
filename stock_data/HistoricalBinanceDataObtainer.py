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
from util.Constants import MINUTES_OF_DATA_TO_LOOK_AT


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

                    entry = {
                        "Timestamp": timing,
                        "Open": float(row["open"]),
                        "High": float(row["high"]),
                        "Low": float(row["low"]),
                        "Close": float(row["close"]),
                        "Volume": int(row["trades"])
                    }

                    listOfDicts.append(entry)
                    index.append(timing)
                    entries.append([timing, float(row["open"]), float(row["high"]),
                                    float(row["low"]), float(row["close"]),
                                    int(row["trades"])])
                    count += 1

                    if count == 10000:
                        print("Read " + ticker + " data up to " + str(timing))
                        count = 0

            # self.data[ticker] = df[["Volume", "Close"]]
            df = pd.DataFrame(entries, index=index, columns=["Timestamp", "Open", "High", "Low", "Close", "Volume"])
            self._dataAsDataFrames[ticker] = df
            self._dataAsListOfDicts[ticker] = listOfDicts
            print("Done reading " + ticker + " historical data.")

        except IOError as e:
            print("Could not read " + path + "!")

    def obtainPrice(self, ticker: str) -> float:
        date = self._getCurrentHistoricalDate()
        start_date_to_use = datetime(date.year, date.month, date.day,
                                     hour=date.hour, minute=date.minute)
        timezone = pytz.timezone(self.timezone)
        d_aware = timezone.localize(start_date_to_use)
        return self._getValueFromDataframe(self._dataAsDataFrames[ticker], "High", d_aware)

    def obtainPrices(self, ticker: str, numberOfPrices=1) -> List[float]:
        now = datetime.now()
        diff = (now - self._startTime) * self._fastForwardAmount
        date = self.dateOfStart + diff
        start_date_to_use = datetime(date.year, date.month, date.day,
                                     hour=date.hour, minute=date.minute)
        timezone = pytz.timezone(self.timezone)
        d_aware = timezone.localize(start_date_to_use)
        return self._getValues(ticker, ["High"], d_aware)["High"]

    def obtainPricesAndVolumes(self, ticker: str, numberOfPrices=1):
        now = datetime.now()
        diff = (now - self._startTime) * self._fastForwardAmount
        date = self.dateOfStart + diff
        start_date_to_use = datetime(date.year, date.month, date.day,
                                     hour=date.hour, minute=date.minute)
        timezone = pytz.timezone(self.timezone)
        d_aware = timezone.localize(start_date_to_use)
        print("Obtaining price and volume data of " + ticker + " at " + str(d_aware) + ".")
        values = self._getValues(ticker, ["High", "Volume"], d_aware)
        # values = self._getValuesFromDataframe(self._dataAsDataFrames[ticker], ["High", "Volume"], d_aware)

        if len(values["High"]) != 0:
            print("Price of " + ticker + ": " + str(values["High"][-1]))
        else:
            print("Price of " + ticker + ": 0 prices!")

        time2 = datetime.now()
        print("obtainPricesAndVolumes took " + str(time2 - now) + ".")
        return values["High"], values["Volume"]

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

    def _getValues(self, symbol: str, values: List, endTime: datetime, pricesToObtain=-1) -> Dict:
        if pricesToObtain < 0:
            pricesToObtain = MINUTES_OF_DATA_TO_LOOK_AT

        startTime = endTime - timedelta(minutes=pricesToObtain)
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


