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
from util.Constants import MINUTES_OF_DATA_TO_LOOK_AT_FOR_MODEL, \
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
        entries = []

        path = self.filePathPrefix + ticker + "-1m-data.csv"
        count = 0
        numSamples = 0
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

                    entries2, dicts, totalSamples = self._generateSubMinuteData(row, timing, SAMPLES_PER_MINUTE)
                    listOfDicts += dicts
                    numSamples += totalSamples
                    entries += entries2
                    count += 1

                    if count == 10000:
                        print("Read " + ticker + " data up to " + str(timing))
                        count = 0

            # df = pd.DataFrame(entries, index=index, columns=["Timestamp", "Open", "High", "Low", "Close", "Volume"])
            df = pd.DataFrame(entries, index=[i for i in range(numSamples)], columns=["Timestamp", "Close", "Volume"])
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
        price = self._getValues(ticker, ["Close"], d_aware, seconds=60)["Close"]

        if len(price) == 0:
            price = 0.0
        else:
            price = price[-1]

        print("Price at " + str(d_aware) + ": " + str(price))

        return price

    def obtainVolume(self, ticker: str) -> float:
        date = self._getCurrentHistoricalDate()
        start_date_to_use = datetime(date.year, date.month, date.day,
                                     hour=date.hour, minute=date.minute,
                                     second=date.second)
        timezone = pytz.timezone(self.timezone)
        d_aware = timezone.localize(start_date_to_use)
        volume = self._getValues(ticker, ["Volume"], d_aware, seconds=1)["Volume"]

        if len(volume) == 0:
            return 0.0

        return volume[0]

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
        # print("Obtaining price and volume data of " + ticker + " at " + str(d_aware) + ".")
        values = self._getValues(ticker, ["Close", "Volume"], d_aware, numberOfPrices * SECONDS_BETWEEN_SAMPLES)
        # values = self._getValuesFromDataframe(self._dataAsDataFrames[ticker], ["High", "Volume"], d_aware)

        if len(values["Close"]) != 0:
            # print("Price of " + ticker + ": " + str(values["Close"][-1]))
            pass
        else:
            print("Price of " + ticker + ": 0 prices!")

        time2 = datetime.now()
        # print("obtainPricesAndVolumes took " + str(time2 - now) + ".")
        return values["Close"], values["Volume"]

    def obtainMinutePricesAndVolumes(self, ticker: str, numberOfPrices=SAMPLES_OF_DATA_TO_LOOK_AT):
        now = datetime.now()
        diff = (now - self._startTime) * self._fastForwardAmount
        date = self.dateOfStart + diff
        # Don't use second=date.second:
        start_date_to_use = datetime(date.year, date.month, date.day,
                                     hour=date.hour, minute=date.minute)
        timezone = pytz.timezone(self.timezone)
        d_aware = timezone.localize(start_date_to_use)
        print("Obtaining minute price and volume data of " + ticker + " at " + str(d_aware) + ".")
        values = self._getMinuteValues(ticker, ["Close", "Volume"], d_aware, numberOfPrices)

        if len(values["Close"]) != 0:
            print("Price of " + ticker + ": " + str(values["Close"][-1]) + " (minute)")
        else:
            print("Price of " + ticker + ": 0 prices! (minute)")

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

    def _getMinuteValues(self, symbol: str, values: List, endTime: datetime, minutes=-1) -> Dict:
        if minutes < 0:
            minutes = SAMPLES_OF_DATA_TO_LOOK_AT

        startTime = endTime - timedelta(minutes=minutes)
        lst = {}
        lastTimestamp = None

        for v in values:
            lst[v] = []

        for d in self._dataAsListOfDicts[symbol]:
            if d["Timestamp"] > endTime:
                break

            if d["Timestamp"] <= startTime:
                continue

            if lastTimestamp is None or d["Timestamp"] >= lastTimestamp + timedelta(minutes=1):
                lastTimestamp = d["Timestamp"]

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

    def _generateSubMinuteData(self, row, timing, samplesPerMinute):
        timeIndex = [timing + timedelta(seconds=i) for i in range(0, 60, 60 // samplesPerMinute)]
        open = float(row["open"])
        mid = (float(row["high"]) + float(row["low"])) / 2
        close = float(row["close"])
        prices = [open + ((mid - open) / (samplesPerMinute / 2)) * i for i in range(samplesPerMinute // 2)]
        prices += [mid + ((close - mid) / (samplesPerMinute / 2)) * i for i in range(samplesPerMinute // 2)]
        dicts = []
        entries = []

        for i in range(samplesPerMinute):
            trade = int(row["trades"])

            d = {
                "Timestamp": timeIndex[i],
                "Close": prices[i],
                "Volume": trade
            }

            dicts.append(d)
            entries.append([timeIndex[i], prices[i], trade])

        return entries, dicts, samplesPerMinute


