"""
An abstract class which makes transactions.
"""

class Wallet:
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

    def getBalance(self, ticker="BTC") -> float:
        """
        Returns amount owned of stock/cryptocurrency.
        :param ticker: the asset
        :return: amount owned
        """
        pass

    def getPortionOfBalance(self, portion: float, ticker="BTC") -> float:
        """
        Returns a certain portion of the balance.
        Precondition: 0 <= portion <= 1
        :param portion: the portion of the funds, e.g. 0.5 for 50%
        :return: the portion
        """
        return self.getBalance(ticker) * portion

    def lacksFunds(self, ticker="BTC"):
        return self.getBalance(ticker) <= 0
