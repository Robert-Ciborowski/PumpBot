"""
An abstract class which is used by PumpTrader to figure out how
much to invest.
"""
from trading.Wallet import Wallet


class InvestmentStrategy:
    def getAmountToInvest(self, wallet: Wallet, price: float,
                          confidence: float) -> float:
        """
        Determines how many funds from the wallet should be used towards an
        investment.
        :param wallet: the trader's wallet
        :param price: the price of the stock/currency
        :param confidence: the confidence of the model that suggested to invest.
        :return: how many funds should be invested.
        """
        pass
