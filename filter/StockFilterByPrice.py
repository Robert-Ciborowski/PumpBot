# Name: Stock filter by price
# Author: Robert Ciborowski
# Date: 26/03/2020
# Description: Filters out stocks.

from __future__ import annotations

from typing import Dict
import pandas as pd
import yfinance as yf

from listing_obtainers import ListingObtainer

class StockFilterByPrice:
    priceThreshold: int
    template: Dict
    filtered_stocks: pd.DataFrame
    dayThreshold: int

    def __init__(self, priceThreshold: int):
        self.priceThreshold = priceThreshold
        self.data = {
            "Ticker": [],
            "Price": []
        }
        self.dayThreshold = 5

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

        print(to_download)

        df = yf.download(tickers=to_download, period=str(self.dayThreshold) + "d", interval="1m", threads=False)
        df = df.iloc[:, 0:len(self.data["Ticker"])]

        self.data = self._extractMostRecentPrices(df)

        print("df: -----------------------------------------")
        print(df)
        print(df.info())

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

        self.filtered_stocks = pd.DataFrame(dictionary, columns=["Ticker", "Price"])

        for i in range(len(self.data["Ticker"])):
            if self.data["Price"][i] <= self.priceThreshold:
                df = pd.DataFrame([[self.data["Ticker"][i], self.data["Price"][i]]], columns=["Ticker", "Price"])
                self.filtered_stocks = self.filtered_stocks.append(df, ignore_index=True)

        return self

    def _extractMostRecentPrices(self, data: pd.DataFrame) -> Dict:
        dataDict = {
            "Ticker": [],
            "Price": []
        }

        for i in range(0, len(data.columns)):
            s = data.iloc[:, i]
            val_index = s.last_valid_index()

            print("--------------------------")
            print(val_index)

            if val_index is not None:
                val = s[val_index]
                print(val)

                if val is not None:
                    dataDict["Price"].append(val)
                    dataDict["Ticker"].append(data.columns[i][1])

        return dataDict
