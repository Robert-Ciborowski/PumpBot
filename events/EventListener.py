# Name: Event
# Author: Robert Ciborowski
# Date: 14/04/2020
# Description: A super class which reacts when an event occurs.

from __future__ import annotations
from typing import Dict

from events import Event

class EventListener:
    def onEvent(self, event: Event):
        pass
