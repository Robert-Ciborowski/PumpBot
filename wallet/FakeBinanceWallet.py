"""
A simple wallet for testing.
"""
import json
from typing import Dict

from wallet.Wallet import Wallet

class FakeBinanceWallet(Wallet):
    baseCurrencyAmount: float
    baseCurrencyName: str
    binanceFee: float
    minimumTradeAmount: float
    balances: Dict

    def __init__(self, baseCurrencyAmount=0.0, binanceFee=0.1, minimumTradeAmount=0.0001):
        self.baseCurrencyAmount = baseCurrencyAmount
        self.baseCurrencyName = "BTC"
        self.binanceFee = binanceFee
        self.minimumTradeAmount = minimumTradeAmount
        self.balances = {}

    def purchase(self, ticker: str, amount: float, test=True) -> bool:
        """
        Purchases a cryptocurrency.
        :param ticker: what to purchase
        :param amount: the amount to purchase
        :param test: whether this is a test order or a real one
        :return: success of the transaction
        """
        if amount < self.minimumTradeAmount:
            print(
                "Tried to purchase " + ticker + " but amount is too small: " + str(amount) + " (FakeBinanceWallet).")
            return False

        if self.baseCurrencyAmount <= amount:
            print("Tried to purchase " + ticker + " with more funds than available (FakeBinanceWallet).")
            return False

        if ticker in self.balances:
            self.balances[ticker] += (1 - self.binanceFee) * amount
        else:
            self.balances[ticker] = (1 - self.binanceFee) * amount

        self.baseCurrencyAmount -= amount
        return True


    def sell(self, ticker: str, amount: float, test=True) -> bool:
        """
        Sells a cryptocurrency.
        :param ticker: what to sell
        :param amount: the amount to sell
        :return: success of the transaction
        """
        if ticker in self.balances:
            self.balances[ticker] -= amount
        else:
            print("Tried to sell " + ticker + " but not enough is owned (FakeBinanceWallet).")
            return False

        self.baseCurrencyAmount += (1 - self.binanceFee) * amount
        return True

    def getBalance(self, ticker="BTC") -> float:
        """
        Returns amount owned of stock/cryptocurrency.
        :param ticker: the asset
        :return: amount owned
        """
        if ticker == self.baseCurrencyName:
            return self.baseCurrencyAmount
        else:
            if ticker in self.balances:
                return self.balances[ticker]
            else:
                print("Tried to get balance of " + ticker + ", which is not owned (FakeBinanceWallet).")
                return 0.0
