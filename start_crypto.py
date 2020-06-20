# Name: Start
# Author: Robert Ciborowski
# Date: 14/04/2020
# Description: Starts the program.
import json
import time
from typing import Dict

from discord_bot.DiscordBot import DiscordBot
from events.EventDispatcher import EventDispatcher
from example_bot.ExampleBot import ExampleBot
from filter import StockFilterByPrice
from filter.PassThroughStockFilter import PassThroughStockFilter
from listing_obtainers.BinanceListingObtainer import BinanceListingObtainer
from listing_obtainers.NASDAQListingObtainer import NASDAQListingObtainer
from listing_obtainers.SpecifiedListingObtainer import SpecifiedListingObtainer
from models.CryptoPumpAndDumpDetector import CryptoPumpAndDumpDetector
from models.DummyPumpAndDumpDetector import DummyPumpAndDumpDetector
from datetime import datetime

from stock_data import CurrentStockDataObtainer
from stock_data.CurrentBinanceDataObtainer import CurrentBinanceDataObtainer
from stock_data.HistoricStockDataObtainer import HistoricStockDataObtainer
from stock_data.TrackedStockDatabase import TrackedStockDatabase
from trading.BasicInvestmentStrategy import BasicInvestmentStrategy
from trading.ProfitPumpTrader import ProfitPumpTrader
from wallet.BinanceWallet import BinanceWallet


def getProperties(propertiesFile: str) -> Dict:
    try:
        with open(propertiesFile, mode='r') as file:
            data = json.load(file)
            return data
    except:
        print(
            "You are missing " + propertiesFile + ". Please ask Robert" \
                                                  "(robert.ciborowski"
                                                  "@mail.utoronto.ca) for "
                                                  "help.")

if __name__ == "__main__":
    # tickers = ["BNBBTC", "BQXBTC", "FUNBTC", "GASBTC", "HSRBTC",
    #            "KNCBTC", "LRCBTC", "LTCBTC", "MCOBTC", "NEOBTC", "OAXBTC",
    #            "OMGBTC", "QTUMBTC", "SNGLSBTC", "STRATBTC", "WTCBTC",
    #            "YOYOBTC", "ZRXBTC"]
    tickers = ["SNGLSBTC", "STRATBTC"]

    properties = getProperties("crypto_properties.json")

    # This sets up data obtaining.
    dataObtainer = CurrentBinanceDataObtainer()
    listings_obtainer = SpecifiedListingObtainer(tickers)
    filter = PassThroughStockFilter(dataObtainer)
    filter.addListings(listings_obtainer) \
        .getDataForFiltering() \
        .filter()

    # This sets up the price & volume database.
    database = TrackedStockDatabase.getInstance()
    database.useObtainer(dataObtainer)\
           .trackStocksInFilter(filter)\
           .setSecondsBetweenStockUpdates(60)

    # This sets up bots that output messages.
    bot = ExampleBot()
    EventDispatcher.getInstance().addListener(bot, "PumpAndDump")

    bot = DiscordBot(CurrentBinanceDataObtainer(), "bot_properties.json",
                     "bot_secret_properties.json", "8")
    bot.runOnSeperateThread()
    EventDispatcher.getInstance().addListener(bot, "PumpAndDump")

    # This sets up the model.
    model = CryptoPumpAndDumpDetector()
    model.setupUsingDefaults()
    model.createModelUsingDefaults()
    model.exportPath = "models/model_exports/cryptopumpanddumpdetector"
    model.loadWeights()
    model.prepareForUse()
    EventDispatcher.getInstance().addListener(model, "ListingPriceUpdated")

    # This sets up the wallet.
    wallet = BinanceWallet()
    wallet.useBinanceKeysFromFile("binance_properties.json")

    # This sets up the trader.
    trader = ProfitPumpTrader(
        BasicInvestmentStrategy(properties["Investment Ratio"]),
        wallet,
        profitRatioToAimFor=properties["Target Profit Ratio"],
        acceptableLossRatio=properties["Acceptable Loss Ratio"],
        minutesAfterSellIfPump=properties["Minutes After Pump Sell"],
        minutesAfterSellIfPriceInactivity=properties["Minutes After Price-Inactive Sell"],
        minutesAfterSellIfLoss=properties["Minutes After Loss Sell"],
        maxTimeToHoldStock=properties["Max Time To Hold Stock"],
        fastForwardAmount=1)
    EventDispatcher.getInstance().addListener(trader, "PumpAndDump")

    # This starts the trading!
    database.startSelfUpdating()
    trader.start()

    time.sleep(190885)

    # This stops the trading.
    print("It is time to stop.")
    database.stopSelfUpdating()
    trader.stop()
    bot.stopRunning()

    # This outputs statistics.
    print("Ended cryptocurrency trading.")
    print("Results:")
    print(trader.tracker.tradesStr())
    print("=== Profits (in BTC) ===")
    print(trader.tracker.calculateProfits())
