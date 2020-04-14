# Name: Event
# Author: Robert Ciborowski
# Date: 14/04/2020
# Description: A class which is outputted to event listeners when an event
#              occurs.

from __future__ import annotations
from typing import Dict

class Event:
    data: Dict

    def __init__(self):
        self.data = {}

    def addData(self, dataName: str, data) -> Event:
        self.data[dataName] = data
        return self

