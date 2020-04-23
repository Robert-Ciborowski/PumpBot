if __name__ == "__main__":
    import time

    from discord_bot.DiscordBot import DiscordBot
    from events import EventDispatcher
    from events.PumpAndDumpEvent import PumpAndDumpEvent

    bot = DiscordBot()
    bot.runOnSeperateThread()
    EventDispatcher.getInstance().addListener(bot, "PumpAndDump")

    time.sleep(4)
    EventDispatcher.getInstance().dispatchEvent(PumpAndDumpEvent("ABUS", 0.2555))
