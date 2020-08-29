
import csv
import re
from datetime import datetime
from matplotlib import pyplot as plt
import pandas as pd
import os

from stock_data.HistoricalBinanceDataObtainer import \
    HistoricalBinanceDataObtainer
from util.Constants import SAMPLES_OF_DATA_TO_LOOK_AT, ROLLING_AVERAGE_SIZE

def start(plotIndividual: bool, plotMain: bool, profitThreshold=0.0):
    currentDate = str(datetime.now().replace(microsecond=0)).replace(":", "-")
    os.mkdir("simulator_figures/" + currentDate)

    start = datetime(2018, 1, 1, 0, 0)
    end = datetime(2020, 8, 2, 0, 0)

    dataObtainer = HistoricalBinanceDataObtainer(start, end, "binance_historical_data/")
    dataObtainer.trackStocks(["YOYOBTC"])

    df = pd.read_csv("simulator_trades.csv")

    if plotIndividual:
        previousProfit = 0.0

        for index, row in df.iterrows():
            print("Individual: " + str(index))
            if row["sell"] == "None":
                continue

            currentProfit = float(row["profit"])
            difference = currentProfit - previousProfit
            previousProfit = currentProfit

            if difference > 0:
                profitText = "profitable"
            else:
                profitText = "unprofitable"

            buy = pd.to_datetime(row["buy"])
            buy = buy.replace(second=0, microsecond=0)
            start = buy - pd.Timedelta(minutes=SAMPLES_OF_DATA_TO_LOOK_AT)
            sell = pd.to_datetime(row["sell"])
            sell = sell.replace(second=0, microsecond=0)
            df2 = dataObtainer.getHistoricalDataAsDataframe(row["ticker"])[start : sell]

            fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(15, 10))
            fig.tight_layout()

            df2.plot(ax=axes[0], x="Timestamp", y="High", label="High")
            df2[start : buy].plot(ax=axes[0], x="Timestamp", y="High",
                                  label="High before pump", color="red")
            axes[0].set_title("Price High - " + row["ticker"] + " - " +
                              str(difference) + " - mean: " +
                              str(df2["High"].mean()) + " - std: " +
                              str(df2["High"].std()))

            df2.plot(ax=axes[1], x="Timestamp", y="Volume", label="Volume")
            df2[start: buy].plot(ax=axes[1], x="Timestamp", y="Volume",
                                 label="Volume before pump", color="red")
            axes[1].set_title("Volume - " + row["ticker"] + " - " +
                              str(difference) + " - mean: " +
                              str(df2["Volume"].mean()) + " - std: " +
                              str(df2["Volume"].std()))

            fig.savefig("simulator_figures/" + currentDate + "/" + profitText + " - " + row["ticker"] + "-" + str(index) + ".png")
            plt.close()

        print("Finished individual graphs.")

    if plotMain:
        previousProfit = 0.0

        mainFig, mainAxes = plt.subplots(nrows=4, ncols=1, figsize=(15, 10))
        mainFig.tight_layout()
        mainAxes[0].set_title("Profitable Highs")
        mainAxes[1].set_title("Profitable Volumes")
        mainAxes[2].set_title("Unprofitable Highs")
        mainAxes[3].set_title("Unprofitable Volumes")

        for index, row in df.iterrows():
            print("Total: " + str(index))
            if row["sell"] == "None":
                continue

            currentProfit = float(row["profit"])
            difference = currentProfit - previousProfit
            previousProfit = currentProfit

            buy = pd.to_datetime(row["buy"])
            buy = buy.replace(second=0, microsecond=0)
            start = buy - pd.Timedelta(minutes=SAMPLES_OF_DATA_TO_LOOK_AT)
            # sell = pd.to_datetime(row["sell"])
            # sell = sell.replace(second=0, microsecond=0)
            df2 = dataObtainer.getHistoricalDataAsDataframe(row["ticker"])[start: buy]

            mean = df2["High"].mean()
            std = df2["High"].std()
            prices = (df2["High"] - mean) / mean
            prices = prices.reset_index(drop=True)
            mean = df2["Volume"].mean()
            std = df2["Volume"].std()
            volumes = (df2["Volume"] - mean) / mean
            volumes = volumes.reset_index(drop=True)

            if difference >= profitThreshold:
                prices.plot(ax=mainAxes[0], x="Time", y="High", label="High")
                volumes.plot(ax=mainAxes[1], x="Timestamp", y="Volume", label="Volume")
            else:
                prices.plot(ax=mainAxes[2], x="Time", y="High", label="High")
                volumes.plot(ax=mainAxes[3], x="Timestamp", y="Volume", label="Volume")


        mainFig.savefig("simulator_figures/" + currentDate + "/main.png")
        plt.close()

start(True, True, 0.02)
print("Done!")
