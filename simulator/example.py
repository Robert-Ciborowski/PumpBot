from datetime import datetime

from simulator.HistoricalBinanceTradingSimulator import \
    HistoricalBinanceTradingSimulator
from util.Constants import MINUTES_OF_DATA_TO_LOOK_AT

if __name__ == "__main__":
    # OAXBTC
    # start = datetime(2018, 8, 17, 15, 20)
    # end = datetime(2018, 8, 17, 16, 15)
    # start = datetime(2018, 9, 16, 21, 20)
    # end = datetime(2018, 9, 21, 0, 15)
    # start = datetime(2020, 1, 10, 0, 0)
    # end = datetime(2020, 1, 11, 5, 0)
    start = datetime(2020, 1, 10, 18, 0)
    end = datetime(2020, 1, 11, 0, 0)

    # BQXBTC
    # start = datetime(2019, 5, 10, 11, 45)
    # end = datetime(2019, 5, 10, 15, 45)
    # start = datetime(2019, 5, 10, 5, 45)
    # end = datetime(2019, 5, 10, 15, 45)
    simulator = HistoricalBinanceTradingSimulator(start, end, 7, 30, 1.0, 0.3,
                                                  fastForwardAmount=24)
    simulator.start()
