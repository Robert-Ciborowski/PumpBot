# Name: Start
# Author: Robert Ciborowski
# Date: 14/04/2020
# Description: Starts the program.
import time

from discord_bot import DiscordBot
from events import EventDispatcher
from example_bot import ExampleBot
from filter import StockFilterByPrice
from filter.PassThroughStockFilter import PassThroughStockFilter
from listing_obtainers.BinanceObtainer import BinanceObtainer
from listing_obtainers.NASDAQObtainer import NASDAQObtainer
from models.DummyPumpAndDumpDetector import DummyPumpAndDumpDetector
from datetime import datetime

from stock_data import CurrentStockDataObtainer
from stock_data.CurrentBinanceDataObtainer import CurrentBinanceDataObtainer
from stock_data.HistoricStockDataObtainer import HistoricStockDataObtainer
from stock_data.TrackedStockDatabase import TrackedStockDatabase

if __name__ == "__main__":
    dataObtainer = CurrentBinanceDataObtainer()
    binance_obtainer = BinanceObtainer()
    filter = PassThroughStockFilter(dataObtainer)
    filter.addListings(binance_obtainer)\
        .getDataForFiltering()\
        .filter()

    database = TrackedStockDatabase.getInstance()
    database.useObtainer(dataObtainer)\
           .trackStocksInFilter(filter)\
           .setSecondsBetweenStockUpdates(15)

    bot = ExampleBot()
    EventDispatcher.getInstance().addListener(bot, "PumpAndDump")

    bot = DiscordBot(CurrentBinanceDataObtainer(), "bot_properties.json",
                     "bot_secret_properties.json", "8")
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
