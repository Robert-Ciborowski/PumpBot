import time
from datetime import datetime, timedelta
from typing import List
import pandas as pd
import numpy as np
import threading as th

from events.EventDispatcher import EventDispatcher
from filter.PassThroughStockFilter import PassThroughStockFilter
from listing_obtainers.BinanceListingObtainer import BinanceListingObtainer
from listing_obtainers.SpecifiedListingObtainer import SpecifiedListingObtainer
from models.CryptoPumpAndDumpDetector import CryptoPumpAndDumpDetector
from stock_data.HistoricalBinanceDataObtainer import \
    HistoricalBinanceDataObtainer
from stock_data.TrackedStockDatabase import TrackedStockDatabase
from thread_runner.ThreadRunner import ThreadRunner
from trading.BasicInvestmentStrategy import BasicInvestmentStrategy
from trading.MinutePumpTrader import MinutePumpTrader
from trading.ProfitPumpTrader import ProfitPumpTrader
from trading.PumpTrader import PumpTrader

from wallet.SimpleWallet import SimpleWallet
from wallet.Wallet import Wallet


class HistoricalBinanceTradingSimulator:
    startDate: datetime
    endDate: datetime
    maxTimeToHoldStock: int
    minutesAfterSellIfPump: int
    minutesAfterSellIfPriceInactivity: int
    minutesAfterSellIfLoss: int
    trader: PumpTrader
    database: TrackedStockDatabase
    dataObtainer: HistoricalBinanceDataObtainer
    model: CryptoPumpAndDumpDetector
    investmentFraction: float
    wallet: Wallet
    tickers: List
    modelLocation: str
    historicalDataLocation: str
    threadRunner: ThreadRunner

    _fastForwardAmount: int

    def __init__(self, startDate: datetime, endDate: datetime, wallet: Wallet,
                 minutesBeforeSell: int, minutesAfterSell: int,
                 minutesAfterSellIfPriceInactivity: int,
                 minutesAfterSellIfLoss: int, investmentFraction: float,
                 coins: List, fastForwardAmount=1,
                 modelLocation="../models/model_exports/cryptopumpanddumpdetector",
                 historicalDataLocation="../binance_historical_data"):
        self.startDate = startDate
        self.endDate = endDate
        self.maxTimeToHoldStock = minutesBeforeSell
        self.minutesAfterSellIfPump = minutesAfterSell
        self.minutesAfterSellIfPriceInactivity = minutesAfterSellIfPriceInactivity
        self.minutesAfterSellIfLoss = minutesAfterSellIfLoss
        self._fastForwardAmount = fastForwardAmount
        self.investmentFraction = investmentFraction
        self.wallet = wallet
        self.tickers = coins
        self.modelLocation = modelLocation
        self.historicalDataLocation = historicalDataLocation
        sleepAmount = (self.endDate - self.startDate).total_seconds() // self._fastForwardAmount
        self.threadRunner = ThreadRunner(endTime=datetime.now() + timedelta(seconds=sleepAmount))
        self._setup()

    def _setup(self):
        # We add an hour to the end date just in case.
        self.dataObtainer = HistoricalBinanceDataObtainer(self.startDate,
                                                          self.endDate + timedelta(days=1),
                                                          filePathPrefix=self.historicalDataLocation + "/",
                                                          fastForwardAmount=self._fastForwardAmount)
        listings_obtainer = SpecifiedListingObtainer(self.tickers)
        filter = PassThroughStockFilter(self.dataObtainer)
        filter.addListings(listings_obtainer) \
            .getDataForFiltering() \
            .filter()

        self.database = TrackedStockDatabase.getInstance()
        self.database.useObtainer(self.dataObtainer) \
            .trackStocksInFilter(filter) \
            .setSecondsBetweenStockUpdates(60 / self._fastForwardAmount)
        # .setSecondsBetweenStockUpdates(60)

        self.model = CryptoPumpAndDumpDetector(tryUsingGPU=False, threadRunner=self.threadRunner)
        self.model.setupUsingDefaults()
        self.model.createModelUsingDefaults()
        self.model.exportPath = self.modelLocation
        self.model.loadWeights()
        self.model.prepareForUse()
        EventDispatcher.getInstance().addListener(self.model,
                                                  "ListingPriceUpdated")
        self.database.model = self.model


        # self.trader = MinutePumpTrader(BasicInvestmentStrategy(self.investmentFraction),
        #                                Transactor(),
        #                                minutesBeforeSell=self.minutesBeforeSell,
        #                                minutesAfterSell=self.minutesAfterSell,
        #                                fastForwardAmount=self._fastForwardAmount,
        #                                startingFunds=self.startingFunds)
        print("MAIN THREAD: " + str(th.current_thread().ident))
        self.trader = ProfitPumpTrader(
            BasicInvestmentStrategy(self.investmentFraction),
            self.wallet,
            profitRatioToAimFor=0.07,
            acceptableLossRatio=0.02,
            minutesAfterSellIfPump=self.minutesAfterSellIfPump,
            minutesAfterSellIfPriceInactivity=self.minutesAfterSellIfPriceInactivity,
            minutesAfterSellIfLoss=self.minutesAfterSellIfLoss,
            maxTimeToHoldStock=self.maxTimeToHoldStock,
            fastForwardAmount=self._fastForwardAmount)
        EventDispatcher.getInstance().addListener(self.trader, "PumpAndDump")

    def start(self):
        print("Starting historical Binance trading simulator...")

        # If not using threadrunner:
        # self.database.startSelfUpdating()
        # self.trader.start()

        # If using threadrunner:
        self.database.useThreadRunner(self.threadRunner)
        self.trader.useThreadRunner(self.threadRunner)

        self.dataObtainer.setStartTimeToNow()

        print("Started historical Binance trading simulator.")
        self.threadRunner.start()

        print("It is time to stop.")
        # self.database.stopSelfUpdating()
        # self.trader.stop()
        print("Finished historical Binance trading simulation.")
        print("Results:")
        print(self.trader.tracker.tradesStr())
        print("=== Profits (in BTC) ===")
        print(self.trader.tracker.calculateProfits())
