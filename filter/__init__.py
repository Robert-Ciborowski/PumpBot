from filter.StockFilterByPrice import StockFilterByPrice
from listing_obtainers.NASDAQObtainer import NASDAQObtainer
from listing_obtainers.TSXObtainer import TSXObtainer
from listing_obtainers.TestObtainer import TestObtainer

if __name__ == "__main__":
    # tsx_obtainer = TSXObtainer()
    # nasdaq_obtainer = NASDAQObtainer()
    # filter = StockFilterByPrice(10)
    # filter.addListings(tsx_obtainer)\
    #     .addListings(nasdaq_obtainer)\
    #     .getPricesForListings()\
    #     .filterStocks()
    # filter.filtered_stocks.to_csv("filtered_stocks.csv")

    nasdaq_obtainer = NASDAQObtainer(20)
    filter = StockFilterByPrice(5)
    filter.addListings(nasdaq_obtainer) \
        .getPricesForListings() \
        .filterStocks()
    print(filter.filtered_stocks)
    # filter.filtered_stocks.to_csv("filtered_stocks_nasdaq_test.csv")

    # tsx_obtainer = TSXObtainer()
    # filter = StockFilterByPrice(10)
    # filter.addListings(tsx_obtainer) \
    #     .getPricesForListings() \
    #     .filterStocks()
    # filter.filtered_stocks.to_csv("filtered_stocks.csv")

    # test_obtainer = TestObtainer()
    # filter = StockFilterByPrice(100000)
    # filter.addListings(test_obtainer) \
    #     .getPricesForListings() \
    #     .filterStocks()

    print(filter.filtered_stocks)
