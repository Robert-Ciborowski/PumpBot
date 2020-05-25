# Name: Historic Stock Data Obtainer
# Author: Robert Ciborowski
# Date: 13/04/2020
# Description: Keeps track of stock prices to the minute.

# from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import pandas as pd
import pytz
import yfinance as yf

from stock_data.StockDataObtainer import StockDataObtainer


class HistoricStockDataObtainer(StockDataObtainer):
    dateOfStart: datetime
    endOfMarket: Tuple
    timezone: str

    _startTime: datetime
    _downloadedData: Dict[str, pd.Series]
    _downloaded: bool

    def __init__(self, dateOfStart: datetime, timezone="America/Toronto"):
        self.dateOfStart = dateOfStart
        self._startTime = datetime.now()
        self.endOfMarket = (4, 0)
        self._downloadedData = {}
        self.timezone = timezone
        self._downloaded = False

    def trackStocks(self, tickers: List[str]):
        if self._downloaded:
            return

        for ticker in tickers:
            self._predownloadData(ticker)

        self._downloaded = True

    def stopTrackingStocks(self, tickers: List[str]):
        if not self._downloaded:
            return

        for ticker in tickers:
            self._downloadedData.pop(ticker)

    def _predownloadData(self, ticker: str):
        start_date_str = str(self.dateOfStart.strftime("%Y-%m-%d"))
        end_date_str = str((self.dateOfStart + timedelta(days=1)).strftime("%Y-%m-%d"))
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date_str, end=end_date_str, interval="1m")

        # For some reason, the current price is being added at the end, so we
        # need to get rid of it.
        df.drop(df.tail(1).index, inplace=True)
        print(ticker + "================================================")
        print(df["Open"])
        self._downloadedData[ticker] = df["Open"]

    def obtainPrice(self, ticker: str) -> float:
        now = datetime.now()
        diff = now - self._startTime
        date = self.dateOfStart + diff
        start_date_to_use = datetime(date.year, date.month, date.day, hour=date.hour, minute=date.minute)
        timezone = pytz.timezone(self.timezone)
        d_aware = timezone.localize(start_date_to_use)
        price = self._getPriceFromSeries(self._downloadedData[ticker], d_aware)
        return price

    """
    - data: in the form {"Ticker": []}
    """

    def obtainPrices(self, ticker: str, numberOfPrices=-1) -> List[float]:
        now = datetime.now()
        diff = now - self._startTime
        date = self.dateOfStart + diff
        start_date_to_use = datetime(date.year, date.month, date.day,
                                     hour=date.hour, minute=date.minute)
        timezone = pytz.timezone(self.timezone)
        d_aware = timezone.localize(start_date_to_use)

        print("Obtaining prices for: " + ticker + " with date: " + str(start_date_to_use))
        return self._getPricesFromSeries(self._downloadedData[ticker], d_aware,
                                         numberOfPrices)

    def _getPriceFromSeries(self, series: pd.Series, time: datetime) -> float:
        keys = series.keys()
        lastKey = keys[0]

        for key in keys:
            if key.to_pydatetime() > time:
                break
            lastKey = key

        return series[lastKey]

    def _getPricesFromSeries(self, series: pd.Series, time: datetime, pricesToObtain=-1) -> List[float]:
        keys = series.keys()

        if len(keys) == 0:
            return []

        lastIndex = 0

        for i in range(len(keys)):
            if keys[i].to_pydatetime() > time:
                lastIndex = i
                break

        if pricesToObtain < 0 or pricesToObtain >= lastIndex:
            return series[:lastIndex]
        else:
            return series[lastIndex-pricesToObtain:lastIndex]



