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

    def sell(self, sellPrice: float) -> float:
        """
        Sells the asset.
        :param sellPrice: the price at which the asset was sold.
        :return: the amount of funds obtained from the sale.
        """
        print("Selling " + self.ticker + "...")
        self.sellPrice = sellPrice
        self.sellTimestamp = datetime.now()
        return (sellPrice / self.buyPrice) * self.investment

    def wasSold(self) -> bool:
        return self.sellPrice >= 0.0

    def __str__(self) -> str:
        ticker: str
        buyPrice: float
        sellPrice: float
        investment: float
        buyTimestamp: datetime
        sellTimestamp: datetime
        return "PumpTrade(" + str(self.ticker) + ", buy: " + str(self.buyPrice)\
            + " " + str(self.buyTimestamp) + ", sell: " + str(self.sellPrice) + " "\
            + str(self.sellTimestamp) + ", investment: " + str(self.investment)\
            + ", profit: " + str(self.calculateProfit()) + ")\n"

    def calculateProfit(self):
        if not self.wasSold():
            profit = 0.0
        else:
            profit = (self.sellPrice - self.buyPrice) * self.investment

        return profit
