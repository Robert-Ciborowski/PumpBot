# Name: Event Dispatcher
# Author: Robert Ciborowski
# Date: 14/04/2020
# Description: A class which dispatches events. This is a singleton.

# from __future__ import annotations
from typing import Dict

from events import EventListener, Event

"""
This class is a singleton! You get the instance in EventDispatcher.getInstance()

Representation invariants:
- _listeners: a Dict of Lists, and each lists contains an EventListener
              (nu duplicates)
"""
class EventDispatcher:
    _instance = None
    _listeners: Dict

    def __init__(self):
        if not EventDispatcher._instance:
            EventDispatcher._instance = self
        else:
            print("Only one instance of EventDispatcher is allowed!")

        self._listeners = {}

    @staticmethod
    def getInstance():
        if not EventDispatcher._instance:
            return EventDispatcher()
        else:
            return EventDispatcher._instance

    def addListener(self, listener: EventListener, eventType: str):
        if eventType in self._listeners:
            if listener in self._listeners[eventType]:
                return
            else:
                self._listeners[eventType].append(listener)
        else:
            self._listeners[eventType] = [listener]

    def dispatchEvent(self, event: Event):
        if event.type not in self._listeners:
            return

        for listener in self._listeners[event.type]:
            listener.onEvent(event)
