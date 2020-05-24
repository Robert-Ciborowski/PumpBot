if __name__ == "__main__":
    from filter.StockFilterByPrice import StockFilterByPrice
    from listing_obtainers.NASDAQListingObtainer import NASDAQListingObtainer
    from listing_obtainers.TSXListingObtainer import TSXListingObtainer
    from listing_obtainers.TestListingObtainer import TestListingObtainer

    # tsx_obtainer = TSXListingObtainer()
    # nasdaq_obtainer = NASDAQListingObtainer()
    # filter = StockFilterByPrice(10)
    # filter.addListings(tsx_obtainer)\
    #     .addListings(nasdaq_obtainer)\
    #     .getPricesForListings()\
    #     .filterStocks()
    # filter.filtered_stocks.to_csv("filtered_stocks.csv")

    nasdaq_obtainer = NASDAQListingObtainer(20)
    filter = StockFilterByPrice(5)
    filter.addListings(nasdaq_obtainer) \
        .getDataForFiltering() \
        .filter()
    print(filter.filtered_stocks)
    # filter.filtered_stocks.to_csv("filtered_stocks_nasdaq_test.csv")

    # tsx_obtainer = TSXListingObtainer()
    # filter = StockFilterByPrice(10)
    # filter.addListings(tsx_obtainer) \
    #     .getPricesForListings() \
    #     .filterStocks()
    # filter.filtered_stocks.to_csv("filtered_stocks.csv")

    # test_obtainer = TestListingObtainer()
    # filter = StockFilterByPrice(100000)
    # filter.addListings(test_obtainer) \
    #     .getPricesForListings() \
    #     .filterStocks()

    print(filter.filtered_stocks)
