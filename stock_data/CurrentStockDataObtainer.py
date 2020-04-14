# Name: Current Stock Data Obtainer
# Author: Robert Ciborowski
# Date: 13/04/2020
# Description: Obtains the updated stock prices.

from __future__ import annotations

from typing import Dict
from datetime import datetime
import pandas as pd
import yfinance as yf

from stock_data.StockDataObtainer import StockDataObtainer

class CurrentStockDataObtainer(StockDataObtainer):
    def obtainPrice(self, ticker: str) -> float:
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d")
        date_str = str(date_time)
        df = yf.download(tickers=ticker,
                         start=date_str, end=date_str,
                         threads=False)
        return self._get_most_recent(df)

    def _get_most_recent(self, data: pd.DataFrame) -> float:
        if data is None or len(data.columns) == 0:
            return -1

        s = data.iloc[:, 0]
        val_index = s.last_valid_index()

        print("-------------------------- (Current Stock Data Obtainer)")
        print(val_index)

        if val_index is not None:
            val = s[val_index]

            if val is not None:
                return val

        return -1


