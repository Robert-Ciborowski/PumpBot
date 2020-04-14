# Name: Stock Database
# Author: Robert Ciborowski
# Date: 13/04/2020
# Description: Keeps track of stock prices to the minute.

from __future__ import annotations

from typing import Dict
import pandas as pd
import yfinance as yf
import threading as th
from datetime import datetime

from filter import StockFilterByPrice
from stock_data.StockDataObtainer import StockDataObtainer

"""
Representation invariants:
- _updateTimestamps is a Dict of lists, and each list contains x datetimes, 
  where 0 < x <= pricesToKeepTrackOf
- _updateTimestamps is a Dict of lists, and each list contains x floats, 
  where 0 < x <= pricesToKeepTrackOf
"""
class StockDatabase:
    pricesToKeepTrackOf: int
    obtainer: StockDataObtainer

    # PRIVATE:
    _entries: Dict
    _updateTimestamps: Dict
    _entriesLock: th.Lock
    _stopThread: bool
    _updaterThread: th.Thread

    def __init__(self, minutesToKeepTrackOf=5):
        self.pricesToKeepTrackOf = minutesToKeepTrackOf
        self._entries = {}
        self._updateTimestamps = {}
        self.obtainer = None
        self._entriesLock = th.Lock()

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
    def getCurrentStock(self, ticker: str) -> float:
        with self._entriesLock:
            try:
                return self._entries[ticker]
            except KeyError as e:
                print("Tried to obtain " + ticker + "from the database, but "
                                                    "that stock isn't tracked!")
                return -1

    def update(self):
        while not self._stopThread:
            for ticker in self._entries.keys():
                self._updateStock(ticker)

    def _updateStock(self, ticker: str):
        currDateTime = datetime.now()
        diff = currDateTime - self._updateTimestamps[ticker][0]

        if int(diff.total_seconds() / 60) > 0:
            value = self.obtainer.obtainPrice(ticker)

            if value == -1:
                value = self._entries[ticker][0]
                print("Was unable to obtain: " + ticker)
            else:
                print("Was able to obtain: " + ticker)

            self._updateEntryAndTimeStamp(ticker, value)


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
