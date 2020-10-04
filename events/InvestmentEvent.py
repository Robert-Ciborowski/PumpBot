# Name: Investment Event
# Author: Robert Ciborowski
# Date: 04/10/2020
# Description: A class which represents the event in which an investment
#              occurred.

# from __future__ import annotations
from typing import Dict

from events.Event import Event


class InvestmentEvent(Event):
    def __init__(self, ticker: str, price: float, confidence: float, amount: float):
        super().__init__("Investment")
        self.data["Ticker"] = ticker
        self.data["Price"] = price
        self.data["Confidence"] = confidence
        self.data["Amount"] = amount
