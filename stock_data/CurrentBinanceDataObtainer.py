# Name: Current Binance Data Obtainer
# Author: Robert Ciborowski
# Date: 18/04/2020
# Description: Obtains the updated Binance crypto prices. Can only get data up
#              to the minute.

# from __future__ import annotations
import math
from datetime import datetime, timedelta
from typing import Dict, List
import json
import pandas as pd
import numpy as np
import requests
from dateutil import parser

import binance
import pytz
from binance.client import Client
from binance.exceptions import BinanceAPIException

from stock_data.StockDataObtainer import StockDataObtainer
from util.Constants import BINANCE_DATA_FETCH_ATTEMPT_AMOUNT, \
    SAMPLES_OF_DATA_TO_LOOK_AT


class CurrentBinanceDataObtainer(StockDataObtainer):
    maxPricesToTrack: int
    secondsBetweenUpdates: int

    _client: Client
    _recentTradesLimit: int
    _timezone: pytz.timezone
    _recentPrices: Dict[str, List[float]]
    _recentVolumes: Dict[str, List[float]]
    _lastUpdateTime: datetime
    _epoch: datetime
    _incomingDataLimit: int
    _tryAmount: int

    def __init__(self, maxPricesToTrack: int, secondsBetweenUpdates: int, propertiesFile="binance_properties.json"):
        super().__init__()
        self.maxPricesToTrack = maxPricesToTrack
        self.secondsBetweenUpdates = secondsBetweenUpdates
        api_key, api_secret = self._getKeysFromFile(propertiesFile)
        self._client = Client(api_key=api_key, api_secret=api_secret)
        self._recentTradesLimit = 10
        self._timezone = pytz.timezone("Etc/GMT-0")
        self._epoch = datetime.utcfromtimestamp(0)
        self._lastUpdateTime = self._epoch
        self._incomingDataLimit = 3
        self._recentPrices = {}
        self._recentVolumes = {}
        self._tryAmount = BINANCE_DATA_FETCH_ATTEMPT_AMOUNT

    def trackStocks(self, tickers: List[str]):
        for ticker in tickers:
            self._recentPrices[ticker] = []
            self._recentVolumes[ticker] = []

    def stopTrackingStocks(self, tickers: List[str]):
        for ticker in tickers:
            self._recentPrices.pop(ticker)
            self._recentVolumes.pop(ticker)

    def obtainPrice(self, ticker: str) -> float:
        self._update(ticker)
        return self._recentPrices[ticker][-1]

        # COULD ALSO USE client.get_avg_price, but that uses a 5 minute interval.
        # We want a tighter interval, preferably 1 minute.
        # try:
        #     trades = self._client.get_recent_trades(symbol=ticker, limit=self._recentTradesLimit)
        # except binance.exceptions.BinanceAPIException:
        #     return -1
        #
        # if len(trades) == 0:
        #     return -1
        #
        # priceTotal = 0.0
        # numberOfTrades = 0
        #
        # for trade in trades:
        #     priceTotal += float(trade["price"])
        #     numberOfTrades += 1
        #
        # return priceTotal / numberOfTrades

    def obtainVolume(self, ticker: str) -> float:
        self._update(ticker)
        return self._recentVolumes[ticker][-1]

        # COULD ALSO USE client.get_avg_price, but that uses a 5 minute interval.
        # We want a tighter interval, preferably 1 minute.
        # try:
        #     trades = self._client.get_recent_trades(symbol=ticker, limit=self._recentTradesLimit)
        # except binance.exceptions.BinanceAPIException:
        #     return -1
        #
        # if len(trades) == 0:
        #     return -1
        #
        # priceTotal = 0.0
        # numberOfTrades = 0
        #
        # for trade in trades:
        #     priceTotal += float(trade["qty"])
        #     numberOfTrades += 1
        #
        # return priceTotal / numberOfTrades

    def obtainPrices(self, ticker: str, numberOfPrices=1) -> List[float]:
        self._update(ticker)

        if numberOfPrices > self.maxPricesToTrack:
            numberOfPrices = self.maxPricesToTrack

        return self._recentPrices[ticker][:-numberOfPrices]

        # if numberOfPrices == -1:
        #     numberOfPrices = 1
        #
        # trades = self._client.get_recent_trades(symbol=ticker,
        #                                         limit=self._recentTradesLimit * numberOfPrices)
        #
        # if len(trades) == 0:
        #     return []
        #
        # prices = []
        # priceTotal = 0.0
        # numberOfTrades = 0
        #
        # for trade in trades:
        #     priceTotal += float(trade["price"])
        #     numberOfTrades += 1
        #
        #     if numberOfTrades == self._recentTradesLimit:
        #         prices.insert(0, priceTotal / numberOfTrades)
        #         priceTotal = 0
        #         numberOfTrades = 0
        #
        # return prices

    def obtainPricesAndVolumes(self, ticker: str, numberOfPrices=1):
        self._update(ticker)

        if numberOfPrices > self.maxPricesToTrack:
            numberOfPrices = self.maxPricesToTrack

        return self._recentPrices[ticker][:-numberOfPrices], self._recentVolumes[ticker][:-numberOfPrices]

        # if numberOfPrices < 1:
        #     numberOfPrices = 1
        #
        # trades = self._client.get_recent_trades(symbol=ticker,
        #                                         limit=self._recentTradesLimit * numberOfPrices)
        #
        # if len(trades) == 0:
        #     return []
        #
        # prices = []
        # volumes = []
        # priceTotal = 0.0
        # volumeTotal = 0.0
        # numberOfTrades = 0
        #
        # for trade in trades:
        #     priceTotal += float(trade["price"])
        #     volumeTotal += float(trade["qty"])
        #     numberOfTrades += 1
        #
        #     if numberOfTrades == self._recentTradesLimit:
        #         prices.insert(0, priceTotal / numberOfTrades)
        #         volumes.insert(0, volumeTotal / numberOfTrades)
        #         priceTotal = 0
        #         volumeTotal = 0
        #         numberOfTrades = 0
        #
        # print("Obtained price and volume data of " + ticker + " at " + str(
        #     datetime.now()) + ".")
        # return prices, volumes

    def obtainMinutePricesAndVolumes(self, ticker: str, numberOfPrices=SAMPLES_OF_DATA_TO_LOOK_AT):
        # return self.obtainPricesAndVolumes(ticker, numberOfPrices)
        for i in range(self._tryAmount):
            try:
                now = datetime.now()
                now = datetime(now.year, now.month, now.day, now.hour, now.minute)
                df = self._get_all_binance(ticker, now, SAMPLES_OF_DATA_TO_LOOK_AT)
                return df["close"].to_numpy(), df["volume"].to_numpy()
            except binance.exceptions.BinanceAPIException as e:
                print(
                    "obtainMinutePricesAndVolumes failed to work for " + ticker + "! BinanceAPIException. Trying " + str(
                        self._tryAmount - 1 - i) + " more times.")
                print(e)
            except requests.exceptions.ReadTimeout as e:
                print(
                    "obtainMinutePricesAndVolumes failed to work for " + ticker + "! ReadTimeout. Trying " + str(
                        self._tryAmount - 1 - i) + " more times.")
                print(e)
            except:
                print(
                    "obtainMinutePricesAndVolumes failed to work for " + ticker + "! Unknown. Trying " + str(
                        self._tryAmount - 1 - i) + " more times.")

        return np.asarray([0.0 for i in range(numberOfPrices)])


    def getCurrentDate(self) -> datetime:
        now = datetime.now()
        now = self._timezone.localize(now)
        return now

    def _update(self, ticker: str):
        now = datetime.now()
        numberOfValuesToAppend = int((now - self._lastUpdateTime).total_seconds() // self.secondsBetweenUpdates)

        if numberOfValuesToAppend == 0:
            return

        numberOfValuesToAppend = min(numberOfValuesToAppend, self.maxPricesToTrack)

        try:
            trades = self._client.get_recent_trades(symbol=ticker,
                                                 # startTime=int(startTime),
                                                 # endTime=int(endTime),
                                                 limit=self._incomingDataLimit)
        except binance.exceptions.BinanceAPIException as e:
            print("CurrentBinanceDataObtainer _update failed! BinanceAPIException")
            print(e)
            return
        except requests.exceptions.ReadTimeout as e:
            print("CurrentBinanceDataObtainer _update failed! requests.exceptions.ReadTimeout")
            print(e)
            return
        except:
            print("CurrentBinanceDataObtainer _update failed! Unknown error")
            return

        price = 0.0
        volume = 0.0

        for trade in trades:
            p = float(trade['price'])
            q = float(trade['qty'])
            price += p
            volume += q

        if len(trades) != 0:
            price /= len(trades)
            volume /= len(trades)
        elif len(self._recentPrices[ticker]) != 0:
            price = self._recentPrices[ticker][-1]
            volume = self._recentVolumes[ticker][-1]

        print("Price of " + ticker + " at " + str(now) + " is " + str(
            price) + ", volume is " + str(volume) + ".")

        for i in range(numberOfValuesToAppend):
            self._recentPrices[ticker].append(price)
            self._recentVolumes[ticker].append(volume)

        while len(self._recentPrices[ticker]) > self.maxPricesToTrack:
            self._recentPrices[ticker].pop(0)
            self._recentVolumes[ticker].pop(0)

        self._lastUpdateTime = now

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

    def _get_all_binance(self, symbol, newest_point, numberOfMinutes):
        kline_size = "1m"
        # newest_point = self._minutes_of_new_data(symbol, kline_size)
        oldest_point = newest_point - timedelta(minutes=numberOfMinutes)

        klines = self._client.get_historical_klines(symbol, kline_size,
                                                      oldest_point.strftime(
                                                          "%d %b %Y %H:%M:%S"),
                                                      newest_point.strftime(
                                                          "%d %b %Y %H:%M:%S"))
        klines2 = []

        for i in klines:
            klines2.append([float(i[4]), float(i[5])])

        # Depending on the computer, we might get one too many results?!?!
        # This fixes that.
        while len(klines2) > numberOfMinutes:
            klines2.pop(0)

        data = pd.DataFrame(klines2, columns=['close', 'volume'])
        return data
