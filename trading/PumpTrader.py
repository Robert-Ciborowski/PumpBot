import pytz

from events.Event import Event
from events.EventListener import EventListener
from stock_data.TrackedStockDatabase import TrackedStockDatabase
from thread_runner.ThreadRunner import ThreadRunner
from trading.InvestmentStrategy import InvestmentStrategy
from trading.PumpTradeTracker import PumpTradeTracker
from datetime import datetime, timedelta

from wallet.Wallet import Wallet


class PumpTrader(EventListener):
    tracker: PumpTradeTracker
    stockDatabase: TrackedStockDatabase
    wallet: Wallet
    investmentStrategy: InvestmentStrategy

    _lastProfitOutputTime: datetime
    _minutesBetweenProfitOutputs: int

    def __init__(self, investmentStrategy: InvestmentStrategy, wallet: Wallet):
        self.tracker = PumpTradeTracker()
        self.stockDatabase = TrackedStockDatabase.getInstance()
        self.wallet = wallet
        self.investmentStrategy = investmentStrategy
        self._lastProfitOutputTime = datetime(year=1970, month=1, day=1)
        self.timezone = "Etc/GMT-0"
        timezone = pytz.timezone(self.timezone)
        self._lastProfitOutputTime = timezone.localize(self._lastProfitOutputTime)
        self._minutesBetweenProfitOutputs = 30

    def onEvent(self, event: Event):
        if event.type == "PumpAndDump":
            self._onPumpAndDump(event.data["Ticker"], event.data["Price"], event.data["Confidence"])

    def _outputProfitsSoFar(self):
        if self.stockDatabase.getCurrentTime() >= self._lastProfitOutputTime + timedelta(minutes=self._minutesBetweenProfitOutputs):
            self._lastProfitOutputTime = self.stockDatabase.getCurrentTime()
            print("Money left in wallet: " + str(self.wallet.getBalance()))
            print("Profits so far:")
            print(self.tracker.calculateProfits())

    def _onPumpAndDump(self, ticker: str, price: str, confidence: float):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def runUntil(self, endTime: datetime):
        pass

    def useThreadRunner(self, threadRunner: ThreadRunner):
        pass
