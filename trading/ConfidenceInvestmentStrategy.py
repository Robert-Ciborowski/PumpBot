"""
An investment strategy in which the funds that are invested are based on
a linear function of confidence of the investment. You can also multiply the
determined investment amount by a predefined fraction.
"""
from trading.InvestmentStrategy import InvestmentStrategy
from wallet.Wallet import Wallet


class BasicInvestmentStrategy(InvestmentStrategy):
    investmentFraction: float
    confidenceForFullInvestment: float

    def __init__(self, investmentFraction=1.0, confidenceForFullInvestment=0.8):
        self.investmentFraction = investmentFraction
        self.confidenceForFullInvestment = confidenceForFullInvestment

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
        if confidence > self.confidenceForFullInvestment:
            confidenceMultiplier = 1.0
        else:
            confidenceMultiplier = confidence / self.confidenceForFullInvestment

        return wallet.getPortionOfBalance(self.investmentFraction) * confidenceMultiplier
