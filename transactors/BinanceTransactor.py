"""
Makes transactions on Binance.
"""
from transactors.Transactor import Transactor


class BinanceTransactor(Transactor):
    def purchase(self, ticker: str, amount: float) -> bool:
        """
        Purschases a cryptocurrency.
        :param ticker: what to purchase
        :param amount: the amount to purchase
        :return: success of the transaction
        """
        pass

    def sell(self, ticker: str, amount: float) -> bool:
        """
        Sells a cryptocurrency.
        :param ticker: what to sell
        :param amount: the amount to sell
        :return: success of the transaction
        """
        pass
