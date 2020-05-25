# Name: Current Binance Data Obtainer
# Author: Robert Ciborowski
# Date: 18/04/2020
# Description: Obtains the updated Binance crypto prices.

# from __future__ import annotations

from typing import Dict, List
import json

import binance
from binance.client import Client

from stock_data.StockDataObtainer import StockDataObtainer

class CurrentBinanceDataObtainer(StockDataObtainer):
    _client: Client
    _recentTradesLimit: int

    def __init__(self, propertiesFile="binance_properties.json"):
        super().__init__()
        api_key, api_secret = self._getKeysFromFile(propertiesFile)
        self._client = Client(api_key=api_key, api_secret=api_secret)
        self._recentTradesLimit = 10

    def obtainPrice(self, ticker: str) -> float:
        # COULD ALSO USE client.get_avg_price, but that uses a 5 minute interval.
        # We want a tighter interval, preferably 1 minute.
        try:
            trades = self._client.get_recent_trades(symbol=ticker, limit=self._recentTradesLimit)
        except binance.exceptions.BinanceAPIException:
            return -1

        if len(trades) == 0:
            return -1

        priceTotal = 0.0
        numberOfTrades = 0

        for trade in trades:
            priceTotal += float(trade["price"])
            numberOfTrades += 1

        return priceTotal / numberOfTrades

    def obtainPrices(self, ticker: str, numberOfPrices=1) -> List[float]:
        if numberOfPrices == -1:
            numberOfPrices = 1

        trades = self._client.get_recent_trades(symbol=ticker,
                                                limit=self._recentTradesLimit * numberOfPrices)

        if len(trades) == 0:
            return []

        prices = []
        priceTotal = 0.0
        numberOfTrades = 0

        for trade in trades:
            priceTotal += float(trade["price"])
            numberOfTrades += 1

            if numberOfTrades == self._recentTradesLimit:
                prices.insert(0, priceTotal / numberOfTrades)
                priceTotal = 0
                numberOfTrades = 0

        return prices

    def obtainPricesAndVolumes(self, ticker: str, numberOfPrices=1):
        if numberOfPrices < 1:
            numberOfPrices = 1

        trades = self._client.get_recent_trades(symbol=ticker,
                                                limit=self._recentTradesLimit * numberOfPrices)

        if len(trades) == 0:
            return []

        prices = []
        volumes = []
        priceTotal = 0.0
        volumeTotal = 0.0
        numberOfTrades = 0

        for trade in trades:
            priceTotal += float(trade["price"])
            volumeTotal += float(trade["qty"])
            numberOfTrades += 1

            if numberOfTrades == self._recentTradesLimit:
                prices.insert(0, priceTotal / numberOfTrades)
                volumes.insert(0, volumeTotal / numberOfTrades)
                priceTotal = 0
                volumeTotal = 0
                numberOfTrades = 0

        return prices, volumes

    def _getKeysFromFile(self, propertiesFile: str):
        try:
            with open(propertiesFile, mode='r') as file:
                data = json.load(file)
                apiKey = data["API Key"]
                apiKeySecret = data["API Key Secret"]
                return apiKey, apiKeySecret
        except:
            print(
                "You are missing " + propertiesFile + ". Please ask Robert" \
                                                      "(robert.ciborowski"
                                                      "@mail.utoronto.ca) for "
                                                      "help.")


