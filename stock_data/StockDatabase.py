# Name: Stock Database
# Author: Robert Ciborowski
# Date: 13/04/2020
# Description: Keeps track of stock prices to the minute.

from __future__ import annotations

from typing import Dict, List
import pandas as pd
import yfinance as yf
import threading as th
from datetime import datetime

from events import EventDispatcher
from events.ListingPriceUpdatedEvent import ListingPriceUpdatedEvent
from filter import StockFilterByPrice
from stock_data.StockDataObtainer import StockDataObtainer

"""
Representation invariants:
- _updateTimestamps is a Dict of lists, and each list contains x datetimes, 
  where 0 < x <= pricesToKeepTrackOf
- _entries is a Dict of lists, and each list contains x floats, 
  where 0 < x <= pricesToKeepTrackOf. Last element in each list contains most
  recent price.
"""
class StockDatabase:
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
        if not StockDatabase._instance:
            StockDatabase._instance = self
        else:
            print("Only one instance of EventDispatcher is allowed!")

        self.pricesToKeepTrackOf = 5
        self._entries = {}
        self._updateTimestamps = {}
        self.obtainer = None
        self._entriesLock = th.Lock()
        self.secondsBetweenStockUpdates = 60

    @staticmethod
    def getInstance() -> StockDatabase:
        if not StockDatabase._instance:
            return StockDatabase()
        else:
            return StockDatabase._instance

    def useObtainer(self, obtainer: StockDataObtainer) -> StockDatabase:
        self.obtainer = obtainer
        return self

    # def trackStock(self, ticker: str) -> StockDatabase:
    #     if self._entries.get(ticker):
    #         print("Stock " + ticker + " is already being tracked!")
    #     else:
    #         self._entries[ticker] = []
    #         self._updateTimestamps[ticker] = [datetime(1970, 1, 1)]
    #
    #     return self

    def setPricesToKeepTrackOf(self, pricesToKeepTrackOf: int) -> StockDatabase:
        self.pricesToKeepTrackOf = pricesToKeepTrackOf
        return self

    def setSecondsBetweenStockUpdates(self, secondsBetweenStockUpdates: int) -> StockDatabase:
        self.secondsBetweenStockUpdates = secondsBetweenStockUpdates
        return self

    def trackStocksInFilter(self, filter: StockFilterByPrice) -> StockDatabase:
        series = filter.filtered_stocks["Ticker"]

        for item in series.iteritems():
            ticker = item[1]
            if self._entries.get(ticker):
                print("Stock " + ticker + " is already being tracked!")
            else:
                self._entries[ticker] = [filter.filtered_stocks.at[item[0], "Price"]]
                self._updateTimestamps[ticker] = [filter.timestampOfDownload]

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
                return self._entries[ticker]
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
        diff = currDateTime - self._updateTimestamps[ticker][0]

        if int(diff.total_seconds() / self.secondsBetweenStockUpdates) > 0:
            value = self.obtainer.obtainPrice(ticker)

            if value == -1:
                value = self._entries[ticker][0]
                print("Was unable to obtain: " + ticker)
            else:
                print("Was able to obtain: " + ticker)

            self._updateEntryAndTimeStamp(ticker, value)
            EventDispatcher.getInstance().dispatchEvent(ListingPriceUpdatedEvent(ticker))


    def _updateEntryAndTimeStamp(self, ticker: str, value: float):
        with self._entriesLock:
            entriesRef = self._entries[ticker]
            entriesRef.append(value)
            timestampRef = self._updateTimestamps[ticker]
            timestampRef.append(datetime.now())

            if len(entriesRef) > self.pricesToKeepTrackOf:
                while len(self._entries[ticker]) > self.pricesToKeepTrackOf:
                    self._entries[ticker].pop(0)

                while len(self._updateTimestamps[ticker]) > self.pricesToKeepTrackOf:
                    self._updateTimestamps[ticker].pop(0)
