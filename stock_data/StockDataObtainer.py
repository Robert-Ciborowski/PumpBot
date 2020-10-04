# Name: Stock Data Obtainer
# Author: Robert Ciborowski
# Date: 13/04/2020
# Description: Keeps track of stock prices to the minute.

# from __future__ import annotations
from datetime import datetime
from typing import Dict, List
import pandas as pd
import yfinance as yf

class StockDataObtainer:
    """
    Optional to implement. Lets the obtainer know that the following stocks
    will be requested by use of obtainPrices and obtainPrice.
    """
    def trackStocks(self, tickers: List[str]):
        pass

    def stopTrackingStocks(self, tickers: List[str]):
        pass

    """
    Returns the stock price, or -1 if the price has not changed today.
    """
    def obtainPrice(self, ticker: str) -> float:
        return 0

    """
    Returns the stock volume, or -1 if the price has not changed today.
    """

    def obtainVolume(self, ticker: str) -> float:
        return 0

    """
    - data: in the form {"Ticker": []}
    - numberOfPrices: the number of most recent prices to obtain, where each
                      price is from a different minute. For example, if this
                      value is 3, then this function could return
                      [1.0, 1.05, 1.25], where 1.25 is the most recent price,
                      and 1.05 was the price from one minute ago.
                      
    """
    def obtainPrices(self, ticker: str, numberOfPrices=-1) -> List[float]:
        return []

    def obtainPricesAndVolumes(self, ticker: str, numberOfPrices=-1):
        return []

    def obtainMinutePricesAndVolumes(self, ticker: str, numberOfPrices=-1):
        return []

    def getCurrentDate(self) -> datetime:
        pass

    """
    Useful helper method for getting just the most recent price from a
    yahoo finance pandas dataframe.
    """
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

    """
    If a minute is missing in a series, this fills them in.
    """
    # def _fixSeriesDates(self, series: pd.Series) -> pd.Series:
    #     keys = series.keys()
    #
    #     if len(keys) == 0:
    #         return series
    #
    #     prev = keys[0]
    #     for i in range(1, len(keys)):
    #         curr = keys[i]
    #         diff = curr - prev
    #         minutes_diff = int(diff.total_seconds() / 60)
    #
    #         if minutes_diff > 1:
    #             price_diff = series[curr] - series[prev]
    #             slope = price_diff / minutes_diff
    #
    #             for j in range(minutes_diff):
    #
    #         if keys[i].to_pydatetime() > time:
    #             lastIndex = i
    #             break
    #
    #         prev = curr
