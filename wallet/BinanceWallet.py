"""
A wallet tied to Binance.
"""
import json

import binance
import requests

from util.Constants import BINANCE_DATA_FETCH_ATTEMPT_AMOUNT
from wallet.Wallet import Wallet
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceWithdrawException
from decimal import *

class BinanceWallet(Wallet):
    client: Client
    withdrawAddress: str

    # Amount of times to try to get data with the Binance API if we fail to get
    # it the first time:
    _tryAmount: int

    def __init__(self, withdrawAddress="", binanceKey="", binanceAPIKey=""):
        if binanceKey is None or binanceAPIKey is None:
            self.client = None
        else:
            self.client = Client(api_key=binanceKey,
                                 api_secret=binanceAPIKey)

        self.withdrawAddress = withdrawAddress
        self._tryAmount = BINANCE_DATA_FETCH_ATTEMPT_AMOUNT

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

    def purchase(self, ticker: str, amountInPurchaseCurrency: float, test=True) -> bool:
        """
        Purchases a cryptocurrency.
        :param ticker: what to purchase
        :param amountInPurchaseCurrency: the amount to purchase, units: ticker
        :param test: whether this is a test order or a real one
        :return: success of the transaction
        """
        for i in range(self._tryAmount):
            try:
                if test:
                    # quantity is the amount in the purchase currency!
                    self.client.create_test_order(
                        symbol=ticker,
                        side=Client.SIDE_BUY,
                        type=Client.ORDER_TYPE_MARKET,
                        quantity=amountInPurchaseCurrency)
                    return True
                else:
                    getcontext().prec = 5
                    self.client.create_order(
                        symbol=ticker,
                        side=Client.SIDE_BUY,
                        type=Client.ORDER_TYPE_MARKET,
                        quantity=Decimal(amountInPurchaseCurrency))
                    return True
            except binance.exceptions.BinanceAPIException as e:
                print(
                    "purchase failed to work for " + ticker + "! BinanceAPIException. Trying " + str(
                        self._tryAmount - 1 - i) + " more times.")
                print(e)
            except requests.exceptions.ReadTimeout as e:
                print(
                    "purchase failed to work for " + ticker + "! ReadTimeout. Trying " + str(
                        self._tryAmount - 1 - i) + " more times.")
                print(e)
            except:
                print(
                    "purchase failed to work for " + ticker + "! Unknown. Trying " + str(
                        self._tryAmount - 1 - i) + " more times.")

        return False

    def sell(self, ticker: str, amountInSellCurrency: float, test=True) -> bool:
        """
        Sells a cryptocurrency.
        :param ticker: what to sell
        :param amountInSellCurrency: the amount to sell, units: ticker
        :return: success of the transaction
        """
        for i in range(self._tryAmount):
            try:
                if test:
                    self.client.create_test_order(
                        symbol=ticker,
                        side=Client.SIDE_SELL,
                        type=Client.ORDER_TYPE_MARKET,
                        quantity=amountInSellCurrency)
                    return True
                else:
                    self.client.create_order(
                        symbol=ticker,
                        side=Client.SIDE_SELL,
                        type=Client.ORDER_TYPE_MARKET,
                        quantity=amountInSellCurrency)
                    return True
            except binance.exceptions.BinanceAPIException as e:
                print(
                    "sell failed to work for " + ticker + "! BinanceAPIException. Trying " + str(
                        self._tryAmount - 1 - i) + " more times.")
                print(e)
            except requests.exceptions.ReadTimeout as e:
                print(
                    "sell failed to work for " + ticker + "! ReadTimeout. Trying " + str(
                        self._tryAmount - 1 - i) + " more times.")
                print(e)
            except:
                print(
                    "sell failed to work for " + ticker + "! Unknown. Trying " + str(
                        self._tryAmount - 1 - i) + " more times.")

        return False

    def getBalance(self, ticker="BTC") -> float:
        """
        Returns amount owned of stock/cryptocurrency.
        :param ticker: the asset
        :return: amount owned, units: ticker
        """
        for i in range(self._tryAmount):
            try:
                return float(self.client.get_asset_balance(asset=ticker)["free"])
            except binance.exceptions.BinanceAPIException as e:
                print(
                    "getBalance failed to work for " + ticker + "! BinanceAPIException. Trying " + str(
                        self._tryAmount - 1 - i) + " more times.")
                print(e)
            except requests.exceptions.ReadTimeout as e:
                print(
                    "getBalance failed to work for " + ticker + "! ReadTimeout. Trying " + str(
                        self._tryAmount - 1 - i) + " more times.")
                print(e)
            except:
                print(
                    "getBalance failed to work for " + ticker + "! Unknown. Trying " + str(
                        self._tryAmount - 1 - i) + " more times.")

        return 0.0

    def getBalanceLocked(self, ticker="BTC") -> float:
        """
        Returns amount owned of locked stock/cryptocurrency.
        :param ticker: the asset
        :return: amount owned, units: ticker
        """
        for i in range(self._tryAmount):
            try:
                return float(self.client.get_asset_balance(asset=ticker)["locked"])
            except binance.exceptions.BinanceAPIException as e:
                print(
                    "getBalanceLocked failed to work for " + ticker + "! BinanceAPIException. Trying " + str(
                        self._tryAmount - 1 - i) + " more times.")
                print(e)
            except requests.exceptions.ReadTimeout as e:
                print(
                    "getBalanceLocked failed to work for " + ticker + "! ReadTimeout. Trying " + str(
                        self._tryAmount - 1 - i) + " more times.")
                print(e)
            except:
                print(
                    "getBalanceLocked failed to work for " + ticker + "! Unknown. Trying " + str(
                        self._tryAmount - 1 - i) + " more times.")

        return 0.0

    def getDepositAddress(self, ticker="BTC") -> str:
        for i in range(self._tryAmount):
            try:
                return self.client.get_deposit_address(asset=ticker)["address"]
            except binance.exceptions.BinanceAPIException as e:
                print(
                    "getDepositAddress failed to work for " + ticker + "! BinanceAPIException. Trying " + str(
                        self._tryAmount - 1 - i) + " more times.")
                print(e)
            except requests.exceptions.ReadTimeout as e:
                print(
                    "getBalance failed to work for " + ticker + "! ReadTimeout. Trying " + str(
                        self._tryAmount - 1 - i) + " more times.")
                print(e)
            except:
                print(
                    "getBalance failed to work for " + ticker + "! Unknown. Trying " + str(
                        self._tryAmount - 1 - i) + " more times.")

        return ""

    def getWithdrawals(self, ticker=""):
        for i in range(self._tryAmount):
            try:
                if ticker == "":
                    withdraws = self.client.get_withdraw_history()
                    return withdraws

                withdraws = self.client.get_withdraw_history(asset=ticker)
                return withdraws
            except binance.exceptions.BinanceAPIException as e:
                print(
                    "getWithdrawals failed to work for " + ticker + "! BinanceAPIException. Trying " + str(
                        self._tryAmount - 1 - i) + " more times.")
                print(e)
            except requests.exceptions.ReadTimeout as e:
                print(
                    "getWithdrawals failed to work for " + ticker + "! ReadTimeout. Trying " + str(
                        self._tryAmount - 1 - i) + " more times.")
                print(e)
            except:
                print(
                    "getWithdrawals failed to work for " + ticker + "! Unknown. Trying " + str(
                        self._tryAmount - 1 - i) + " more times.")

        return 0.0

    def getTradeFee(self, ticker: str):
        for i in range(self._tryAmount):
            try:
                return self.client.get_trade_fee(symbol=ticker)
            except binance.exceptions.BinanceAPIException as e:
                print(
                    "getTradeFee failed to work for " + ticker + "! BinanceAPIException. Trying " + str(
                        self._tryAmount - 1 - i) + " more times.")
                print(e)
            except requests.exceptions.ReadTimeout as e:
                print(
                    "getTradeFee failed to work for " + ticker + "! ReadTimeout. Trying " + str(
                        self._tryAmount - 1 - i) + " more times.")
                print(e)
            except:
                print(
                    "getTradeFee failed to work for " + ticker + "! Unknown. Trying " + str(
                        self._tryAmount - 1 - i) + " more times.")

        return 0.0
