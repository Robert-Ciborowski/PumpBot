from data_set.BinanceDataSetCreator import BinanceDataSetCreator

if __name__ == "__main__":
    from filter.PassThroughStockFilter import PassThroughStockFilter
    from listing_obtainers.TestListingObtainer import TestListingObtainer
    from datetime import datetime
    from stock_data.HistoricalBinanceDataObtainer import \
        HistoricalBinanceDataObtainer

    # listOfStocks = ["BNBBTC", "BQXBTC", "FUNBTC", "GASBTC", "HSRBTC",
    #                 "KNCBTC",  "LRCBTC", "LTCBTC", "MCOBTC", "NEOBTC", "OAXBTC",
    #                 "OMGBTC", "QTUMBTC", "SNGLSBTC", "STRATBTC", "WTCBTC",
    #                 "YOYOBTC", "ZRXBTC"]
    # listOfStocks = ["LRCBTC", "YOYOBTC", "FUNBTC", "GASBTC", "KNCBTC", "STRATBTC"]
    # listOfStocks = ["BCCBTC"]
    # listOfStocks = ["YOYOBTC"]
    # listOfStocks = ["BCCBTC", "BQXBTC"]
    # listOfStocks = ["FUNBTC", "GASBTC", "HSRBTC",
    #                 "KNCBTC",  "LRCBTC", "LTCBTC", "MCOBTC", "NEOBTC", "OAXBTC",
    #                 "OMGBTC", "QTUMBTC", "SNGLSBTC", "STRATBTC", "WTCBTC",
    #                 "YOYOBTC", "ZRXBTC"]
    # listOfStocks = ["TRXUSDT"]
    # listOfStocks = ["SNGLSBTC"]
    listOfStocks = [
        # "TRXUSDT",
        "BTCUSDT",
        # "ETHUSDT",
        # "BNBUSDT",
        # "EOSUSDT",
        # "DOTUSDT",
        # "SUSHIUSDT",
        # "YFIIUSDT",
        # "VETUSDT",
        # "OAXBTC",
        # "YOYOBTC",
        # "SNGLSBTC",
        # "FUNBTC",
        # "GASBTC",
        # # "HSRBTC",
        # "KNCBTC",
        # "LRCBTC",
        # # "LTCBTC",
        # "MCOBTC",
        # # "NEOBTC",
        # # "OMGBTC",
        # # "QTUMBTC"
    ]
    historicalObtainer = HistoricalBinanceDataObtainer(
        # datetime(day=17, month=8, year=2018, hour=0, minute=1), datetime(day=27, month=12, year=2019, hour=0, minute=1),
        # datetime(day=17, month=8, year=2018, hour=0, minute=1), datetime(day=31, month=8, year=2018, hour=0, minute=1),
        # datetime(day=31, month=8, year=2018, hour=0, minute=1), datetime(day=30, month=9, year=2018, hour=0, minute=1),
        # datetime(day=27, month=12, year=2019, hour=0, minute=1), datetime(day=27, month=2, year=2020, hour=0, minute=1),
        # datetime(day=10, month=1, year=2020, hour=0, minute=0),
        # datetime(day=30, month=1, year=2020, hour=0, minute=0),
        # datetime(day=1, month=1, year=2018, hour=0, minute=0),
        # datetime(day=1, month=9, year=2019, hour=0, minute=0),
        # datetime(day=1, month=1, year=2018, hour=0, minute=0),
        # datetime(day=20, month=3, year=2018, hour=0, minute=0),
        datetime(day=18, month=8, year=2017, hour=0, minute=0),
        datetime(day=20, month=4, year=2020, hour=0, minute=0),
        "../binance_historical_data/")
    print("Reading historical stock data...")
    historicalObtainer.trackStocks(listOfStocks)
    # set timeInterval to 60 when creating actual dataset!
    # dataSetCreator = BinanceDataSetCreator(historicalObtainer, pumpSpike=0.03, pumpDrop=0.03, timeIntervalForNonPumps=60)
    dataSetCreator = BinanceDataSetCreator(historicalObtainer, pumpSpike=0.01, pumpDrop=0.01, timeIntervalForNonPumps=3000)
    print("Analyzing historical stock data for pumps...")
    pumps, rightBeforePumps = dataSetCreator.findPumpsForSymbols(listOfStocks,
                                                                 1440)
    pumps2, rightBeforePumps2 = dataSetCreator.findNonPumpsForSymbols(
        listOfStocks, 6000)
    rightBeforePumps, extraNonPumpsToAdd = dataSetCreator.createFinalPumpsDataSet(pumps, rightBeforePumps)
    print(rightBeforePumps2[0].columns)
    dataSetCreator.exportPumpsToCSV("final-dataset", rightBeforePumps)
    rightBeforePumps2 = dataSetCreator.createFinalNonPumpsDataSet(pumps2, rightBeforePumps2)
    rightBeforePumps2.extend(extraNonPumpsToAdd)
    dataSetCreator.exportPumpsToCSV("final-dataset", rightBeforePumps2, areTheyPumps=False)
