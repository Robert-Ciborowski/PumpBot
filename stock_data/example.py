if __name__ == "__main__":
    from filter.PassThroughStockFilter import PassThroughStockFilter
    from listing_obtainers.TestObtainer import TestObtainer
    # from stock_data.CurrentStockDataObtainer import CurrentStockDataObtainer
    # from stock_data import TrackedStockDatabase
    import time
    from datetime import datetime

    from stock_data.HistoricalBinanceDataObtainer import \
        HistoricalBinanceDataObtainer

    obtainer = TestObtainer("TEST")
    historicalObtainer = HistoricalBinanceDataObtainer(
        datetime(day=14, month=7, year=2017, hour=4, minute=0), datetime(day=14, month=7, year=2017, hour=4, minute=21),
        "../binance_historical_data/")
    filter = PassThroughStockFilter(historicalObtainer)
    filter.addListings(obtainer) \
        .getDataForFiltering() \
        .filter()

    print(historicalObtainer._data)


    # tsx_obtainer = NASDAQObtainer(20)
    # filter = StockFilterByPrice(10, CurrentStockDataObtainer())
    # filter.addListings(tsx_obtainer)\
    #     .getDataForFiltering()\
    #     .filter()
    #
    # # Recommended for setSecondsBetweenStockUpdates: 60 (which is the default)
    # database = TrackedStockDatabase.getInstance()
    # database.setPricesToKeepTrackOf(7)\
    #         .setSecondsBetweenStockUpdates(30)\
    #         .useObtainer(CurrentStockDataObtainer())\
    #         .trackStocksInFilter(filter)\
    #         .startSelfUpdating()
    #
    # time.sleep(75)
    # database.stopSelfUpdating()
    # # print(database.getCurrentStock("AAB.TO"))

