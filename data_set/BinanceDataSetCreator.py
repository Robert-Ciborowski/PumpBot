# Name: BinanceDataSetCreator
# Author: Robert Ciborowski
# Date: 19/04/2020
# Description: Creates a data set for Binance Pump & Dumps.
import math
from math import pi
from random import uniform, randint
from typing import List

from stock_data import HistoricalBinanceDataObtainer
import pandas as pd
from matplotlib import pyplot as plt
import csv

from util.Constants import GROUPED_DATA_SIZE, BIN_SIZE_FOR_BINNING, SAMPLES_OF_DATA_TO_LOOK_AT, \
    ROLLING_AVERAGE_SIZE, EXTENDED_SAMPLES_OF_DATA_TO_LOOK_AT


class BinanceDataSetCreator:
    dataObtainer: HistoricalBinanceDataObtainer
    numberOfSamples: int
    samplesBeforePumpPeak: int

    def __init__(self, dataObtainer: HistoricalBinanceDataObtainer):
        self.dataObtainer = dataObtainer
        self.numberOfSamples = SAMPLES_OF_DATA_TO_LOOK_AT
        # self.samplesBeforePumpPeak = 3
        self.samplesBeforePumpPeak = 0
        # self.samplesBeforePumpPeak = 30
        # self.samplesBeforePumpPeak = 7

    def exportPumpsToCSV(self, symbol: str, rightBeforePumps: List,
                         areTheyPumps=True, pathPrefix=""):
        if len(rightBeforePumps) == 0:
            return

        if areTheyPumps:
            path = pathPrefix + symbol + "-pumps.csv"
        else:
            path = pathPrefix + symbol + "-non-pumps.csv"

        try:
            with open(path, 'w', newline='') as file:
                writer = csv.writer(file)
                # numberOfRAs = self.numberOfSamples
                priceList = ["Price-" + str(i) for i in range(SAMPLES_OF_DATA_TO_LOOK_AT)]
                priceRAList = ["Price-RA-" + str(i) for i in range(SAMPLES_OF_DATA_TO_LOOK_AT)]
                volumeList = ["Volume-" + str(i) for i in range(SAMPLES_OF_DATA_TO_LOOK_AT)]
                volumeRAList = ["Volume-RA-" + str(i) for i in range(SAMPLES_OF_DATA_TO_LOOK_AT)]
                # volumeList = ["Volume-RA-" + str(i) for i in range(int(SAMPLES_OF_DATA_TO_LOOK_AT / GROUPED_DATA_SIZE))]
                # priceList = ["Price-RA-" + str(i) for i in range(int(SAMPLES_OF_DATA_TO_LOOK_AT / GROUPED_DATA_SIZE))]
                # volumeList2 = ["Volume-RA2-" + str(i) for i in range(int(SAMPLES_OF_DATA_TO_LOOK_AT / GROUPED_DATA_SIZE / 2))]
                # priceList2 = ["Price-RA2-" + str(i) for i in range(int(SAMPLES_OF_DATA_TO_LOOK_AT / GROUPED_DATA_SIZE / 2))]
                # volumeList3 = ["Volume-RA3-" + str(i) for i in range(int(SAMPLES_OF_DATA_TO_LOOK_AT / GROUPED_DATA_SIZE / 3))]
                # priceList3 = ["Price-RA3-" + str(i) for i in range(int(SAMPLES_OF_DATA_TO_LOOK_AT / GROUPED_DATA_SIZE / 3))]
                writer.writerow(priceList + priceRAList + volumeList + volumeRAList + ["Pump"])
                count = 1

                for df in rightBeforePumps:
                    print(str(count) + "/" + str(len(rightBeforePumps)) + " arePumps: " + str(areTheyPumps))
                    count += 1
                    # if str(ROLLING_AVERAGE_SIZE) + "m Volume RA" not in df.columns:
                    #     print(str(ROLLING_AVERAGE_SIZE) + "m Volume RA not in dataframe! Are they pumps: " + str(areTheyPumps))
                    #     print(df.columns)
                    #     continue

                    mean = df["Volume"].mean()
                    std = df["Volume"].std()
                    volumes = (df["Volume"] - mean) / std
                    mean = df["Close"].mean()
                    std = df["Close"].std()
                    prices = (df["Close"] - mean) / std
                    # volumes = volumes.abs()
                    # prices = prices.abs()
                    # volumes = volumes / volumes.max()
                    # prices = prices / prices.max()
                    # volumes = df["Volume"]
                    # prices = df["Close"]
                    # pricesMax = prices.max()

                    priceRA = prices.rolling(window=24, min_periods=1,
                                               center=False).mean()
                    volumeRA = volumes.rolling(window=24, min_periods=1,
                                               center=False).mean()

                    pricesMax = prices.max()

                    if pricesMax < 10:
                        pricesMax = 10

                    pricesRAMax = priceRA.max()

                    if pricesRAMax < 10:
                        pricesRAMax = 10

                    prices = prices / pricesMax
                    priceRA = priceRA / pricesRAMax

                    volumesMax = volumes.max()

                    if volumesMax < 10:
                        volumesMax = 10

                    volumesRAMax = volumeRA.max()

                    if volumesRAMax < 10:
                        volumesRAMax = 10

                    volumes = volumes / volumesMax
                    volumeRA = volumeRA / volumesRAMax

                    # prices = prices / pricesMax

                    # max = df["Volume"].max()
                    # volumes = df["Volume"] / max
                    # max = df["Close"].max()
                    # prices = df["Close"] / max
                    # csvRow = []

                    # volumes = pd.cut(volumes, bins=MEME).value_counts().values
                    # prices = pd.cut(prices, bins=MEME).value_counts().values
                    # volumes = df["Volume"]
                    # prices = df["Close"]

                    # volumesDf = df["Volume"]
                    # pricesDf = df["Close"]
                    #
                    # volumes, prices = self._generateVolumeAndPriceData(volumesDf, pricesDf, GROUPED_DATA_SIZE)
                    # volumes2, prices2 = self._generateVolumeAndPriceData(volumesDf, pricesDf, GROUPED_DATA_SIZE * 2)
                    # volumes3, prices3 = self._generateVolumeAndPriceData(volumesDf, pricesDf, GROUPED_DATA_SIZE * 3)

                    # Becomes true if a value is nan so that we can skip this
                    # pump.
                    cancel = False
                    extension = EXTENDED_SAMPLES_OF_DATA_TO_LOOK_AT
                    numTimes = 80

                    if not areTheyPumps:
                        numTimes = 4
                        # extension = 0

                    for i in range(numTimes):
                        csvRow = []
                        offset = randint(0, extension)
                        scaling = uniform(0.8, 1.4)

                        for i in range(offset, self.numberOfSamples + offset):
                            value = prices[i]

                            if math.isnan(value):
                                cancel = True
                                break

                            csvRow.append(value * uniform(0.998, 1.002) * scaling)

                        if cancel:
                            continue

                        for i in range(offset, self.numberOfSamples + offset):
                            value = priceRA[i]

                            if math.isnan(value):
                                cancel = True
                                break

                            csvRow.append(value * uniform(0.998, 1.002) * scaling)

                        if cancel:
                            continue

                        scaling = uniform(0.8, 1.4)

                        for i in range(offset, self.numberOfSamples + offset):
                            value = volumes[i]

                            if math.isnan(value):
                                cancel = True
                                break

                            csvRow.append(value * uniform(0.998, 1.002) * scaling)

                        if cancel:
                            continue

                        for i in range(offset, self.numberOfSamples + offset):
                            value = volumeRA[i]

                            if math.isnan(value):
                                cancel = True
                                break

                            csvRow.append(value * uniform(0.998, 1.002) * scaling)

                        if cancel:
                            continue

                        if areTheyPumps:
                            csvRow.append(1)
                        else:
                            csvRow.append(0)

                        writer.writerow(csvRow)

                    # for value in prices:
                    #     if math.isnan(value):
                    #         cancel = True
                    #         break
                    #     csvRow.append(value)
                    #
                    # if cancel:
                    #     continue

                    # for value in volumes2:
                    #     if math.isnan(value):
                    #         cancel = True
                    #         break
                    #
                    #     csvRow.append(value)
                    #
                    # if cancel:
                    #     continue
                    #
                    # for value in prices2:
                    #     if math.isnan(value):
                    #         cancel = True
                    #         break
                    #     csvRow.append(value)
                    #
                    # if cancel:
                    #     continue
                    #
                    # for value in volumes3:
                    #     if math.isnan(value):
                    #         cancel = True
                    #         break
                    #
                    #     csvRow.append(value)
                    #
                    # if cancel:
                    #     continue
                    #
                    # for value in prices3:
                    #     if math.isnan(value):
                    #         cancel = True
                    #         break
                    #     csvRow.append(value)
                    #
                    # if cancel:
                    #     continue



        except IOError as e:
            print("Error writing to csv file! " + str(e))

    def createFinalPumpsDataSet(self, pumps: List, rightBeforePumps: List):
        # lst = []
        actualPumps = []
        falsePositives = []
        length = len(pumps)
        print("Automatically add all pumps to dataset? (y/n)")
        input1 = input()

        if input1 == "y":
            for i in range(0, length):
                df2 = rightBeforePumps[i]
                self._addRAs(df2, ROLLING_AVERAGE_SIZE)

            return rightBeforePumps, falsePositives

        print("Please tell me if these are pumps or not.")
        print("'y' = pump, 'n' = not a pump, 'm' = not a pump, add to non-pump dataset")

        i = 0
        while i < length:
            print("Is this a pump? " + str(i + 1) + "/" + str(length))
            df = pumps[i]
            df2 = rightBeforePumps[i]
            self._plotWithPyPlot(df, df2, i)
            input1 = input()

            if input1 == "y":
                # lst.append(df)
                self._addRAs(df2, ROLLING_AVERAGE_SIZE)
                actualPumps.append(df2)
                i += 1
            elif input1 == "n":
                i += 1
                continue
            elif input1 == "m":
                self._addRAs(df2, ROLLING_AVERAGE_SIZE)
                falsePositives.append(df2)
                i += 1
            else:
                print("Invalid input.")

        return actualPumps, falsePositives

    def createFinalNonPumpsDataSet(self, pumps: List, rightBeforePumps: List):
        # We don't need to do anything anymore.
        return rightBeforePumps

    def findPumpsForSymbols(self, symbols: List[str], amountToIncrement: int):
        """
        Returns random non-pumps for a list of symbols.
        Precondition: symbols is not empty!!!

        :param symbols: the symbols
        :param amountToIncrement: the amount of time to increment by after
               finding a pump, in minutes
        :return: a tuple (df, df2) of dataframe lists where df contains pumps,
                 df2 contains the moment before the pumps.
        """
        lst1, lst2 = [], []

        for i in range(0, len(symbols)):
            lst3, lst4 = self.findPumpsForSymbol(symbols[i], amountToIncrement)
            print(symbols[i] + " had " + str(len(lst4)) + " potential pumps!")
            lst1 += lst3
            lst2 += lst4

        return lst1, lst2

    def findNonPumpsForSymbols(self, symbols: List[str], amountToIncrement: int):
        """
        Returns random non-pumps for a list of symbols.
        Precondition: symbols is not empty!!!

        :param symbols: the symbols
        :param amountToIncrement: the amount of time to increment by after
               finding a pump, in minutes
        :return: a tuple (df, df2) of dataframe lists where df contains
                 non-pumps, df2 contains non-pumps of size self.numberOfSamples
        """
        lst1, lst2 = [], []

        for i in range(0, len(symbols)):
            lst3, lst4 = self.findNonPumpsForSymbol(symbols[i], amountToIncrement)
            lst1 += lst3
            lst2 += lst4

        return lst1, lst2

    def findPumpsForSymbol(self, symbol: str, amountToIncrement: int):
        """
        Returns pumps for a symbol.
        Precondition: symbol is not empty!!!

        :param symbol: the symbols
        :param amountToIncrement: the amount of time to increment by after
               finding a pump, in minutes
        :return: a tuple (df, df2) of dataframes where df contains pump & dumps,
                 df2 contains the moment before the pump.
        """
        df = self.dataObtainer.getHistoricalDataAsDataframe(symbol)
        dfs = []
        dfs2 = []

        for i in range(0, self._getNumberOfRows(df) - amountToIncrement, amountToIncrement):
            rowEntry, df = self.findPumpAndDumps(symbol, i, i + amountToIncrement)

            if rowEntry["Pump and Dumps"] > 0:
                for df2 in rowEntry["Right Before DF"]:
                    dfs.append(df)
                    dfs2.append(df2)

        return dfs, dfs2

    def findNonPumpsForSymbol(self, symbol: str, amountToIncrement: int):
        """
        Returns random non-pumps for a symbol.
        Precondition: symbols is not empty!!!

        :param symbol: the symbol
        :param amountToIncrement: the amount of time to increment by after
               finding a pump, in minutes
        :return: a tuple (df, df2) of dataframes where df contains non-pumps,
                 df2 contains non-pumps of size self.numberOfSamples
        """
        df = self.dataObtainer.getHistoricalDataAsDataframe(symbol)
        dfs = []
        dfs2 = []

        for i in range(0, self._getNumberOfRows(df) - amountToIncrement,
                       amountToIncrement):
            rowEntry, df2 = self.findPumpAndDumps(symbol, i,
                                                 i + amountToIncrement)

            if rowEntry["Pump and Dumps"] == 0:
                dfs.append(df2)

                for i in range(0, amountToIncrement - self.numberOfSamples - EXTENDED_SAMPLES_OF_DATA_TO_LOOK_AT, 3):
                    # df3 = df2.iloc[i:i + int(self.numberOfSamples * 0.9)]
                    # std = df3.std(axis=0, skipna=True)["Close"]
                    df4 = df2.iloc[i:i + self.numberOfSamples + EXTENDED_SAMPLES_OF_DATA_TO_LOOK_AT]
                    # std = df4.std(axis=0, skipna=True)["Close"]

                    # if std < 5.0e-08:
                    # if df4["Close"].max() > df4["Close"].min() * 1.025:
                    dfs2.append(df4)

        return dfs, dfs2


    def findPumpAndDumps(self, symbol: str, startIndex: int, endIndex: int,
                         plot=False):
        df = self.dataObtainer.getHistoricalDataAsDataframe(symbol).iloc[startIndex:endIndex]
        # return self._analyseSymbolForPumps(symbol, df, 3, 1.05), df
        # return self._analyseSymbolForPumps(symbol, df, 2.5, 1.05), df
        # return self._analyseSymbolForPumps(symbol, df, 2.0, 1.05), df
        # return self._analyseSymbolForPumps(symbol, df, 1.0, 1.045, 1.045), df
        return self._analyseSymbolForPumps(symbol, df, 1.0, 1.04, 1.04), df

    # returns final dataframe
    def _analyseSymbolForPumps(self, symbol: str, df: pd.DataFrame, volumeThreshold: float,
                               priceThreshold: float, priceThreshold2: float, windowSize=ROLLING_AVERAGE_SIZE * 2):
        """
        :param symbol: symbol code (e.g. OAXBTC)
        :param df: pandas dataframe with the data
        :param volumeThreshold: volume threshold, e.g. 5 (500%)
        :param priceThreshold: price threshold, e.g. 1.05 (5%)
        :param windowSize: size of the window to use for computing rolling
               average, in hours
        :return: a dict with all the computed data (see end of this function)
        """
        exchangeName = "binance"

        # This finds spikes for volume and price.
        volumeMask = self._findVolumeSpikes(df, volumeThreshold, windowSize)
        # volumeSpikeAmount = self._getNumberOfRows(vdf)

        pmask, pmask2 = self._findPriceSpikes(df, priceThreshold, priceThreshold2, windowSize)
        # priceSpikeAmount = self._getNumberOfRows(pdf)

        # pdmask, pddf = self._findPriceDumps(df, windowSize)
        # vdmask, vddf = self._findVolumeDumps(df, windowSize)

        # This finds coinciding price and volume spikes.
        # volumePriceMask = (volumeMask) & (pmask)
        # volumePriceDF = df[volumePriceMask]
        # volumePriceCombinedRowsAmount = self._getNumberOfRows(volumePriceDF)

        # These are coinciding price and volume spikes for alleged P&D (more
        # than 1x per given time removed).
        # volumePriceFinalDF = self._removeSamePumps(volumePriceDF)
        # allegedAmount = self._getNumberOfRows(volumePriceFinalDF)

        # This finds coinciding price and volume spikes (with dumps afterwards).
        # finalMask = (volumeMask) & (pmask) & (pdmask)
        finalMask = (volumeMask) & (pmask) & (pmask2)
        finalDF = df[finalMask]

        # This removes indicators which occur on the same day.
        finalCombined = self._removeSamePumps(finalDF)
        finalCombinedAmount = self._getNumberOfRows(finalCombined)

        pumps = []

        if finalCombinedAmount != 0:
            for i in range(len(finalCombined.index)):
                timeIndex = finalCombined.index[0]
                endIndex = self.dataObtainer.getHistoricalDataAsDataframe(symbol).index.get_loc(timeIndex)\
                           - self.samplesBeforePumpPeak
                startIndex = endIndex - self.numberOfSamples - EXTENDED_SAMPLES_OF_DATA_TO_LOOK_AT

                if startIndex >= 0:
                    pumpPeak = self.dataObtainer.getHistoricalDataAsDataframe(
                            symbol).iloc[endIndex]["Close"]
                    # print("----------")

                    numIters = 0

                    while True:
                        if startIndex < 0 or numIters == 12:
                            break

                        dfToAppend2 = self.dataObtainer.getHistoricalDataAsDataframe(
                            symbol).iloc[startIndex:endIndex]
                        # std = dfToAppend2.std(axis=0, skipna=True)["Close"]
                        # print(str(pumpPeak) + " " + str(dfToAppend2["Close"].max()))

                        # if pumpPeak < dfToAppend2.iloc[0]["Close"]:
                        if pumpPeak < dfToAppend2["Close"].max():
                            break

                        if self.dataObtainer.getHistoricalDataAsDataframe(
                            symbol).iloc[startIndex:startIndex + int(SAMPLES_OF_DATA_TO_LOOK_AT * 0.8)]["Close"].max() * 1.03 > pumpPeak:
                            # if dfToAppend2["Close"].max() > dfToAppend2["Close"].min() * 1.025:
                            startIndex -= 5
                            endIndex -= 5
                            numIters += 1
                            continue

                        half = (endIndex - startIndex) // 2
                        idealDerivative = (self.dataObtainer.getHistoricalDataAsDataframe(
                            symbol).iloc[startIndex + half]["Close"] - self.dataObtainer.getHistoricalDataAsDataframe(
                            symbol).iloc[startIndex]["Close"]) / half

                        derivative = (self.dataObtainer.getHistoricalDataAsDataframe(
                            symbol).iloc[endIndex]["Close"] - self.dataObtainer.getHistoricalDataAsDataframe(
                            symbol).iloc[endIndex - 15]["Close"]) / 15

                        if abs(derivative) > abs(idealDerivative * 1.3):
                            startIndex -= 5
                            endIndex -= 5
                            numIters += 1
                            continue

                        # print("Value " + str(idealDerivative) + " vs " + str(derivative))

                        # diff = abs((dfToAppend2.iloc[-1]["Close"] - dfToAppend2.iloc[0]["Close"]) / dfToAppend2.iloc[0]["Close"])
                        # std = dfToAppend2.std(axis=0, skipna=True)["Close"]

                        # if std > 5.0e-08:
                        #     break

                        # if diff < 0.035 and std < 5.0e-08:
                        # if std < 5.0e-08:
                        pumps.append(dfToAppend2)
                        break

                        startIndex -= 30
                        endIndex -= 30

                        # if std < 2.0e-08:
                        #     pumps.append(dfToAppend2)
                        # else:
                        #     break

                        # startIndex -= self.numberOfSamples
                        # endIndex -= self.numberOfSamples


        rowEntry = {'Exchange': exchangeName,
                    'Symbol': symbol,
                    'Pump and Dumps': finalCombinedAmount,
                    "Right Before DF": pumps
                    }

        return rowEntry

    def _getNumberOfRows(self, df: pd.DataFrame):
        return df.shape[0]

    def _removeSamePumps(self, df: pd.DataFrame):
        """
        Removes spikes that occur on the same day.
        """
        df2 = df.copy()
        # df['Timestamp_SAME'] = df['Timestamp'].apply(
        #     lambda x: x.replace(hour=0, minute=0, second=0))
        # df = df.drop_duplicates(subset='Timestamp_SAME', keep='last')

        prevDate = None
        for index, row in df2.iterrows():
            if prevDate is not None and row["Timestamp"] < prevDate + pd.Timedelta(hours=16):
                df = df.drop(index)

            prevDate = row["Timestamp"]

        return df

    def _findVolumeSpikes(self, df: pd.DataFrame, volumeThreshold: float,
                          windowSize: int):
        """
        Finds volume spikes in a given dataframe, with a certain threshold
        and window size.

        :return: a (boolean_mask,dataframe) tuple
        """
        # -- add rolling average column to df --
        vRA = str(windowSize) + 'm Volume RA'
        self._addRA(df, windowSize, 'Volume', vRA)

        # -- find spikes --
        volumeThreshold = volumeThreshold * df[vRA]
        # This is where the volume is at least v_thresh greater than the x-hr RA
        volumeSpikeMask = df["Volume"] > volumeThreshold
        # volumeSpikeDF = df[volumeSpikeMask]
        return volumeSpikeMask

    def _findPriceSpikes(self, df: pd.DataFrame, priceThreshold: float,
                         priceThreshold2: float, windowSize: int):
        """
        Finds price spikes in a given df, with a certain threshold and window
        size.

        :return: a (boolean_mask,dataframe) tuple
        """
        # -- add rolling average column to df --
        pRA = str(windowSize) + "m Close Price RA"
        pRA2 = pRA + " Backwards"
        self._addRA(df, windowSize, "Close", pRA)
        self._addBackwardsRA(df, windowSize, "Close", pRA2)

        # -- find spikes --
        newThreshold = priceThreshold * df[pRA]
        newThreshold2 = priceThreshold2 * df[pRA2]
        # This is where the high is at least p_thresh greater than the x-hr RA.
        priceSpikeMask = df["Close"] > newThreshold
        priceSpikeMask2 = df["Close"] > newThreshold2
        # priceSpikeDF = df[priceSpikeMask]
        # priceSpikeDF = priceSpikeDF[priceSpikeMask2]
        return (priceSpikeMask, priceSpikeMask2)

    def _findPriceDumps(self, df: pd.DataFrame, windowSize: int):
        """
        Finds price dumps in a given dataframe, with a certain threshold and
        window size. Requires a price rolling average column of the proper
        window size and naming convention

        :return: a (boolean_mask,dataframe) tuple
        """
        pRA = str(windowSize) + "m Close Price RA"
        pRA_plus = pRA + "+" + str(windowSize)
        df[pRA_plus] = df[pRA].shift(-windowSize)
        priceDumpMask = df[pRA_plus] <= (df[pRA] + df[pRA].std())
        priceDumpsDF = df[priceDumpMask]
        return (priceDumpMask, priceDumpsDF)

    def _findVolumeDumps(self, df: pd.DataFrame, windowSize: int):
        vRA = str(windowSize) + "m Volume RA"
        vRA_plus = vRA + "+" + str(windowSize)
        df[vRA_plus] = df[vRA].shift(-windowSize)
        priceDumpMask = df[vRA_plus] <= (df[vRA] + df[vRA].std())
        priceDumpsDF = df[priceDumpMask]
        return (priceDumpMask, priceDumpsDF)

    def _findNonVolumeSpikes(self, df: pd.DataFrame, volumeThreshold: float,
                             windowSize: int):
        # -- add rolling average column to df --
        vRA = str(windowSize) + 'm Volume RA'
        self._addRA(df, windowSize, 'Volume', vRA)

        # -- find spikes --
        volumeThreshold = volumeThreshold * df[vRA]
        # This is where the volume is at least v_thresh greater than the x-hr RA
        volumeSpikeMask = df["Volume"] <= volumeThreshold
        volumeSpikeDF = df[volumeSpikeMask]
        return (volumeSpikeMask, volumeSpikeDF)

    def _findNonPriceSpikes(self, df: pd.DataFrame, priceThreshold: float,
                            windowSize: int):
        """
        Finds price spikes in a given dataframe, with a certain threshold and
        window size.

        :return: a (boolean_mask,dataframe) tuple
        """
        # -- add rolling average column to df --
        pRA = str(windowSize) + 'm Close Price RA'
        self._addRA(df, windowSize, 'Close', pRA)

        # -- find spikes --
        newThreshold = priceThreshold * df[pRA]
        # This is where the high is at least priceThreshold greater than the
        # x-hr RA.
        priceSpikeMask = df["Close"] <= newThreshold
        priceSpikeDF = df[priceSpikeMask]
        return (priceSpikeMask, priceSpikeDF)

    def _findNonPriceDumps(self, df: pd.DataFrame, windowSize: int):
        """
        Finds price dumps in a given dataframe, with a certain threshold and
        window size. Requires a price rolling average column of the proper
        window size and naming convention :return: a (boolean_mask,
        dataframe) tuple
        """
        pRA = str(windowSize) + "m Close Price RA"
        pRA_plus = pRA + "+" + str(windowSize)
        df[pRA_plus] = df[pRA].shift(-windowSize)
        priceDumpMask = df[pRA_plus] > (df[pRA] + df[pRA].std())
        priceDumpsDF = df[priceDumpMask]
        return (priceDumpMask, priceDumpsDF)

    def _findNonVolumeDumps(self, df: pd.DataFrame, windowSize: int):
        vRA = str(windowSize) + "m Volume RA"
        vRA_plus = vRA + "+" + str(windowSize)
        df[vRA_plus] = df[vRA].shift(-windowSize)
        priceDumpMask = df[vRA_plus] > (df[vRA] + df[vRA].std())
        priceDumpsDF = df[priceDumpMask]
        return (priceDumpMask, priceDumpsDF)

    def _addRA(self, df, windowSize, col, name):
        """
        Adds a rolling average column with specified window size to a given
        dataframe and column.
        """
        df[name] = df[col].rolling(window=windowSize, min_periods=1,
                                     center=False).mean()

    def _addBackwardsRA(self, df, windowSize, col, name):
        """
        Adds a rolling average column with specified window size to a given
        dataframe and column.
        """
        df[name] = df[col].reindex(index=df[col].index[::-1])
        df[name] = df[name].rolling(window=windowSize, min_periods=1,
                                     center=False).mean()
        df[name] = df[name].reindex(index=df[name].index[::-1])

    def _plotWithPyPlot(self, df, df2, i):
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 8))
        fig.tight_layout()

        df.plot(ax=axes[0][0], x="Timestamp", y="Close", label="Close")
        df2.plot(ax=axes[0][0], x="Timestamp", y="Close", label="Close before pump", color="red")
        axes[0][0].set_title("Zoomed Out - Price Close - " + str(i + 1))

        df.plot(ax=axes[1][0], x="Timestamp", y="Volume", label="Volume")
        df2.plot(ax=axes[1][0], x="Timestamp", y="Volume", label="Volume before pump", color="red")
        axes[1][0].set_title("Zoomed Out - Volume " + str(i + 1))

        df2.plot(ax=axes[0][1], x="Timestamp", y="Close", label="Close",
                 color="red")
        axes[0][1].set_title("Zoomed In - Price Close " + str(i + 1))
        df2.plot(ax=axes[1][1], x="Timestamp", y="Volume", label="Volume",
                 color="red")
        axes[1][1].set_title("Zoomed In - Volume " + str(i + 1))

        fig.show()

    def _addRAs(self, df2, size: int):
        vRA = str(size) + "m Volume RA"
        self._addRA(df2, ROLLING_AVERAGE_SIZE, 'Volume', vRA)
        pRA = str(size) + "m Close Price RA"
        self._addRA(df2, ROLLING_AVERAGE_SIZE, 'Close', pRA)

    def _generateVolumeAndPriceData(self, volumesDf: pd.DataFrame, pricesDf: pd.DataFrame, subsectionSize: int):
        volumes = []
        prices = []
        volumeMax = volumesDf.max()
        pricesMax = pricesDf.max()
        collectiveVolume = 0.0
        collectivePrice = 0.0
        index = 0

        for item in volumesDf.iteritems():
            collectiveVolume += item[1]
            index += 1

            if index == subsectionSize:
                index = 0
                volumes.append(collectiveVolume / subsectionSize / volumeMax)
                collectiveVolume = 0.0

        index = 0

        for item in pricesDf.iteritems():
            collectivePrice += item[1]
            index += 1

            if index == subsectionSize:
                index = 0
                prices.append(collectivePrice / subsectionSize / pricesMax)
                collectivePrice = 0.0

        return volumes, prices
