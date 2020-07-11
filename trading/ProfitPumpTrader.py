"""
Trades by buying when the pump is detected and selling a certain number of
minutes later. This class updates itself on a seperate thread so that
stocks are sold at the right time.
"""
from datetime import datetime, timedelta
from typing import Dict
import threading as th

from stock_data.TrackedStockDatabase import TrackedStockDatabase
from thread_runner.ThreadRunner import ThreadRunner
from trading.InvestmentStrategy import InvestmentStrategy
from trading.PumpTrade import PumpTrade
from trading.PumpTradeTracker import PumpTradeTracker
from trading.PumpTrader import PumpTrader
from util.Constants import TEST_MODE
from wallet.Wallet import Wallet


class ProfitPumpTrader(PumpTrader):
    tracker: PumpTradeTracker
    stockDatabase: TrackedStockDatabase
    profitRatioToAimFor: float
    acceptableLossRatio: float
    acceptableDipFromStartRatio: float
    minutesAfterSellIfPump: int
    minutesAfterSellIfPriceInactivity: int
    minutesAfterSellIfLoss: int
    maxTimeToHoldStock: int
    unprofitableTradesPerDay: int
    wallet: Wallet
    investmentStrategy: InvestmentStrategy
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
                 wallet: Wallet, profitRatioToAimFor=0.1,
                 acceptableLossRatio=0.1, acceptableDipFromStartRatio=0.1,
                 maxTimeToHoldStock=30, minutesAfterSellIfPump=0,
                 minutesAfterSellIfPriceInactivity=0, minutesAfterSellIfLoss=0,
                 unprofitableTradesPerDay=5, fastForwardAmount=1):
        super().__init__(investmentStrategy, wallet)
        self.ongoingTrades = {}
        self.sellCooldown = {}
        self.profitRatioToAimFor = profitRatioToAimFor
        self.acceptableLossRatio = acceptableLossRatio
        self.acceptableDipFromStartRatio = acceptableDipFromStartRatio
        self.minutesAfterSellIfPump = minutesAfterSellIfPump
        self.minutesAfterSellIfPriceInactivity = minutesAfterSellIfPriceInactivity
        self.minutesAfterSellIfLoss = minutesAfterSellIfLoss
        self.maxTimeToHoldStock = maxTimeToHoldStock
        self.unprofitableTradesPerDay = unprofitableTradesPerDay
        self._tradesLock = th.Lock()
        self._fastForwardAmount = fastForwardAmount

    def _onPumpAndDump(self, ticker: str, price: float, confidence: float):
        if self.wallet.lacksFunds():
            print("Did not buy " + ticker + " because wallet lacks funds.")
            return

        investment = self.investmentStrategy.getAmountToInvest(self.wallet, price, confidence)
        time = self.stockDatabase.getCurrentTime()

        if ticker in self.sellCooldown and self.sellCooldown[ticker] > time:
            print("Did not buy " + ticker + " due to sell cooldown.")
            return

        if self.tracker.getNumberOfUnprofitableTradesOnDay(ticker, time) >= self.unprofitableTradesPerDay:
            print("Did not buy " + ticker + " due to too many unprofitable trades.")
            return

        pumpTrade = PumpTrade(ticker, price, investment, buyTimestamp=time)
        success = self.tracker.isOwned(pumpTrade)

        if success:
            if self.wallet.purchase(ticker, investment, investment / price, test=TEST_MODE):
                print("MinutePumpTrader is buying " + ticker + " with " + str(
                    investment) + "...")
                self.tracker.addNewTrade(pumpTrade)

                with self._tradesLock:
                    self.ongoingTrades[ticker] = [self.stockDatabase.getCurrentTime(), price, price]
            else:
                print("MinutePumpTrader failed to buy " + ticker + " with " + str(
                    investment) + "...")

    def start(self):
        self._stopThread = False
        self._updaterThread = th.Thread(target=self.update, daemon=True)
        self._updaterThread.start()

    def stop(self):
        self._stopThread = True
        self._updaterThread.join()

    def runUntil(self, endTime: datetime):
        self.update(endTime=endTime)

    def useThreadRunner(self, threadRunner: ThreadRunner):
        f = lambda: self._update()
        threadRunner.runPerdiodically(f)

    def update(self, endTime=None):
        if endTime is None:
            while not self._stopThread:
                self._update()
        else:
            while datetime.now() < endTime:
                self._update()

    def _update(self):
        self._outputProfitsSoFar()

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
                self._sell(ticker, currentPrice, self.minutesAfterSellIfPump)
            elif self.ongoingTrades[ticker][1] * (1 - self.acceptableLossRatio) >= currentPrice:
                print("Stock's price dipped too much from its peak. Selling stock.")
                self._sell(ticker, currentPrice, self.minutesAfterSellIfPriceInactivity)
            elif self.ongoingTrades[ticker][2] * (1 - self.acceptableDipFromStartRatio) >= currentPrice:
                print("Stock's price dipped too much from start price. Selling stock.")
                self._sell(ticker, currentPrice, self.minutesAfterSellIfPriceInactivity)
            elif (now - time).total_seconds() / 60 >= self.maxTimeToHoldStock:
                print("Held a stock for too long and decided to sell it.")
                self._sell(ticker, currentPrice, self.minutesAfterSellIfLoss)
            elif currentPrice > self.ongoingTrades[ticker][1]:
                self.ongoingTrades[ticker][1] = currentPrice

    def _sell(self, ticker: str, price: float, cooldown: int):
        print("MinutePumpTrader is selling " + ticker)
        self.sellCooldown[ticker] = self.stockDatabase.getCurrentTime() + \
                                    timedelta(minutes=cooldown)

        # This sells all of the asset.
        amount = self.wallet.getBalance(ticker)
        self.wallet.sell(ticker, amount * price, amount, test=TEST_MODE)

        # This keeps track of statistics.
        price = self.stockDatabase.getCurrentStockPrice(ticker)
        time = self.stockDatabase.getCurrentTime()
        returns = self.tracker.getUnsoldTradeByTicker(ticker).sell(price * (1.0 - self.wallet.getTransactionFee()), sellTimestamp=time)
        self.ongoingTrades.pop(ticker)
