"""
An investment strategy in which the funds that are invested are based on
a predefined fraction.
"""
from trading.InvestmentStrategy import InvestmentStrategy
from wallet.Wallet import Wallet


class BasicInvestmentStrategy(InvestmentStrategy):
    investmentFraction: float

    def __init__(self, investmentFraction=0.0):
        self.investmentFraction = investmentFraction

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
        return wallet.getPortionOfBalance(self.investmentFraction)
