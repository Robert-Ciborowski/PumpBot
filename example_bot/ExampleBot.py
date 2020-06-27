# Name: Example Bot
# Author: Robert Ciborowski
# Date: 14/04/2020
# Description: An example of a bot which can react to stock market pump and
#              dumps. This bot simply outputs the pump and dump info into the
#              console.

# from __future__ import annotations

from events import Event
from events.EventListener import EventListener

class ExampleBot(EventListener):
    def onEvent(self, event: Event):
        if event.type == "PumpAndDump":
            # or you can do if isinstance(event, PumpAndDumpEvent)
            print("Pump and Dump is occurring! " + event._dataAsDataFrames["Ticker"] + \
                  " at price " + str(event._dataAsDataFrames["Price"]))
