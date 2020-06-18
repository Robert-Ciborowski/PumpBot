"""
An abstract class which makes transactions.
"""

class Transactor:
    def purchase(self, ticker: str, amount: float) -> bool:
        """
        Purschases a stock/cryptocurrency.
        :param ticker: what to purchase
        :param amount: the amount to purchase
        :return: success of the transaction
        """
        pass

    def sell(self, ticker: str, amount: float) -> bool:
        """
        Sells a stock/cryptocurrency.
        :param ticker: what to sell
        :param amount: the amount to sell
        :return: success of the transaction
        """
        pass

    def getBalance(self, ticker: str) -> float:
        """
        Returns amount owned of stock/cryptocurrency.
        :param ticker: the asset
        :return: amount owned
        """
        pass
