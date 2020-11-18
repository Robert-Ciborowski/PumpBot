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
from logger.Logger import Logger
from models.CryptoPumpAndDumpDetector import CryptoPumpAndDumpDetector
from models.DummyPumpAndDumpDetector import DummyPumpAndDumpDetector
from datetime import datetime, timedelta

from stock_data import CurrentStockDataObtainer
from stock_data.CurrentBinanceDataObtainer import CurrentBinanceDataObtainer
from stock_data.HistoricStockDataObtainer import HistoricStockDataObtainer
from stock_data.TrackedStockDatabase import TrackedStockDatabase
from thread_runner.ThreadRunner import ThreadRunner
from trading.BasicInvestmentStrategy import BasicInvestmentStrategy
from trading.ProfitPumpTrader import ProfitPumpTrader
from util.Constants import MINUTES_OF_DATA_TO_LOOK_AT_FOR_MODEL, \
    SAMPLES_PER_MINUTE, SECONDS_BETWEEN_SAMPLES
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
    tickers = ["OAXBTC"]

    properties = getProperties("crypto_properties.json")

    # For logging our outputs to a file
    import sys
    sys.stdout = Logger("crypto_output.txt")

    # This sets up data obtaining.
    dataObtainer = CurrentBinanceDataObtainer(MINUTES_OF_DATA_TO_LOOK_AT_FOR_MODEL * SAMPLES_PER_MINUTE, SECONDS_BETWEEN_SAMPLES)
    listings_obtainer = SpecifiedListingObtainer(tickers)
    filter = PassThroughStockFilter(dataObtainer)
    filter.addListings(listings_obtainer) \
        .getDataForFiltering() \
        .filter()

    # This sets up the price & volume database.
    database = TrackedStockDatabase.getInstance()
    database.useObtainer(dataObtainer) \
        .trackStocksInFilter(filter) \
        .setSecondsBetweenStockUpdates(SECONDS_BETWEEN_SAMPLES)

    # This sets up bots that output messages.
    # bot = ExampleBot()
    # EventDispatcher.getInstance().addListener(bot, "PumpAndDump")
    #
    discordObtainer = CurrentBinanceDataObtainer(MINUTES_OF_DATA_TO_LOOK_AT_FOR_MODEL * SAMPLES_PER_MINUTE, SECONDS_BETWEEN_SAMPLES)
    discordObtainer.trackStocks(tickers)
    bot = DiscordBot(discordObtainer, "bot_properties.json",
                     "bot_secret_properties.json", "8")
    bot.runOnSeperateThread()
    EventDispatcher.getInstance().addListener(bot, "Investment")

    # This sets up the model.
    model = CryptoPumpAndDumpDetector()
    model.setupUsingDefaults()
    model.createModelUsingDefaults()
    model.exportPath = "models/model_exports/cryptopumpanddumpdetector"
    model.loadWeights()
    model.prepareForUse()
    EventDispatcher.getInstance().addListener(model, "ListingPriceUpdated")

    # This sets up the wallet.
    wallet = BinanceWallet(baseCurrency="BTC")
    wallet.useBinanceKeysFromFile("binance_properties.json")
    print(wallet.getBalance("OAXBTC"))
    print("Current balance: " + str(wallet.getBalance()))
    # wallet.purchase("OAXBTC", 0.0, 100, test=True)
    # wallet.sell("OAXBTC", 0.0, 100, test=True)
    print("Current balance: " + str(wallet.getBalance()))

    # This sets up the trader.
    trader = ProfitPumpTrader(
        BasicInvestmentStrategy(properties["Investment Ratio"]),
        wallet,
        profitRatioToAimFor=properties["Target Profit Ratio"],
        acceptableLossRatio=properties["Acceptable Loss Ratio"],
        acceptableDipFromStartRatio=properties["Acceptable Dip From Start Ratio"],
        minutesAfterSellIfPump=properties["Minutes After Pump Sell"],
        minutesAfterSellIfPriceInactivity=properties["Minutes After Price-Inactive Sell"],
        minutesAfterSellIfLoss=properties["Minutes After Loss Sell"],
        maxTimeToHoldStock=properties["Max Time To Hold Stock"],
        fastForwardAmount=1)
    EventDispatcher.getInstance().addListener(trader, "PumpAndDump")

    threadRunner = ThreadRunner(endTime=datetime.now() + timedelta(days=7))
    database.useThreadRunner(threadRunner)
    trader.useThreadRunner(threadRunner)

    print("Started trading crypto!")
    threadRunner.start()

    # This starts the trading!
    # database.startSelfUpdating()
    # trader.start()

    # This stops the trading.
    print("It is time to stop.")
    # database.stopSelfUpdating()
    # trader.stop()
    # bot.stopRunning()

    # This outputs statistics.
    print("Ended cryptocurrency trading.")
    print("Results:")
    print(trader.tracker.tradesStr())
    print("=== Profits (in BTC) ===")
    print(trader.tracker.calculateProfits())
