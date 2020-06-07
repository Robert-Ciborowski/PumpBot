"""
Makes transactions on Binance.
"""
from transactors.Transactor import Transactor
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceWithdrawException

class BinanceTransactor(Transactor):
    client: Client
    withdrawAddress: str

    def __init__(self, binanceKey: str, binanceAPIKey: str, withdrawAddress: str):
        self.client = Client(api_key=binanceKey,
                                api_secret=binanceAPIKey)
        self.withdrawAddress = withdrawAddress

    def purchase(self, ticker: str, amount: float, test=True) -> bool:
        """
        Purschases a cryptocurrency.
        :param ticker: what to purchase
        :param amount: the amount to purchase
        :param test: whether this is a test order or a real one
        :return: success of the transaction
        """
        if test:
            order = self.client.create_order(
                symbol=ticker,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=amount)
        else:
            order = self.client.create_order(
                symbol=ticker,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=amount)
        return order["status"] == "FILLED"

    def sell(self, ticker: str, amount: float) -> bool:
        """
        Sells a cryptocurrency.
        :param ticker: what to sell
        :param amount: the amount to sell
        :return: success of the transaction
        """
        try:
            result = self.client.withdraw(asset=ticker,
                                          address=self.withdrawAddress,
                                          amount=amount)
        except BinanceAPIException as e:
            print(e)
            return False
        except BinanceWithdrawException as e:
            print(e)
            return False
        else:
            return True

    def getBalance(self, ticker: str) -> float:
        """
        Returns amount owned of stock/cryptocurrency.
        :param ticker: the asset
        :return: amount owned
        """
        return self.client.get_asset_balance(asset=ticker)

    def getDepositAddress(self, coin="BTC") -> str:
        pass
        # Need to test this since idk its return type
        # return self.client.get_deposit_address(asset=coin)

    def getWithdrawals(self, coin=""):
        if coin == "":
            withdraws = self.client.get_withdraw_history()
            return withdraws

        withdraws = self.client.get_withdraw_history(asset=coin)
        return withdraws

    def getTradeFee(self, coin: str):
        return self.client.get_trade_fee(symbol=coin)
