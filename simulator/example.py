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
    # start = datetime(2020, 1, 10, 18, 0)
    # end = datetime(2020, 1, 11, 0, 0)
    # start = datetime(2020, 1, 9, 12, 0)
    # end = datetime(2020, 1, 15, 0, 0)
    # start = datetime(2020, 1, 10, 0, 0)
    # end = datetime(2020, 1, 15, 0, 0)

    # LRCBTC, YOYOBTC
    # start = datetime(2020, 1, 17, 5, 0)
    # end = datetime(2020, 1, 17, 20, 0)
    # start = datetime(2020, 1, 17, 5, 0)
    # end = datetime(2020, 1, 17, 11, 0)

    # LRCBTC, YOYOBTC, FUNBTC, GASBTC, KNCBTC, STRATBTC
    start = datetime(2020, 1, 17, 0, 0)
    end = datetime(2020, 1, 19, 0, 0)

    # BQXBTC
    # start = datetime(2019, 5, 10, 11, 45)
    # end = datetime(2019, 5, 10, 15, 45)
    # start = datetime(2019, 5, 10, 5, 45)
    # end = datetime(2019, 5, 10, 15, 45)
    simulator = HistoricalBinanceTradingSimulator(start, end, 240, 120, 10, 1.0,
                                                  0.3, fastForwardAmount=4)
    simulator.start()
