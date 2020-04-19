# Name: Current Stock Data Obtainer
# Author: Robert Ciborowski
# Date: 13/04/2020
# Description: Obtains the updated stock prices.
#              Note: I was experimenting with the Google Finance API but it
#              hasn't been maintained in a long time and gets HTTP 403 errors :(

# from __future__ import annotations

from typing import Dict, List
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
import json


from stock_data.StockDataObtainer import StockDataObtainer

class CurrentStockDataObtainer(StockDataObtainer):
    def obtainPrice(self, ticker: str) -> float:
        lst = self.obtainPrices(ticker, 1)

        if len(lst) == 0:
            return -1

        return lst[-1]

    """
    - data: in the form {"Ticker": []}
    """
    def obtainPrices(self, ticker: str, numberOfPrices=-1) -> List[float]:
        start_date_str = str(datetime.now().strftime("%Y-%m-%d"))
        end_date_str = str(
            (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"))
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date_str, end=end_date_str,
                           interval="1m")
        prices = df["Open"].tolist()

        if numberOfPrices > len(prices) or numberOfPrices < 0:
            return prices

        return prices[len(prices) - numberOfPrices:len(prices)]


        # to_download = ""
        #
        # for i in range(len(data["Ticker"])):
        #     to_download += data["Ticker"][i] + " "
        #
        # self.timestampOfDownload = datetime.now()
        # df = yf.download(tickers=to_download,
        #                  period=str(dayThreshold) + "d", interval="1m",
        #                  threads=False)
        # df = df.iloc[:, 0:len(data["Ticker"])]
        # data = self._extractMostRecentPrices(df)
        # return data

    def _get_most_recent(self, data: pd.DataFrame) -> float:
        if data is None or len(data.columns) == 0:
            return -1

        s = data.iloc[:, 0]
        val_index = s.last_valid_index()

        if val_index is not None:
            val = s[val_index]

            if val is not None:
                return val

        return -1

    # def _obtainPriceYahooFinance(self, ticker: str) -> float:
    #     return self.obtainPrices
    #
    #
    #     now = datetime.now()
    #     date_str = str(now.strftime("%Y-%m-%d"))
    #     date_str_2 = str((now + timedelta(days=1)).strftime("%Y-%m-%d"))
    #     df = yf.download(tickers=ticker,
    #                      start=date_str, end=date_str_2)
    #     price = self._get_most_recent(df)
    #     print("PRICE ------")
    #     print(price)
    #     return price

    # def _obtainPriceGoogleFinance(self, ticker: str) -> float:
    #     now = datetime.now()
    #     date_time = now.strftime("%Y-%m-%d")
    #     date_str = str(date_time)
    #     df = getQuotes('AAPL')
    #     print("AAPL!!!!!!")
    #     print(df)
    #     return 0



