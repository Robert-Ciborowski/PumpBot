# Name: Pump and Dump Event
# Author: Robert Ciborowski
# Date: 14/04/2020
# Description: A class which represents the event in which a pump and dump
#              occurred.

# from __future__ import annotations
from typing import Dict

from events.Event import Event


class PumpAndDumpEvent(Event):
    def __init__(self, ticker: str, price: float):
        super().__init__("PumpAndDump")
        self.data["Ticker"] = ticker
        self.data["Price"] = price
