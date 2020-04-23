# Name: Pass Through Stock Filter
# Author: Robert Ciborowski
# Date: 18/04/2020
# Description: Does not filter out any stocks.

# from __future__ import annotations

from typing import Dict

from filter.StockFilter import StockFilter
from stock_data import StockDataObtainer
import pandas as pd

class PassThroughStockFilter(StockFilter):
    data: Dict
    filtered_stocks: pd.DataFrame
    dataObtainer: StockDataObtainer

    def __init__(self, dataObtainer: StockDataObtainer):
        super().__init__(dataObtainer)

    def getDataForFiltering(self):
        return self

    def filter(self):
        self.filtered_stocks = pd.DataFrame(self.data,
                                            columns=["Ticker", "Price"])
        return self
