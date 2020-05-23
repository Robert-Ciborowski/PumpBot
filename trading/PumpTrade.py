"""
A trade which begins with a buy, and ends with a sell.
"""

class PumpTrade:
    ticker: str
    buyPrice: float
    sellPrice: float

    def __init__(self, ticker: str, buyPrice: float):
        self.ticker = ticker
        self.buyPrice = buyPrice
        self.sellPrice = -1.0

    def sell(self, sellPrice: float):
        self.sellPrice = sellPrice

    def wasSold(self) -> bool:
        return self.sellPrice >= 0.0
