
import csv
import re
from datetime import datetime
from matplotlib import pyplot as plt
import pandas as pd
import os

from util.Constants import GROUPED_DATA_SIZE, MINUTES_OF_DATA_TO_LOOK_AT, \
    MINUTES_OF_DATA_TO_LOOK_AT, \
    ROLLING_AVERAGE_SIZE

def start(plotIndividual: bool, plotMain: bool, pumpSrc: str, nonPumpSrc: str):
    currentDate = str(datetime.now().replace(microsecond=0)).replace(":", "-")
    os.mkdir("dataset_figures/" + currentDate)

    pumps = pd.read_csv(pumpSrc)
    nonPumps = pd.read_csv(nonPumpSrc)

    if plotIndividual:
        for index, row in pumps.iterrows():
            print("Individual pump: " + str(index))
            volumes = []
            prices = []
            xAxis = range(0, int(MINUTES_OF_DATA_TO_LOOK_AT / GROUPED_DATA_SIZE))

            for i in range(0, int(MINUTES_OF_DATA_TO_LOOK_AT / GROUPED_DATA_SIZE)):
                volumes.append(float(row["Volume-RA-" + str(i)]))

            for i in range(0, int(MINUTES_OF_DATA_TO_LOOK_AT / GROUPED_DATA_SIZE)):
                prices.append(float(row["Price-RA-" + str(i)]))

            fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(15, 10))
            fig.tight_layout()

            axes[0].plot(xAxis, prices, label="High")
            axes[1].plot(xAxis, volumes, label="Volumes")

            axes[0].set_title("Price")
            axes[1].set_title("Volumes")

            fig.savefig("dataset_figures/" + currentDate + "/" + "pumps-" + str(index) + ".png")
            plt.close()

        for index, row in nonPumps.iterrows():
            print("Individual pumps: " + str(index))
            volumes = []
            prices = []
            xAxis = range(0, int(MINUTES_OF_DATA_TO_LOOK_AT / GROUPED_DATA_SIZE))

            for i in range(0, int(MINUTES_OF_DATA_TO_LOOK_AT / GROUPED_DATA_SIZE)):
                volumes.append(float(row["Volume-RA-" + str(i)]))

            for i in range(0, int(MINUTES_OF_DATA_TO_LOOK_AT / GROUPED_DATA_SIZE)):
                prices.append(float(row["Price-RA-" + str(i)]))

            fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(15, 10))
            fig.tight_layout()

            axes[0].plot(xAxis, prices, label="High")
            axes[1].plot(xAxis, volumes, label="Volumes")

            axes[0].set_title("Price")
            axes[1].set_title("Volumes")

            fig.savefig("dataset_figures/" + currentDate + "/" + "nonpumps-" + str(index) + ".png")
            plt.close()

        print("Finished individual graphs.")

    if plotMain:
        mainFig, mainAxes = plt.subplots(nrows=4, ncols=1, figsize=(15, 10))
        mainFig.tight_layout()
        mainAxes[0].set_title("Pump Highs")
        mainAxes[1].set_title("Pump Volumes")
        mainAxes[2].set_title("Nonpump Highs")
        mainAxes[3].set_title("Nonpump Volumes")

        xAxis = range(0, MINUTES_OF_DATA_TO_LOOK_AT // GROUPED_DATA_SIZE + MINUTES_OF_DATA_TO_LOOK_AT // GROUPED_DATA_SIZE // 2 + MINUTES_OF_DATA_TO_LOOK_AT // GROUPED_DATA_SIZE // 3)

        for index, row in pumps.iterrows():
            print("Total: " + str(index))

            volumes = []
            prices = []

            for i in range(0, int(MINUTES_OF_DATA_TO_LOOK_AT / GROUPED_DATA_SIZE)):
                volumes.append(float(row["Volume-RA-" + str(i)]))

            for i in range(0, int(MINUTES_OF_DATA_TO_LOOK_AT / GROUPED_DATA_SIZE)):
                prices.append(float(row["Price-RA-" + str(i)]))

            for i in range(0, int(
                    MINUTES_OF_DATA_TO_LOOK_AT / GROUPED_DATA_SIZE / 2)):
                volumes.append(float(row["Volume-RA2-" + str(i)]))

            for i in range(0, int(
                    MINUTES_OF_DATA_TO_LOOK_AT / GROUPED_DATA_SIZE / 2)):
                prices.append(float(row["Price-RA2-" + str(i)]))

            for i in range(0, int(MINUTES_OF_DATA_TO_LOOK_AT / GROUPED_DATA_SIZE / 3)):
                volumes.append(float(row["Volume-RA3-" + str(i)]))

            for i in range(0, int(MINUTES_OF_DATA_TO_LOOK_AT / GROUPED_DATA_SIZE / 3)):
                prices.append(float(row["Price-RA3-" + str(i)]))

            mainAxes[0].plot(xAxis, prices, label="High")
            mainAxes[1].plot(xAxis, volumes, label="Volumes")

        for index, row in nonPumps.iterrows():
            print("Total: " + str(index))

            volumes = []
            prices = []

            for i in range(0, int(MINUTES_OF_DATA_TO_LOOK_AT / GROUPED_DATA_SIZE)):
                volumes.append(float(row["Volume-RA-" + str(i)]))

            for i in range(0, int(MINUTES_OF_DATA_TO_LOOK_AT / GROUPED_DATA_SIZE)):
                prices.append(float(row["Price-RA-" + str(i)]))

            for i in range(0, int(MINUTES_OF_DATA_TO_LOOK_AT / GROUPED_DATA_SIZE / 2)):
                volumes.append(float(row["Volume-RA2-" + str(i)]))

            for i in range(0, int(MINUTES_OF_DATA_TO_LOOK_AT / GROUPED_DATA_SIZE / 2)):
                prices.append(float(row["Price-RA2-" + str(i)]))

            for i in range(0, int(MINUTES_OF_DATA_TO_LOOK_AT / GROUPED_DATA_SIZE / 3)):
                volumes.append(float(row["Volume-RA3-" + str(i)]))

            for i in range(0, int(MINUTES_OF_DATA_TO_LOOK_AT / GROUPED_DATA_SIZE / 3)):
                prices.append(float(row["Price-RA3-" + str(i)]))

            mainAxes[2].plot(xAxis, prices, label="High")
            mainAxes[3].plot(xAxis, volumes, label="Volumes")


        mainFig.savefig("dataset_figures/" + currentDate + "/main.png")
        plt.close()

start(False, True, "final-dataset-pumps.csv", "final-dataset-non-pumps.csv")
print("Done!")
