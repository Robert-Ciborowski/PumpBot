# Name: SimulatorOutputDataSetCreator
# Author: Robert Ciborowski
# Date: 04/08/2020
# Description: Creates a data set for Pump & Dumps based on the results of
#              the simulator. Uses the "simulator_trades.csv" file that the
#              simulator outputs.
import math
from math import pi
from typing import Dict, List

from stock_data import HistoricalBinanceDataObtainer
import pandas as pd
from matplotlib import pyplot as plt
import csv

from util.Constants import MINUTES_OF_DATA_TO_LOOK_AT, ROLLING_AVERAGE_SIZE


class SimulatorOutputDataSetCreator:
    dataObtainer: HistoricalBinanceDataObtainer
    numberOfSamples: int
    stockSrcs: Dict
    windowSize: int

    def __init__(self, dataObtainer: HistoricalBinanceDataObtainer):
        self.dataObtainer = dataObtainer
        self.numberOfSamples = MINUTES_OF_DATA_TO_LOOK_AT
        self.stockSrcs = {}
        self.windowSize = 24

    def trackStock(self, ticker: str, src: str):
        self.stockSrcs[ticker] = src
        df = self.dataObtainer.getHistoricalDataAsDataframe(ticker)
        pRA = str(self.windowSize) + "m Close Price RA"
        self._addRA(df, self.windowSize, "Close", pRA)
        vRA = str(self.windowSize) + 'm Volume RA'
        self._addRA(df, self.windowSize, 'Volume', vRA)

    def generateDataset(self, pumpsSrc: str, nonPumpsSrc: str):
        pumps = []
        nonPumps = []
        previous = 0.0

        for ticker, src in self.stockSrcs.items():
            with open(src, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='|')

                first = True
                for row in reader:
                    if first:
                        first = False
                        continue

                    current = float(row[3])

                    if current - previous < 0.002:
                        nonPumps.append(row)
                    else:
                        pumps.append(row)

                    previous = current

        self._writeToFile(pumps, pumpsSrc, True)
        self._writeToFile(nonPumps, nonPumpsSrc, False)

    def _writeToFile(self, pumps: List, pumpsSrc: str, areTheyPumps: bool):
        try:
            with open(pumpsSrc, 'w', newline='') as file:
                writer = csv.writer(file)
                numberOfRAs = self.numberOfSamples
                volumeList = ["Volume-RA-" + str(i) for i in range(numberOfRAs)]
                priceList = ["Price-RA-" + str(i) for i in range(numberOfRAs)]
                writer.writerow(volumeList + priceList + ["Pump"])

                for pump in pumps:
                    if pump[2] == "None":
                        continue


                    startDate = pd.to_datetime(pump[1])
                    startDate = startDate.replace(second=0, microsecond=0)
                    sellDate = pd.to_datetime(pump[2])
                    sellDate = sellDate.replace(second=0, microsecond=0)
                    # endDate = pd.to_datetime(pump[2])
                    # endDate = endDate.replace(second=0, microsecond=0)
                    # df = self.dataObtainer.getHistoricalDataAsDataframe(pump[0])
                    # mask = (df["Timestamp"] > startDate) & (
                    #             df["Timestamp"] <= endDate)
                    # df = df.loc[mask]

                    endIndex = None
                    sellIndex = None

                    try:
                        endIndex = self.dataObtainer.getHistoricalDataAsDataframe(
                            pump[0]).index.get_loc(startDate)
                        sellIndex = self.dataObtainer.getHistoricalDataAsDataframe(
                            pump[0]).index.get_loc(sellDate)
                    except:
                        print("Error with a pump!!!")
                        continue

                    startIndex = endIndex - self.numberOfSamples

                    if startIndex >= 0:
                        # std = dfToAppend.std(axis=0, skipna=True)["Close"]
                        # if std < 2.0e-08:

                        # for i in range(0, 2):
                        while endIndex < sellIndex - 20:
                            df = self.dataObtainer.getHistoricalDataAsDataframe(
                                pump[0]).iloc[startIndex:endIndex]

                            # With rolling averages
                            mean = df[str(ROLLING_AVERAGE_SIZE) + "m Volume RA"].mean()
                            std = df[str(ROLLING_AVERAGE_SIZE) + "m Volume RA"].std()
                            volumes = (df[str(
                                ROLLING_AVERAGE_SIZE) + "m Volume RA"] - mean) / std
                            mean = df[
                                str(ROLLING_AVERAGE_SIZE) + "m Close Price RA"].mean()
                            std = df[
                                str(ROLLING_AVERAGE_SIZE) + "m Close Price RA"].std()
                            prices = (df[str(
                                ROLLING_AVERAGE_SIZE) + "m Close Price RA"] - mean) / std

                            # No rolling averages
                            # mean = df["Close"].mean()
                            # std = df["Close"].std()
                            # volumes = (df["Close"] - mean) / std
                            # mean = df["Volume"].mean()
                            # std = df["Volume"].std()
                            # prices = (df["Volume"] - mean) / std

                            csvRow = []

                            # Becomes true if a value is nan so that we can skip this
                            # pump.
                            cancel = False

                            for value in volumes:
                                if math.isnan(value):
                                    cancel = True
                                    break

                                csvRow.append(value)

                            if cancel:
                                continue

                            for value in prices:
                                if math.isnan(value):
                                    cancel = True
                                    break

                                csvRow.append(value)

                            if cancel:
                                continue

                            if areTheyPumps:
                                csvRow.append(1)
                            else:
                                csvRow.append(0)

                            writer.writerow(csvRow)
                            # startIndex -= 5
                            # endIndex -= 5
                            startIndex += MINUTES_OF_DATA_TO_LOOK_AT
                            endIndex += MINUTES_OF_DATA_TO_LOOK_AT

        except IOError as e:
            print("Error writing to csv file! " + str(e))

    def _addRA(self, df, windowSize, col, name):
        """
        Adds a rolling average column with specified window size to a given
        dataframe and column.
        """
        df[name] = df[col].rolling(window=windowSize, min_periods=1,
                                     center=False).mean()
