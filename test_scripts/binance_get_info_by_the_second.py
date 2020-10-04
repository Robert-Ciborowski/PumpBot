from datetime import datetime, timedelta
from time import sleep

from binance.client import Client

binance_api_key = ""    #Enter your own API-key here
binance_api_secret = "" #Enter your own API-secret here

### CONSTANTS
binsizes = {"1m": 1, "5m": 5, "1h": 60, "1d": 1440}
batch_size = 750
# bitmex_client = bitmex(test=False, api_key=bitmex_api_key, api_secret=bitmex_api_secret)
client = Client(api_key=binance_api_key, api_secret=binance_api_secret)

start = datetime.now()
now = start
epoch = datetime.utcfromtimestamp(0)
interval = 3
incomingDataLimit = 5
ticker = "BTCUSDT"

# Aggregation
minuteAggregatePrice = 0.0
minuteAggregateVolume = 0.0
aggregateQuantity = 0
lastAggregateTime = now
aggregateMinuteInterval = 1

while now < start + timedelta(minutes=5):
    startTime = (now - timedelta(seconds=interval) - epoch).total_seconds() * 1000.0
    endTime = (now - epoch).total_seconds() * 1000.0
    trades = client.get_aggregate_trades(symbol=ticker, startTime=int(startTime), endTime=int(endTime), limit=incomingDataLimit)
    price = 0.0
    volume = 0.0

    for trade in trades:
        p = float(trade['p'])
        q = float(trade['q'])
        price += p
        volume += q
        minuteAggregatePrice += p
        minuteAggregateVolume += q

    price /= len(trades)
    volume /= len(trades)
    aggregateQuantity += len(trades)
    print("Price of " + ticker + " at " + str(now) + " is " + str(price) + ", volume is " + str(volume) + ".")

    if now >= lastAggregateTime + timedelta(minutes=aggregateMinuteInterval):
        print("Minute price of " + ticker + " at " + str(now) + " is " + str(
            minuteAggregatePrice / aggregateQuantity) + ", volume is " + str(minuteAggregateVolume) + ".")
        minuteAggregatePrice = 0.0
        minuteAggregateVolume = 0.0
        aggregateQuantity = 0
        lastAggregateTime = now


    sleep(interval)
    now = datetime.now()

def get_all_binance(symbol, kline_size, save = False, oldest=None):
    filename = '%s-%s-data.csv' % (symbol, kline_size)
    if os.path.isfile(filename): data_df = pd.read_csv(filename)
    else: data_df = pd.DataFrame()
    oldest_point, newest_point = minutes_of_new_data(symbol, kline_size, data_df)
    if oldest is not None:
        oldest_point = oldest
    delta_min = (newest_point - oldest_point).total_seconds()/60
    available_data = math.ceil(delta_min/binsizes[kline_size])
    if oldest_point == datetime.strptime('1 Jan 2017', '%d %b %Y'): print('Downloading all available %s data for %s. Be patient..!' % (kline_size, symbol))
    else: print('Downloading %d minutes of new data available for %s, i.e. %d instances of %s data.' % (delta_min, symbol, available_data, kline_size))
    klines = binance_client.get_historical_klines(symbol, kline_size, oldest_point.strftime("%d %b %Y %H:%M:%S"), newest_point.strftime("%d %b %Y %H:%M:%S"))
    data = pd.DataFrame(klines, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    if len(data_df) > 0:
        temp_df = pd.DataFrame(data)
        data_df = data_df.append(temp_df)
    else: data_df = data
    data_df.set_index('timestamp', inplace=True)
    if save: data_df.to_csv(filename)
    print('All caught up..!')
    return data_df
