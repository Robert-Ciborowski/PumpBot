import pandas as pd
from matplotlib import pyplot as plt

if __name__ == "__main__":
    pd.plotting.register_matplotlib_converters()
    df = pd.read_csv("file_name.csv")
    # print(df)
    # print(df.columns)
    # print(df[["Timestamp"]])
    # print(df[["High"]])
    # df.plot(x='Timestamp',y='High')
    # plt.plot(df[["Timestamp"]], df[["High"]], label="High")

    # df.plot(figsize=(15, 4))
    # # df.plot(subplots=True, figsize=(15, 6))
    # # df.plot(y=["R", "F10.7"], figsize=(15, 4))
    # df.plot(x="Timestamp", y=["High", "Volume"])

    # fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 8))
    # fig.tight_layout()
    # print(df)
    # print(df.index)
    # df.to_csv('file_name.csv')
    # # df2.to_csv("file_name_2.csv")
    #
    # # plt.figure()
    # # axes[0].xlabel("Timestamp")
    # # axes[0].ylabel("Value")
    # df.plot(ax=axes[0][0], x="Timestamp", y="High", label="High")
    # # axes[0][0].plot(df[["Timestamp"]], df[["High"]], label="High")
    # # axes[0][0].plot(df[["Timestamp"]], df[["High"]], label="High")
    # axes[0][0].set_title("Zoomed Out - Price High")
    # # axes[0].legend()
    # # plt.show()
    #
    # # plt.figure()
    # # axes[1].xlabel("Timestamp")
    # # axes[1].ylabel("Value")
    # df.plot(ax=axes[1][0], x="Timestamp", y="Volume", label="Volume")
    # # axes[1][0].plot(df[["Timestamp"]], df[["Volume"]], label="Volume")
    # axes[1][0].set_title("Zoomed Out - Volume")
    # # axes[1].legend()
    # # plt.show()
    #
    # fig.show()

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 8))

    # plt.figure()
    # axes[0].xlabel("Timestamp")
    # axes[0].ylabel("Value")
    df.plot(ax=axes[0][0], x="Timestamp", y="High", label="High")
    # axes[0][0].plot(df[["Timestamp"]], df[["High"]], label="High")
    # axes[0][0].plot(df[["Timestamp"]], df[["High"]], label="High")
    # df2.plot(ax=axes[0][0], x="Timestamp", y="High", color="red")
    # axes[0][0].plot(df2.iloc[0]["Timestamp"], df2.iloc[0]["High"],
    #                 marker='o', markersize=3, color="red")
    # axes[0][0].plot(df2.iloc[-1]["Timestamp"], df2.iloc[-1]["High"],
    #                 marker='o', markersize=3, color="red")
    axes[0][0].set_title("Zoomed Out - Price High")
    # axes[0].legend()
    # plt.show()

    # plt.figure()
    # axes[1].xlabel("Timestamp")
    # axes[1].ylabel("Value")
    df.plot(ax=axes[1][0], x="Timestamp", y="Volume", label="Volume")
    # axes[1][0].plot(df[["Timestamp"]], df[["Volume"]], label="Volume")
    # df2.plot(ax=axes[1][0], x="Timestamp", y="Volume", color="red")
    # axes[1][0].plot(df2.iloc[0]["Timestamp"], df2.iloc[0]["Volume"],
    #                 marker='o', markersize=3, color="red")
    # axes[1][0].plot(df2.iloc[-1]["Timestamp"], df2.iloc[-1]["Volume"],
    #                 marker='o', markersize=3, color="red")
    # axes[1][0].set_title("Zoomed Out - Volume")
    # axes[1].legend()
    # plt.show()

    fig.show()

