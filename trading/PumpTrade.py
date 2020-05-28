"""
A trade which begins with a buy, and ends with a sell.
"""
from datetime import datetime


class PumpTrade:
    ticker: str
    buyPrice: float
    sellPrice: float
    investment: float
    buyTimestamp: datetime
    sellTimestamp: datetime

    def __init__(self, ticker: str, buyPrice: float, investment: float, buyTimestamp=None, sellTimestamp=None):
        self.ticker = ticker
        self.buyPrice = buyPrice
        self.investment = investment
        self.sellPrice = -1.0

        if buyTimestamp is None:
            self.buyTimestamp = datetime.now()
        else:
            self.buyTimestamp = buyTimestamp

        self.sellTimestamp = sellTimestamp

    def sell(self, sellPrice: float):
        self.sellPrice = sellPrice
        self.sellTimestamp = datetime.now()

    def wasSold(self) -> bool:
        return self.sellPrice >= 0.0
