# Name: Stock Database
# Author: Robert Ciborowski
# Date: 13/04/2020
# Description: Keeps track of stock prices to the minute.

# from __future__ import annotations

from typing import Dict, List
import pandas as pd
import yfinance as yf
import threading as th
from datetime import datetime

from events.EventDispatcher import EventDispatcher
from events.ListingPriceUpdatedEvent import ListingPriceUpdatedEvent
from filter.StockFilter import StockFilter
from stock_data.StockDataObtainer import StockDataObtainer
from thread_runner.ThreadRunner import ThreadRunner
from util.Constants import MINUTES_OF_DATA_TO_LOOK_AT

"""
Representation invariants:
- _updateTimestamps is a Dict of lists, and each list contains x datetimes,
  where 0 < x <= pricesToKeepTrackOf
- _entries is a Dict of lists, and each list contains x floats, 
  where 0 < x <= pricesToKeepTrackOf. Last element in each list contains most
  recent price.
"""
class TrackedStockDatabase:
    pricesToKeepTrackOf: int
    obtainer: StockDataObtainer
    _secondsBetweenStockUpdates: float

    # PRIVATE:
    _prices: Dict
    _volumes: Dict
    _updateTimestamps: Dict
    _entriesLock: th.Lock
    _stopThread: bool
    _updaterThread: th.Thread
    _instance = None
    _listeners: Dict

    def __init__(self):
        if not TrackedStockDatabase._instance:
            TrackedStockDatabase._instance = self
        else:
            print("Only one instance of EventDispatcher is allowed!")

        self.pricesToKeepTrackOf = MINUTES_OF_DATA_TO_LOOK_AT
        self._prices = {}
        self._volumes = {}
        self._updateTimestamps = {}
        self.obtainer = None
        self._entriesLock = th.Lock()
        self._secondsBetweenStockUpdates = 60.0

    @staticmethod
    def getInstance():
        if not TrackedStockDatabase._instance:
            return TrackedStockDatabase()
        else:
            return TrackedStockDatabase._instance

    def useObtainer(self, obtainer: StockDataObtainer):
        self.obtainer = obtainer
        return self

    def setPricesToKeepTrackOf(self, pricesToKeepTrackOf: int):
        self.pricesToKeepTrackOf = pricesToKeepTrackOf
        return self

    def setSecondsBetweenStockUpdates(self, secondsBetweenStockUpdates: float):
        self._secondsBetweenStockUpdates = secondsBetweenStockUpdates
        return self

    def trackStocksInFilter(self, filter: StockFilter):
        series = filter.filtered_stocks["Ticker"]

        for item in series.iteritems():
            ticker = item[1]
            if self._prices.get(ticker):
                print("Stock " + ticker + " is already being tracked!")
            else:
                self._prices[ticker] = [filter.filtered_stocks.at[item[0], "Price"]]
                self._volumes[ticker] = [filter.filtered_stocks.at[item[0], "Volume"]]
                self._updateTimestamps[ticker] = filter.timestampOfDownload

        self.obtainer.trackStocks(self._prices.keys())
        return self

    def startSelfUpdating(self):
        self._stopThread = False
        self._updaterThread = th.Thread(target=self.update, daemon=True)
        self._updaterThread.start()

    def stopSelfUpdating(self):
        self._stopThread = True
        self._updaterThread.join()

    """
    Returns stock price, or -1 if that stock is not being tracked.
    """
    def getCurrentStockPrice(self, ticker: str, minutesAgo=0) -> float:
        with self._entriesLock:
            try:
                return self._prices[ticker][-1-minutesAgo]
            except KeyError as e:
                print("Tried to obtain " + ticker + "from the database, but "
                                                    "that stock isn't tracked!")
                return -1

    def getCurrentStockVolume(self, ticker: str, minutesAgo=0) -> float:
        with self._entriesLock:
            try:
                return self._volumes[ticker][-1-minutesAgo]
            except KeyError as e:
                print(
                    "Tried to obtain " + ticker + "from the database, but "
                                                  "that stock isn't tracked!")
                return -1

    def getRecentStockPrices(self, ticker: str) -> List[float]:
        with self._entriesLock:
            try:
                return self._prices[ticker]
            except KeyError as e:
                print("Tried to obtain " + ticker + "from the database, but "
                                                    "that stock isn't tracked!")
                return []

    def getRecentStockVolumes(self, ticker: str) -> List[float]:
        with self._entriesLock:
            try:
                return self._volumes[ticker]
            except KeyError as e:
                print("Tried to obtain " + ticker + "from the database, but "
                                                    "that stock isn't tracked!")
                return []

    def update(self):
        while not self._stopThread:
            self._update()

    def _update(self):
        for ticker in self._prices.keys():
            self._updateStock(ticker)

    def getCurrentTime(self) -> datetime:
        return self.obtainer.getCurrentDate()

    def useThreadRunner(self, threadRunner: ThreadRunner):
        f = lambda: self._update()
        threadRunner.runPerdiodically(f)

    def _updateStock(self, ticker: str):
        currDateTime = datetime.now()
        diff = currDateTime - self._updateTimestamps[ticker]

        if int(diff.total_seconds() / self._secondsBetweenStockUpdates) > 0:
            prices, volumes = self.obtainer.obtainPricesAndVolumes(ticker, self.pricesToKeepTrackOf)

            if len(prices) != 0:
                self._updateEntryAndTimeStamp(ticker, prices, volumes)
                EventDispatcher.getInstance().dispatchEvent(ListingPriceUpdatedEvent(ticker))
            else:
                print("Whoa, " + ticker + " had 0 prices!? (TrackedStockDatabase)")


    def _updateEntryAndTimeStamp(self, ticker: str, prices: List[float], volumes: List[float]):
        with self._entriesLock:
            self._prices[ticker] = prices
            self._volumes[ticker] = volumes
            self._updateTimestamps[ticker] = datetime.now()
