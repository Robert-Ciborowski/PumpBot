# Name: Historic Binance Crypto Data Obtainer
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


    def obtainPrice(self, ticker: str) -> float:
        return 0.0

    """
    - data: in the form {"Ticker": []}
    """

    def obtainPrices(self, ticker: str, numberOfPrices=-1) -> List[float]:
        return []


