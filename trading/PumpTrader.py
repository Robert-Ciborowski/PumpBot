from events.Event import Event
from events.EventListener import EventListener
from trading.PumpTradeTracker import PumpTradeTracker


class PumpTrader(EventListener):
    tracker: PumpTradeTracker

    def __init__(self):
        self.tracker = PumpTradeTracker()

    def onEvent(self, event: Event):
        if event.type == "PumpAndDump":
            self._onPumpAndDump(event.data["Ticker"], event.data["Price"])

    def _onPumpAndDump(self, ticker: str, price: str):
        pass
