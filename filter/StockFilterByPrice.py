# Name: Stock filter by price
# Author: Robert Ciborowski
# Date: 26/03/2020
# Description: Filters out stocks.

from __future__ import annotations

from typing import Dict
from datetime import datetime
import pandas as pd
import yfinance as yf


from listing_obtainers import ListingObtainer

class StockFilterByPrice:
    priceThreshold: int
    template: Dict
    filtered_stocks: pd.DataFrame
    dayThreshold: int
    timestampOfDownload: datetime

    def __init__(self, priceThreshold: int, dayThreshold=5):
        self.priceThreshold = priceThreshold
        self.data = {
            "Ticker": [],
            "Price": []
        }
        self.dayThreshold = dayThreshold

    """
    Changes the day threshold (default is 5), which stores how long ago the stock
    must have had a price update/change for it to be used.
    """
    def changeDayThreshold(self, dayThreshold: int) -> StockFilterByPrice:
        self.dayThreshold = dayThreshold
        return self

    def addListings(self, obtainer: ListingObtainer) -> StockFilterByPrice:
        dataframe = obtainer.obtain()

        for index, row in dataframe.iterrows():
            self.data["Ticker"].append(row["Ticker"])
            self.data["Price"].append(0)

        return self

    def getPricesForListings(self) -> StockFilterByPrice:
        to_download = ""

        for i in range(len(self.data["Ticker"])):
            to_download += self.data["Ticker"][i] + " "

        self.timestampOfDownload = datetime.now()
        df = yf.download(tickers=to_download, period=str(self.dayThreshold) + "d", interval="1m", threads=False)
        df = df.iloc[:, 0:len(self.data["Ticker"])]
        self.data = self._extractMostRecentPrices(df)
        return self


    """
    Filters out stocks above a threshold price.
    Preconditions: coloumn "Ticker" of df contains stock tickers as strings,
                   coloumn "Price" of df contains prices
    """
    def filterStocks(self) -> StockFilterByPrice:
        dictionary = {
            "Ticker": [],
            "Price": []
        }

        for i in range(len(self.data["Ticker"])):
            if self.data["Price"][i] <= self.priceThreshold:
                dictionary["Ticker"].append(self.data["Ticker"][i])
                dictionary["Price"].append(self.data["Price"][i])

        self.filtered_stocks = pd.DataFrame(dictionary,
                                            columns=["Ticker", "Price"])

        return self

    def _extractMostRecentPrices(self, data: pd.DataFrame) -> Dict:
        dataDict = {
            "Ticker": [],
            "Price": []
        }

        for i in range(0, len(data.columns)):
            s = data.iloc[:, i]
            val_index = s.last_valid_index()

            if val_index is not None:
                val = s[val_index]

                if val is not None:
                    dataDict["Price"].append(val)
                    dataDict["Ticker"].append(data.columns[i][1])

        return dataDict
