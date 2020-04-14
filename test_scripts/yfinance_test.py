"""
Example of how to use the yfinance library.
"""


import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# data = yf.download(tickers="BA", period="1m", interval="1m")
# print(data.info())
# print(data.iloc[-1]["Close"])
# ba = yf.Ticker("BA")
# print(ba.info)


# data2 = yf.download("SPY AAPL", start="2017-01-01", end="2017-04-30")
#
# print("MSFT:")
# msft = yf.Ticker("MSFT")
# print(msft.info)
#
# print("Data2:")
# print(type(data2))
# print(data2)
# print("End of data2")

data2 = yf.download("VNP.TO", start="2020-04-09", end="2020-04-12")
print(data2)

# Getting the last known price of a list of stocks!
data2 = yf.download("AACG AAL AAME AAOI AAON AAPL AAWW AAXJ AAXN ABCB ABEO ABIO ABMD ABTX ABUS ACAD ACAM ACAMU ACAMW ACBI", period="3d", interval="1m")
# print(data2)
# data2.to_csv('test_data.csv')
# print(data2.columns)
# print(type(range(20, len(data2.columns))))

data2 = data2.iloc[:,0:20]
print(data2)

data = {
    "Ticker": [],
    "Price": []
}

for i in range(0, len(data2.columns)):
    # printing a third element of column
    # print("------------------------------------------------")
    # # print(i)
    s = data2.iloc[:,i]
    # print(data2.columns[i][1])
    # # print(s)
    # # print(s.index)
    # print(s.last_valid_index())
    # print(s.index.get_loc(s.last_valid_index()))
    data["Ticker"].append(data2.columns[i][1])
    val_index = s.last_valid_index()
    data["Price"].append(s[val_index])
    # print(data2.iloc[:,0].last_valid_index())

df = pd.DataFrame(data, columns=["Ticker", "Price"])
print(df)

# data2.drop(data2.columns[ [ tuple(range(20, len(data2.columns))) ] ], axis = 1, inplace = True)
# print(data2.columns)

# data3 = yf.download(  # or pdr.get_data_yahoo(...
#         # tickers list or string as well
#         tickers = "SPY AAPL MSFT",
#
#         # use "period" instead of start/end
#         # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
#         # (optional, default is '1mo')
#         period = "1d",
#
#         # fetch data by interval (including intraday if period < 60 days)
#         # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
#         # (optional, default is '1d')
#         interval = "1m",
#
#         # group by ticker (to access via data['SPY'])
#         # (optional, default is 'column')
#         group_by = 'ticker',
#
#         # adjust all OHLC automatically
#         # (optional, default is False)
#         auto_adjust = True,
#
#         # download pre/post regular market hours data
#         # (optional, default is False)
#         prepost = True,
#
#         # use threads for mass downloading? (True/False/Integer)
#         # (optional, default is True)
#         threads = True,
#
#         # proxy URL scheme use use when downloading?
#         # (optional, default is None)
#         proxy = None
#     )
# data2.Close.plot()
# plt.show()
# data3["SPY"].Close.plot()
# data3["AAPL"].Close.plot()
# data3["MSFT"].Close.plot()
# plt.show()
