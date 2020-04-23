# Name: Stock Filter
# Author: Robert Ciborowski
# Date: 18/04/2020
# Description: Filters out stocks.

# from __future__ import annotations

from typing import Dict

from listing_obtainers import ListingObtainer
from stock_data import StockDataObtainer
import pandas as pd
from datetime import datetime

class StockFilter:
    data: Dict
    filtered_stocks: pd.DataFrame
    dataObtainer: StockDataObtainer
    timestampOfDownload: datetime

    def __init__(self, dataObtainer: StockDataObtainer):
        self.timestampOfDownload = None
        self.data = {
            "Ticker": [],
            "Price": []
        }
        self.dataObtainer = dataObtainer

    def addListings(self, obtainer: ListingObtainer):
        dataframe = obtainer.obtain()

        for index, row in dataframe.iterrows():
            self.data["Ticker"].append(row["Ticker"])
            self.data["Price"].append(0)

        self.dataObtainer.trackStocks(self.data["Ticker"])
        self.timestampOfDownload = datetime.now()
        return self

    def getDataForFiltering(self):
        return self

    def filter(self):
        return self
