# Name: Stock Data Obtainer
# Author: Robert Ciborowski
# Date: 13/04/2020
# Description: Keeps track of stock prices to the minute.

from __future__ import annotations

from typing import Dict
import pandas as pd
import yfinance as yf

class StockDataObtainer:
    """
    Returns the stock price, or -1 if the price has not changed today.
    """
    def obtainPrice(self, ticker: str) -> float:
        return 0

