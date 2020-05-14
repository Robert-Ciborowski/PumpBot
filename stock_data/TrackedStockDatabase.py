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
    secondsBetweenStockUpdates: int

    # PRIVATE:
    _entries: Dict
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

        self.pricesToKeepTrackOf = 5
        self._entries = {}
        self._updateTimestamps = {}
        self.obtainer = None
        self._entriesLock = th.Lock()
        self.secondsBetweenStockUpdates = 60

    @staticmethod
    def getInstance():
        if not TrackedStockDatabase._instance:
            return TrackedStockDatabase()
        else:
            return TrackedStockDatabase._instance

    def useObtainer(self, obtainer: StockDataObtainer):
        self.obtainer = obtainer
        return self

    # def trackStock(self, ticker: str) -> TrackedStockDatabase:
    #     if self._entries.get(ticker):
    #         print("Stock " + ticker + " is already being tracked!")
    #     else:
    #         self._entries[ticker] = []
    #         self._updateTimestamps[ticker] = [datetime(1970, 1, 1)]
    #
    #     return self

    def setPricesToKeepTrackOf(self, pricesToKeepTrackOf: int):
        self.pricesToKeepTrackOf = pricesToKeepTrackOf
        return self

    def setSecondsBetweenStockUpdates(self, secondsBetweenStockUpdates: int):
        self.secondsBetweenStockUpdates = secondsBetweenStockUpdates
        return self

    def trackStocksInFilter(self, filter: StockFilter):
        series = filter.filtered_stocks["Ticker"]

        for item in series.iteritems():
            ticker = item[1]
            if self._entries.get(ticker):
                print("Stock " + ticker + " is already being tracked!")
            else:
                self._entries[ticker] = [filter.filtered_stocks.at[item[0], "Price"]]
                self._updateTimestamps[ticker] = filter.timestampOfDownload

        self.obtainer.trackStocks(self._entries.keys())
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
    def getCurrentStockPrice(self, ticker: str) -> float:
        with self._entriesLock:
            try:
                return self._entries[ticker][-1]
            except KeyError as e:
                print("Tried to obtain " + ticker + "from the database, but "
                                                    "that stock isn't tracked!")
                return -1

    def getRecentStockPrices(self, ticker: str) -> List[float]:
        with self._entriesLock:
            try:
                return self._entries[ticker]
            except KeyError as e:
                print("Tried to obtain " + ticker + "from the database, but "
                                                    "that stock isn't tracked!")
                return []

    def update(self):
        while not self._stopThread:
            for ticker in self._entries.keys():
                self._updateStock(ticker)

    def _updateStock(self, ticker: str):
        currDateTime = datetime.now()
        diff = currDateTime - self._updateTimestamps[ticker]

        if int(diff.total_seconds() / self.secondsBetweenStockUpdates) > 0:
            lst = self.obtainer.obtainPrices(ticker, self.pricesToKeepTrackOf)

            if len(lst) != 0:
                self._updateEntryAndTimeStamp(ticker, lst)
                EventDispatcher.getInstance().dispatchEvent(ListingPriceUpdatedEvent(ticker))



    def _updateEntryAndTimeStamp(self, ticker: str, values: List[float]):
        with self._entriesLock:
            self._entries[ticker] = values
            self._updateTimestamps[ticker] = datetime.now()
