# Name: RSI Pump and Dump Detector
# Author: Robert Ciborowski
# Date: 26/12/2020
# Description: Detects pump and dumps from Binance crypto data.

# from __future__ import annotations
import os
from datetime import datetime
from typing import Dict, List
import random
import numpy as np
import pandas as pd
import tensorflow as tf
from stock_pandas import StockDataFrame

from models.PumpAndDumpDetector import PumpAndDumpDetector
from util.Constants import SAMPLES_OF_DATA_TO_LOOK_AT


class RSIPumpAndDumpDetector(PumpAndDumpDetector):
    rsiForBuy: float
    rsiPeriod: int

    def __init__(self, rsiForBuy: float, rsiPeriod: int):
        super().__init__()
        self.rsiForBuy = rsiForBuy
        self.rsiPeriod = rsiPeriod

    """
    Precondition: prices is a pandas dataframe or series.
    """
    def detect(self, prices, volumes) -> float:
        length = len(prices)

        if length < self.rsiPeriod or length < SAMPLES_OF_DATA_TO_LOOK_AT:
            return 0.0

        df = StockDataFrame(pd.DataFrame(prices[0::60], columns=["close"]))
        rsi = df.exec("rsi:" + str(self.rsiPeriod))

        if rsi[-1] <= self.rsiForBuy:
            return 1.0

        return 0.0
