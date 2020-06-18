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
from trading.Wallet import Wallet
from wallet.Transactor import Transactor


class ProfitPumpTrader(PumpTrader):
    tracker: PumpTradeTracker
    stockDatabase: TrackedStockDatabase
    profitRatioToAimFor: float
    acceptableLossRatio: float
    minutesAfterSell: int
    minutesAfterSellIfPriceInactivity: int
    maxTimeToHoldStock: int
    wallet: Wallet
    investmentStrategy: InvestmentStrategy
    transactor: Transactor
    sellCooldown: Dict

    # Stores ongoing trades in a Dict, with the key being ticker (str)
    # and the value being a list with the time of the trade (datetime) and the
    # highest price it reached (float)
    ongoingTrades: Dict

    # Multithreading stuff
    _tradesLock: th.Lock
    _stopThread: bool
    _updaterThread: th.Thread
    _fastForwardAmount: int

    def __init__(self, investmentStrategy: InvestmentStrategy,
                 transactor: Transactor, profitRatioToAimFor=0.1,
                 acceptableLossRatio=0.1, maxTimeToHoldStock=30,
                 minutesAfterSell=0, minutesAfterSellIfPriceInactivity=0,
                 fastForwardAmount=1, startingFunds=0.0):
        super().__init__(investmentStrategy)
        self.wallet.addFunds(startingFunds)
        self.transactor = transactor
        self.ongoingTrades = {}
        self.sellCooldown = {}
        self.profitRatioToAimFor = profitRatioToAimFor
        self.acceptableLossRatio = acceptableLossRatio
        self.minutesAfterSell = minutesAfterSell
        self.minutesAfterSellIfPriceInactivity = minutesAfterSellIfPriceInactivity
        self.maxTimeToHoldStock = maxTimeToHoldStock
        self._tradesLock = th.Lock()
        self._fastForwardAmount = fastForwardAmount

    def _onPumpAndDump(self, ticker: str, price: float, confidence: float):
        if self.wallet.lacksFunds():
            return

        investment = self.investmentStrategy.getAmountToInvest(self.wallet, price, confidence)
        time = self.stockDatabase.getCurrentTime()

        if ticker in self.sellCooldown and self.sellCooldown[ticker] > self.stockDatabase.getCurrentTime():
            return

        success = self.tracker.addNewTradeIfNotOwned(PumpTrade(ticker, price, investment, buyTimestamp=time))

        if success:
            print("MinutePumpTrader is buying " + ticker + " with " + str(investment) + "...")
            self.transactor.purchase(ticker, investment)

            with self._tradesLock:
                self.ongoingTrades[ticker] = [self.stockDatabase.getCurrentTime(), price]
                self.wallet.removeFunds(investment)

    def start(self):
        self._stopThread = False
        self._updaterThread = th.Thread(target=self.update, daemon=True)
        self._updaterThread.start()

    def stop(self):
        self._stopThread = True
        self._updaterThread.join()

    def update(self):
        super().update()

        while not self._stopThread:
            # We will be deleting items as we iterate over them, so we make a
            # copy of the keys first.
            keys = list(self.ongoingTrades.keys())

            for ticker in keys:
                self._updateTrade(ticker)

    def _updateTrade(self, ticker: str):
        currentPrice = self.stockDatabase.getCurrentStockPrice(ticker)
        now = self.stockDatabase.getCurrentTime()

        with self._tradesLock:
            trade = self.tracker.getUnsoldTradeByTicker(ticker)
            time = self.ongoingTrades[ticker][0]

            if trade.buyPrice * (1 + self.profitRatioToAimFor) <= currentPrice:
                print("Making profit on a trade!")
                self._sell(ticker)
            elif self.ongoingTrades[ticker][1] * (1 - self.acceptableLossRatio) >= currentPrice:
                print("Stock's price dipped too much from its peak. Selling stock.")
                self._sell(ticker)
            elif (now - time).total_seconds() / 60 >= self.maxTimeToHoldStock:
                print("Held a stock for too long and decided to sell it.")
                self._sell(ticker, soldDueToPriceInactivity=True)
            elif currentPrice > self.ongoingTrades[ticker][1]:
                self.ongoingTrades[ticker][1] = currentPrice


    def _sell(self, ticker: str, soldDueToPriceInactivity=False):
        print("MinutePumpTrader is selling " + ticker)

        if soldDueToPriceInactivity:
            self.sellCooldown[ticker] = self.stockDatabase.getCurrentTime() + timedelta(minutes=self.minutesAfterSellIfPriceInactivity)
        else:
            self.sellCooldown[ticker] = self.stockDatabase.getCurrentTime() + timedelta(minutes=self.minutesAfterSell)

        # This sells all of the asset.
        self.transactor.sell(ticker, self.transactor.getBalance(ticker))

        # This keeps track of statistics.
        price = self.stockDatabase.getCurrentStockPrice(ticker)
        time = self.stockDatabase.getCurrentTime()
        returns = self.tracker.getUnsoldTradeByTicker(ticker).sell(price, sellTimestamp=time)
        self.ongoingTrades.pop(ticker)
        self.wallet.addFunds(returns)
