from datetime import datetime

from data_set.SimulatorOutputDataSetCreator import SimulatorOutputDataSetCreator
from stock_data.HistoricalBinanceDataObtainer import \
    HistoricalBinanceDataObtainer

if __name__ == "__main__":
    listOfStocks = ["YOYOBTC"]
    historicalObtainer = HistoricalBinanceDataObtainer(
        datetime(day=1, month=1, year=2018, hour=0, minute=0),
        datetime(day=1, month=2, year=2020, hour=0, minute=0),
        "../binance_historical_data/")
    print("Reading historical stock data...")
    historicalObtainer.trackStocks(listOfStocks)

    creator = SimulatorOutputDataSetCreator(historicalObtainer)
    creator.trackStock("YOYOBTC", "../simulator_trades.csv")
    creator.generateDataset("final-dataset-2-pumps.csv", "final-dataset-2-non-pumps.csv")
    print("Done!")
