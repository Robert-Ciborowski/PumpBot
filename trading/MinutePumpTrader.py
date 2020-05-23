"""
Trades by buying when the pump is detected and selling a certain number of
minutes later. This class updates itself on a seperate thread so that
stocks are sold at the right time.
"""
from datetime import datetime
from typing import Dict
import threading as th

from stock_data.TrackedStockDatabase import TrackedStockDatabase
from trading.PumpTrade import PumpTrade
from trading.PumpTradeTracker import PumpTradeTracker
from trading.PumpTrader import PumpTrader

class MinutePumpTrader(PumpTrader):
    tracker: PumpTradeTracker
    stockDatabase: TrackedStockDatabase
    minutesBeforeSell: int

    # Stores ongoing trades in a Dict, with the key being ticker (str)
    # and the value being the time of the trade (datetime)
    ongoingTrades: Dict

    # Multithreading stuff
    _tradesLock: th.Lock
    _stopThread: bool
    _updaterThread: th.Thread

    def __init__(self, stockDatabase: TrackedStockDatabase, minutesBeforeSell=1):
        super().__init__(stockDatabase)
        self.tracker = PumpTradeTracker()
        self.ongoingTrades = {}
        self.minutesBeforeSell = minutesBeforeSell
        self._tradesLock = th.Lock()

    def _onPumpAndDump(self, ticker: str, price: str):
        success = self.tracker.addNewTradeIfNotOwned(PumpTrade(ticker, price))

        if success:
            with self._tradesLock:
                self.ongoingTrades[ticker] = datetime.now()

    def start(self):
        self._stopThread = False
        self._updaterThread = th.Thread(target=self.update, daemon=True)
        self._updaterThread.start()

    def stop(self):
        self._stopThread = True
        self._updaterThread.join()

    def update(self):
        while not self._stopThread:
            for ticker in self.ongoingTrades.keys():
                self._updateTrade(ticker)

    def _updateTrade(self, ticker: str):
        now = datetime.now()

        with self._tradesLock:
            time = self.ongoingTrades[ticker]

            if (now - time).min >= self.minutesBeforeSell:
                self._sell(ticker)
        pass

    def _sell(self, ticker: str):
        price = self.stockDatabase.getCurrentStockPrice(ticker)
        self.tracker.getTradeByTicker(ticker).sell(price)
        self.ongoingTrades.pop(ticker)
