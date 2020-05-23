"""
Trades by buying when the pump is detected and selling a certain number of
minutes later.
"""
from trading.PumpTrade import PumpTrade
from trading.PumpTradeTracker import PumpTradeTracker
from trading.PumpTrader import PumpTrader


class MinutePumpTrader(PumpTrader):
    tracker: PumpTradeTracker

    def __init__(self):
        super().__init__()

    def _onPumpAndDump(self, ticker: str, price: str):
        self.tracker.addNewTrade(PumpTrade(ticker, price))
