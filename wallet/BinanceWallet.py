"""
A wallet tied to Binance.
"""
import json

import binance

from wallet.Wallet import Wallet
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceWithdrawException


class BinanceWallet(Wallet):
    client: Client
    withdrawAddress: str

    def __init__(self, withdrawAddress="", binanceKey="", binanceAPIKey=""):
        if binanceKey is None or binanceAPIKey is None:
            self.client = None
        else:
            self.client = Client(api_key=binanceKey,
                                 api_secret=binanceAPIKey)

        self.withdrawAddress = withdrawAddress

    def useBinanceKeysFromFile(self, propertiesFile: str):
        try:
            with open(propertiesFile, mode='r') as file:
                data = json.load(file)
                apiKey = data["API Key"]
                apiKeySecret = data["API Key Secret"]
                self.withdrawAddress = data["Wallet"]
                self.client = Client(api_key=apiKey,
                                     api_secret=apiKeySecret)
        except:
            print(
                "You are missing " + propertiesFile + ". Please ask Robert " \
                                                      "(robert.ciborowski"
                                                      "@mail.utoronto.ca) for "
                                                      "help.")

    def purchase(self, ticker: str, amountInBaseCurrency: float,
                 amountInPurchaseCurrency: float, test=True) -> bool:
        """
        Purchases a cryptocurrency.
        :param ticker: what to purchase
        :param amount: the amount to purchase, units: ticker
        :param test: whether this is a test order or a real one
        :return: success of the transaction
        """
        try:
            if test:
                self.client.create_test_order(
                    symbol=ticker,
                    side=Client.SIDE_BUY,
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=amountInPurchaseCurrency)
                print(
                    "BinanceWallet purchase still needs to be tested to see if it "
                    "takes in quantity in buy currency or BTC!")
            else:
                print(
                    "BinanceWallet purchase still needs to be tested to see if it "
                    "takes in quantity in buy currency or BTC!")
                # self.client.create_order(
                #     symbol=ticker,
                #     side=Client.SIDE_BUY,
                #     type=Client.ORDER_TYPE_MARKET,
                #     quantity=amountInPurchaseCurrency)
        except binance.exceptions.BinanceAPIException as e:
            print("A BinanceTransactor transaction failed to occur!")
            print(e)
            return False
        except:
            print("A BinanceTransactor transaction failed to occur! No details.")
            return False

        return True

    def sell(self, ticker: str, amountInBaseCurrency: float,
             amountInSellCurrency: float, test=True) -> bool:
        """
        Sells a cryptocurrency.
        :param ticker: what to sell
        :param amount: the amount to sell, units: ticker
        :return: success of the transaction
        """
        try:
            if test:
                self.client.create_test_order(
                    symbol=ticker,
                    side=Client.SIDE_SELL,
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=amountInSellCurrency)
                print("BinanceWallet sell still needs to be tested to see if it "
                      "takes in quantity in sell currency or BTC!")
            else:
                print(
                    "BinanceWallet sell still needs to be tested to see if it "
                    "takes in quantity in sell currency or BTC!")
                # self.client.create_order(
                #     symbol=ticker,
                #     side=Client.SIDE_SELL,
                #     type=Client.ORDER_TYPE_MARKET,
                #     quantity=amountInSellCurrency)
        except binance.exceptions.BinanceAPIException as e:
            print("A BinanceTransactor transaction failed to occur!")
            print(e)
            return False
        except:
            print("A BinanceTransactor transaction failed to occur! No details.")
            return False

        return True

    def getBalance(self, ticker="BTC") -> float:
        """
        Returns amount owned of stock/cryptocurrency.
        :param ticker: the asset
        :return: amount owned, units: ticker
        """
        return self.client.get_asset_balance(asset=ticker)["free"]

    def getBalanceLocked(self, ticker="BTC") -> float:
        """
        Returns amount owned of locked stock/cryptocurrency.
        :param ticker: the asset
        :return: amount owned, units: ticker
        """
        return self.client.get_asset_balance(asset=ticker)["locked"]

    def getDepositAddress(self, coin="BTC") -> str:
        return self.client.get_deposit_address(asset=coin)["address"]

    def getWithdrawals(self, coin=""):
        if coin == "":
            withdraws = self.client.get_withdraw_history()
            return withdraws

        withdraws = self.client.get_withdraw_history(asset=coin)
        return withdraws

    def getTradeFee(self, coin: str):
        return self.client.get_trade_fee(symbol=coin)
