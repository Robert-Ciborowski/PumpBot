from events.Event import Event
from events.EventListener import EventListener
from stock_data.TrackedStockDatabase import TrackedStockDatabase
from trading.InvestmentStrategy import InvestmentStrategy
from trading.PumpTradeTracker import PumpTradeTracker
from datetime import datetime

from trading.Wallet import Wallet


class PumpTrader(EventListener):
    tracker: PumpTradeTracker
    stockDatabase: TrackedStockDatabase
    wallet: Wallet
    investmentStrategy: InvestmentStrategy

    def __init__(self, investmentStrategy: InvestmentStrategy):
        self.tracker = PumpTradeTracker()
        self.stockDatabase = TrackedStockDatabase.getInstance()
        self.wallet = Wallet()
        self.investmentStrategy = investmentStrategy

    def onEvent(self, event: Event):
        if event.type == "PumpAndDump":
            self._onPumpAndDump(event.data["Ticker"], event.data["Price"], event.data["confidence"])

    def _onPumpAndDump(self, ticker: str, price: str, confidence: float):
        pass

    def start(self):
        pass

    def stop(self):
        pass
