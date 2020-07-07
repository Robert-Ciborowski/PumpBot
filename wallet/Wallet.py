"""
An abstract class which makes transactions.
"""
from stock_data.StockDataObtainer import StockDataObtainer


class Wallet:
    def purchase(self, ticker: str, amountInBaseCurrency: float,
                 amountInPurchaseCurrency: float, test=True) -> bool:
        """
        Purschases a stock/cryptocurrency.
        :param ticker: what to purchase
        :param amount: the amount to purchase, units: ticker
        :return: success of the transaction
        """
        pass

    def sell(self, ticker: str, amountInBaseCurrency: float,
             amountInSellCurrency: float, test=True) -> bool:
        """
        Sells a stock/cryptocurrency.
        :param ticker: what to sell
        :param amount: the amount to sell, units: ticker
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
