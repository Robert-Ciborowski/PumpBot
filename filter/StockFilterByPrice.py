# Name: Stock filter by price
# Author: Robert Ciborowski
# Date: 26/03/2020
# Description: Filters out stocks.

# from __future__ import annotations

from typing import Dict
from datetime import datetime
import pandas as pd

from filter.StockFilter import StockFilter
from stock_data import StockDataObtainer

class StockFilterByPrice(StockFilter):
    priceThreshold: int
    template: Dict
    data: Dict
    filtered_stocks: pd.DataFrame
    dayThreshold: int
    timestampOfDownload: datetime
    dataObtainer: StockDataObtainer

    def __init__(self, priceThreshold: int, dataObtainer: StockDataObtainer, dayThreshold=5):
        super().__init__(dataObtainer)
        self.priceThreshold = priceThreshold
        self.dayThreshold = dayThreshold

    """
    Changes the day threshold (default is 5), which stores how long ago the stock
    must have had a price update/change for it to be used.
    """
    def changeDayThreshold(self, dayThreshold: int):
        self.dayThreshold = dayThreshold
        return self

    def getDataForFiltering(self):
        self.timestampOfDownload = datetime.now()
        data2 = {"Ticker": [], "Price": [], "Volume": []}

        for ticker in self.data["Ticker"]:
            lst, lst2 = self.dataObtainer.obtainPricesAndVolumes(ticker, 1)

            if len(lst) != 0:
                data2["Ticker"].append(ticker)
                data2["Price"].append(lst[0])
                data2["Volume"].append(lst2[0])

        self.data = data2
        return self


    """
    Filters out stocks above a threshold price.
    Preconditions: coloumn "Ticker" of df contains stock tickers as strings,
                   coloumn "Price" of df contains prices
    """
    def filter(self):
        dictionary = {
            "Ticker": [],
            "Price": [],
            "Volume": []
        }

        toRemove = []

        for i in range(len(self.data["Ticker"])):
            if self.data["Price"][i] <= self.priceThreshold:
                dictionary["Ticker"].append(self.data["Ticker"][i])
                dictionary["Price"].append(self.data["Price"][i])
                dictionary["Volume"].append(self.data["Volume"][i])
            else:
                toRemove.append(self.data["Ticker"][i])

        self.filtered_stocks = pd.DataFrame(dictionary,
                                            columns=["Ticker", "Price", "Volume"])
        self.dataObtainer.stopTrackingStocks(toRemove)
        return self
