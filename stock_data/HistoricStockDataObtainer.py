# Name: Historic Stock Data Obtainer
# Author: Robert Ciborowski
# Date: 13/04/2020
# Description: Keeps track of stock prices to the minute.

from __future__ import annotations

from typing import Dict
import pandas as pd
import yfinance as yf

from stock_data.StockDataObtainer import StockDataObtainer


class CurrentStockDataObtainer(StockDataObtainer):
    def obtainPrice(self, ticker: str) -> float:
        df = yf.download(tickers=ticker,
                         period=str(self.dayThreshold) + "d", interval="1m",
                         threads=False)
