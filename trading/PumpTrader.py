from events.Event import Event
from events.EventListener import EventListener
from stock_data.TrackedStockDatabase import TrackedStockDatabase
from trading.PumpTradeTracker import PumpTradeTracker
from datetime import datetime


class PumpTrader(EventListener):
    tracker: PumpTradeTracker
    stockDatabase: TrackedStockDatabase

    def __init__(self):
        self.tracker = PumpTradeTracker()
        self.stockDatabase = TrackedStockDatabase.getInstance()

    def onEvent(self, event: Event):
        if event.type == "PumpAndDump":
            self._onPumpAndDump(event.data["Ticker"], event.data["Price"])

    def _onPumpAndDump(self, ticker: str, price: str):
        pass

    def start(self):
        pass

    def stop(self):
        pass
