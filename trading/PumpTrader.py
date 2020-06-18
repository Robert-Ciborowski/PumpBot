from events.Event import Event
from events.EventListener import EventListener
from stock_data.TrackedStockDatabase import TrackedStockDatabase
from trading.InvestmentStrategy import InvestmentStrategy
from trading.PumpTradeTracker import PumpTradeTracker
from datetime import datetime, timedelta

from trading.Wallet import Wallet


class PumpTrader(EventListener):
    tracker: PumpTradeTracker
    stockDatabase: TrackedStockDatabase
    wallet: Wallet
    investmentStrategy: InvestmentStrategy

    _lastProfitOutputTime: datetime
    _minutesBetweenProfitOutputs: int

    def __init__(self, investmentStrategy: InvestmentStrategy):
        self.tracker = PumpTradeTracker()
        self.stockDatabase = TrackedStockDatabase.getInstance()
        self.wallet = Wallet()
        self.investmentStrategy = investmentStrategy
        self._lastProfitOutputTime = datetime(year=1970, month=1, day=1)
        self._minutesBetweenProfitOutputs = 30

    def onEvent(self, event: Event):
        if event.type == "PumpAndDump":
            self._onPumpAndDump(event.data["Ticker"], event.data["Price"], event.data["Confidence"])

    def update(self):
        if self.stockDatabase.getCurrentTime() >= self._lastProfitOutputTime + timedelta(minutes=self._minutesBetweenProfitOutputs):
            self._lastProfitOutputTime = self.stockDatabase.getCurrentTime()
            print("Money left in wallet: " + str(self.wallet.getPortionOfFunds(1.0)))
            print("Profits:")
            print(self.tracker.calculateProfits())

    def _onPumpAndDump(self, ticker: str, price: str, confidence: float):
        pass

    def start(self):
        pass

    def stop(self):
        pass
