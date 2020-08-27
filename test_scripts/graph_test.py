
import csv
import re
from datetime import datetime
from matplotlib import pyplot as plt
import pandas as pd


def readTickerData(path: str, dateOfStart: datetime, dateOfEnd: datetime) -> pd.DataFrame:
    index = []
    entries = []
    count = 0

    try:
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                timestamp = row["timestamp"]
                times = re.split(r'[-/:\s]\s*', timestamp)

                if len(times) < 5:
                    continue

                try:
                    if "-" in timestamp:
                        timing = datetime(int(times[0]), int(times[1]),
                                          int(times[2]), int(times[3]),
                                          int(times[4]))
                    else:
                        timing = datetime(int(times[2]), int(times[1]),
                                          int(times[0]), int(times[3]),
                                          int(times[4]))
                except:
                    print("Error:")
                    print(timestamp)
                    continue
                    # time.sleep(1)

                if timing < dateOfStart:
                    continue

                if timing > dateOfEnd:
                    break

                price = float(row["open"])
                price2 = float(row["high"])
                price3 = float(row["low"])
                price4 = float(row["close"])
                volume = int(row["trades"])
                index.append(timing)
                entries.append([timing, price, price2, price3, price4, volume])
                count += 1

                if count == 10000:
                    print("Read " + path + " data up to " + str(timing))
                    count = 0

        # self.data[ticker] = df[["Volume", "Close"]]
        df = pd.DataFrame(entries, index=index,
                          columns=["Timestamp", "Open", "High", "Low", "Close",
                                   "Volume"])
        print("Done reading " + path + " historical data.")
        return df

    except IOError as e:
        print("Could not read " + path + "!")

start = datetime(2020, 2, 18, 7, 40)
end = datetime(2020, 2, 18, 8, 0)
# end = datetime(2019, 12, 31, 0, 0)
df = readTickerData("../binance_historical_data/YOYOBTC-1m-data.csv", start, end)

plt.figure()
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 8))
fig.tight_layout()
df.plot(ax=axes[0], x="Timestamp", y="High", label="High")
axes[0].set_title("Zoomed Out - Price High")
df.plot(ax=axes[1], x="Timestamp", y="Volume", label="Volume")
axes[1].set_title("Zoomed Out - Volume")
plt.show()
