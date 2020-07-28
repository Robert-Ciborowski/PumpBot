
import csv
import re
from datetime import datetime
from matplotlib import pyplot as plt
import pandas as pd

df = pd.read_csv("simulator_trades.csv")

plt.figure()
df.plot(x="sell", y="profit", label="Profit", figsize=(21, 9))
locs, labels = plt.xticks()
plt.setp(labels, rotation=90)
plt.show()
