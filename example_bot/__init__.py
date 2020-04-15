from events import EventDispatcher
from events.PumpAndDumpEvent import PumpAndDumpEvent
from example_bot.ExampleBot import ExampleBot

if __name__ == "__main__":
    bot = ExampleBot()
    EventDispatcher.getInstance().addListener(bot, "PumpAndDump")
    EventDispatcher.getInstance().dispatchEvent(PumpAndDumpEvent("ABUS", 0.25))
