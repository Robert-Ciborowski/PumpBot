"""
A simple wallet for testing.
"""
import json
from typing import Dict

from wallet.Wallet import Wallet

class SimpleWallet(Wallet):
    baseCurrencyAmount: float
    baseCurrencyName: str
    balances: Dict

    def __init__(self, baseCurrencyAmount=0.0):
        self.baseCurrencyAmount = baseCurrencyAmount
        self.baseCurrencyName = "BTC"
        self.balances = {}

    def purchase(self, ticker: str, amount: float, test=True) -> float:
        """
        Purchases a cryptocurrency.
        :param ticker: what to purchase
        :param amount: the amount to purchase
        :param test: whether this is a test order or a real one
        :return: success of the transaction
        """
        if self.baseCurrencyAmount <= amount:
            print("Tried to purchase " + ticker + " with more funds than available (SimpleWallet).")
            return False

        if ticker in self.balances:
            self.balances[ticker] += amount
        else:
            self.balances[ticker] = amount

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
            print("Tried to sell " + ticker + " but not enough is owned (SimpleWallet).")
            return False

        self.baseCurrencyAmount += amount
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
                print("Tried to get balance of " + ticker + ", which is not owned (SimpleWallet).")
                return 0.0
