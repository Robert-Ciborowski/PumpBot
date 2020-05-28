"""
Trades by buying when the pump is detected and selling a certain number of
minutes later. This class updates itself on a seperate thread so that
stocks are sold at the right time.
"""
from datetime import datetime
from typing import Dict
import threading as th

from stock_data.TrackedStockDatabase import TrackedStockDatabase
from trading.InvestmentStrategy import InvestmentStrategy
from trading.PumpTrade import PumpTrade
from trading.PumpTradeTracker import PumpTradeTracker
from trading.PumpTrader import PumpTrader
from trading.Wallet import Wallet


class MinutePumpTrader(PumpTrader):
    tracker: PumpTradeTracker
    stockDatabase: TrackedStockDatabase
    minutesBeforeSell: int
    wallet: Wallet
    investmentStrategy: InvestmentStrategy

    # Stores ongoing trades in a Dict, with the key being ticker (str)
    # and the value being the time of the trade (datetime)
    ongoingTrades: Dict

    # Multithreading stuff
    _tradesLock: th.Lock
    _stopThread: bool
    _updaterThread: th.Thread
    _fastForwardAmount: int

    def __init__(self, investmentStrategy: InvestmentStrategy,
                 minutesBeforeSell=1, fastForwardAmount=1, startingFunds=0.0):
        super().__init__(investmentStrategy)
        self.wallet.addFunds(startingFunds)
        self.tracker = PumpTradeTracker()
        self.ongoingTrades = {}
        self.minutesBeforeSell = minutesBeforeSell
        self._tradesLock = th.Lock()
        self._fastForwardAmount = fastForwardAmount

    def _onPumpAndDump(self, ticker: str, price: float, confidence: float):
        investment = self.investmentStrategy.getAmountToInvest(self.wallet, price, confidence)
        success = self.tracker.addNewTradeIfNotOwned(PumpTrade(ticker, price, investment))

        if success:
            print("MinutePumpTrader is buying " + ticker)
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
            # We will be deleting items as we iterate over them, so we make a
            # copy of the keys first.
            keys = list(self.ongoingTrades.keys())

            for ticker in keys:
                self._updateTrade(ticker)

    def _updateTrade(self, ticker: str):
        now = datetime.now()

        with self._tradesLock:
            time = self.ongoingTrades[ticker]

            if (now - time).total_seconds() * self._fastForwardAmount / 60 >= self.minutesBeforeSell:
                self._sell(ticker)
        pass

    def _sell(self, ticker: str):
        print("MinutePumpTrader is selling " + ticker)
        price = self.stockDatabase.getCurrentStockPrice(ticker)
        self.tracker.getTradeByTicker(ticker).sell(price)
        self.ongoingTrades.pop(ticker)
