"""
Trades by buying when the pump is detected and selling a certain number of
minutes later. This class updates itself on a seperate thread so that
stocks are sold at the right time.
"""
from datetime import datetime, timedelta
from typing import Dict
import threading as th

from stock_data.TrackedStockDatabase import TrackedStockDatabase
from trading.InvestmentStrategy import InvestmentStrategy
from trading.PumpTrade import PumpTrade
from trading.PumpTradeTracker import PumpTradeTracker
from trading.PumpTrader import PumpTrader
from util.Constants import TEST_MODE
from wallet.Wallet import Wallet


class MinutePumpTrader(PumpTrader):
    tracker: PumpTradeTracker
    stockDatabase: TrackedStockDatabase
    minutesBeforeSell: int
    minutesAfterSell: int
    timeOfLastSell: datetime
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
                 wallet: Wallet, minutesBeforeSell=1, minutesAfterSell=0,
                 fastForwardAmount=1, startingFunds=0.0):
        super().__init__(investmentStrategy)
        self.wallet.addFunds(startingFunds, wallet)
        self.ongoingTrades = {}
        self.minutesBeforeSell = minutesBeforeSell
        self.minutesAfterSell = minutesAfterSell
        self.timeOfLastSell = datetime(year=1970, month=1, day=1)
        self._tradesLock = th.Lock()
        self._fastForwardAmount = fastForwardAmount

    def _onPumpAndDump(self, ticker: str, price: float, confidence: float):
        if self.wallet.lacksFunds():
            return

        investment = self.investmentStrategy.getAmountToInvest(self.wallet, price, confidence)
        print("Investing " + str(investment) + "...")
        time = self.stockDatabase.getCurrentTime()
        success = self.tracker.isOwned(PumpTrade(ticker, price, investment, buyTimestamp=time))

        if success and self.timeOfLastSell + timedelta(minutes=self.minutesAfterSell) <= datetime.now():
            if self.wallet.purchase(ticker, investment, test=TEST_MODE):
                print("MinutePumpTrader is buying " + ticker)

                with self._tradesLock:
                    self.ongoingTrades[ticker] = datetime.now()
            else:
                print("MinutePumpTrader is failed to buy " + ticker)

    def start(self):
        self._stopThread = False
        self._updaterThread = th.Thread(target=self.update, daemon=True)
        self._updaterThread.start()

    def stop(self):
        self._stopThread = True
        self._updaterThread.join()

    def update(self):
        self._outputProfitsSoFar()

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

    def _sell(self, ticker: str):
        print("MinutePumpTrader is selling " + ticker)
        self.timeOfLastSell = datetime.now()

        # This sells all of the asset.
        self.wallet.sell(ticker, self.wallet.getBalance(ticker), test=TEST_MODE)

        # This keeps track of statistics.
        price = self.stockDatabase.getCurrentStockPrice(ticker)
        time = self.stockDatabase.getCurrentTime()
        returns = self.tracker.getUnsoldTradeByTicker(ticker).sell(price, sellTimestamp=time)
        self.ongoingTrades.pop(ticker)
