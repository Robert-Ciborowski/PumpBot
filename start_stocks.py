# Name: Start
# Author: Robert Ciborowski
# Date: 14/04/2020
# Description: Starts the program.
import time

from discord_bot import DiscordBot
from events import EventDispatcher
from example_bot import ExampleBot
from filter import StockFilterByPrice
from listing_obtainers.NASDAQListingObtainer import NASDAQListingObtainer
from models.DummyPumpAndDumpDetector import DummyPumpAndDumpDetector
from datetime import datetime

from stock_data import CurrentStockDataObtainer
from stock_data.HistoricStockDataObtainer import HistoricStockDataObtainer
from stock_data.TrackedStockDatabase import TrackedStockDatabase

if __name__ == "__main__":
    # April 1st, 2020 at 11:30 am.
    # stockDataObtainer = HistoricStockDataObtainer(datetime(2020, 4, 1, 11, 30))
    stockDataObtainer = CurrentStockDataObtainer()
    nasdaq_obtainer = NASDAQListingObtainer(20)
    filter = StockFilterByPrice(10, stockDataObtainer)
    filter.addListings(nasdaq_obtainer)\
        .getDataForFiltering()\
        .filter()

    database = TrackedStockDatabase.getInstance()
    database.useObtainer(stockDataObtainer)\
           .trackStocksInFilter(filter)\
           .setMillisecondsBetweenStockUpdates(15)

    bot = ExampleBot()
    EventDispatcher.getInstance().addListener(bot, "PumpAndDump")

    bot = DiscordBot(CurrentStockDataObtainer(), "bot_properties.json",
                     "bot_secret_properties.json")
    bot.runOnSeperateThread()
    EventDispatcher.getInstance().addListener(bot, "PumpAndDump")

    model = DummyPumpAndDumpDetector(0.001)
    EventDispatcher.getInstance().addListener(model, "ListingPriceUpdated")

    database.startSelfUpdating()

    time.sleep(190885)
    print("It is time to stop.")
    database.stopSelfUpdating()
    bot.stopRunning()
    # print(database.getCurrentStock("AAB.TO"))
