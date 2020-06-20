from datetime import datetime

from simulator.HistoricalBinanceTradingSimulator import \
    HistoricalBinanceTradingSimulator
from util.Constants import MINUTES_OF_DATA_TO_LOOK_AT
from wallet.BinanceWallet import BinanceWallet
from wallet.SimpleWallet import SimpleWallet

if __name__ == "__main__":
    # OAXBTC
    # start = datetime(2018, 8, 17, 12, 20)
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
    # end = datetime(2020, 1, 17, 10, 0)
    # start = datetime(2020, 1, 17, 5, 0)
    # end = datetime(2020, 1, 17, 9, 30)

    # LRCBTC, YOYOBTC, FUNBTC, GASBTC, KNCBTC, STRATBTC
    start = datetime(2020, 1, 17, 0, 0)
    end = datetime(2020, 1, 18, 0, 0)

    # BQXBTC
    # start = datetime(2019, 5, 10, 11, 45)
    # end = datetime(2019, 5, 10, 15, 45)
    # start = datetime(2019, 5, 10, 5, 45)
    # end = datetime(2019, 5, 10, 15, 45)
    # wallet = BinanceWallet()
    # wallet.useBinanceKeysFromFile("../binance_properties.json")
    wallet = SimpleWallet(1.0)
    simulator = HistoricalBinanceTradingSimulator(start, end, wallet, 240, 120,
                                                  10, 40, 0.3,
                                                  fastForwardAmount=4)
    simulator.start()
