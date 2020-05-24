# Name: Start
# Author: Robert Ciborowski
# Date: 14/04/2020
# Description: Starts the program.
import time

from discord_bot.DiscordBot import DiscordBot
from events.EventDispatcher import EventDispatcher
from example_bot.ExampleBot import ExampleBot
from filter import StockFilterByPrice
from filter.PassThroughStockFilter import PassThroughStockFilter
from listing_obtainers.BinanceListingObtainer import BinanceListingObtainer
from listing_obtainers.NASDAQListingObtainer import NASDAQListingObtainer
from models.CryptoPumpAndDumpDetector import CryptoPumpAndDumpDetector
from models.DummyPumpAndDumpDetector import DummyPumpAndDumpDetector
from datetime import datetime

from stock_data import CurrentStockDataObtainer
from stock_data.CurrentBinanceDataObtainer import CurrentBinanceDataObtainer
from stock_data.HistoricStockDataObtainer import HistoricStockDataObtainer
from stock_data.TrackedStockDatabase import TrackedStockDatabase

if __name__ == "__main__":
    dataObtainer = CurrentBinanceDataObtainer()
    binance_obtainer = BinanceListingObtainer()
    filter = PassThroughStockFilter(dataObtainer)
    filter.addListings(binance_obtainer)\
        .getDataForFiltering()\
        .filter()

    database = TrackedStockDatabase.getInstance()
    database.useObtainer(dataObtainer)\
           .trackStocksInFilter(filter)\
           .setSecondsBetweenStockUpdates(60)

    bot = ExampleBot()
    EventDispatcher.getInstance().addListener(bot, "PumpAndDump")

    bot = DiscordBot(CurrentBinanceDataObtainer(), "bot_properties.json",
                     "bot_secret_properties.json", "8")
    bot.runOnSeperateThread()
    EventDispatcher.getInstance().addListener(bot, "PumpAndDump")

    # model = DummyPumpAndDumpDetector(0.001)
    # EventDispatcher.getInstance().addListener(model, "ListingPriceUpdated")

    model = CryptoPumpAndDumpDetector()
    model.setupUsingDefaults()
    model.createModelUsingDefaults()
    model.exportPath = "./models/model_exports/cryptopumpanddumpdetector"
    model.loadWeights()
    EventDispatcher.getInstance().addListener(model, "ListingPriceUpdated")

    database.startSelfUpdating()

    time.sleep(190885)
    print("It is time to stop.")
    database.stopSelfUpdating()
    bot.stopRunning()
    # print(database.getCurrentStock("AAB.TO"))
