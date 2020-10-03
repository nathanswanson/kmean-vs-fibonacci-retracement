import pytz
from matplotlib import pyplot as plt
import yfinance as yf
import numpy as np
from sklearn.cluster import KMeans


def __main__():
    symbol = "tgt"
    start = "2019-01-02"
    end = "2019-06-02"
    ticker = yf.Ticker(symbol)
    data = ticker.history(start=start, end=end, interval="1d", prepost=False, actions=False)
    data["Time"] = [d.timestamp() for d in data.index]
    data = data[["Time", "Open", "High", "Low", "Close", "Volume"]]

    plt.plot(data["Open"], 'g')
    max = data["Open"].max()
    min = data["Open"].min()
    fibvalues = [min, ((max - min) * .236) + min, ((max - min) * .382) + min, ((max - min) * .5) + min,
                 ((max - min) * .618) + min, ((max - min) * .786) + min, max]
    for i in range(len(fibvalues)):
        plt.axhline(fibvalues[i], c='k')

    plt.axhline((max + min) / 2, c='k')

    print(
        "I estimate that the stock will rally to " + str(
            ((max - min) * 1.618) + min) + " facing resistance at this value. " \
                                           "after hitting a support level the " \
                                           "stock would reach " + str(
            ((max - min) *
             2.618) + min))
    X = data["Open"].to_numpy()

    kmeans = KMeans(n_clusters=4).fit(X.reshape(-1, 1))
    c = kmeans.predict(X.reshape(-1, 1))
    minmax = []
    for i in range(4):
        minmax.append([-np.inf, np.inf])
    for i in range(len(X)):
        cluster = c[i]
        if X[i] > minmax[cluster][0]:
            minmax[cluster][0] = X[i]
        if X[i] < minmax[cluster][1]:
            minmax[cluster][1] = X[i]

    np_minmax = np.asarray(minmax)
    np_minmax = np.delete(np_minmax, 0)
    np_minmax = np.sort(np_minmax)

    np_minmax = np_minmax.tolist()

    maxarray = np.maximum(np_minmax, fibvalues)
    minarray = np.minimum(np_minmax, fibvalues)
    res = [i / j for i, j in zip(minarray, maxarray)]
    print()
    print("I am " + str(int(average(res) * 100)) + "% sure that fibonachi is accurate using k means clustering ")
    for i in range(len(minmax)):
        plt.axhline(minmax[i][0], c='b')

    plt.tick_params(axis="both", which="both", bottom="off", top="off",
                    labelbottom="on", left="off", right="off", labelleft="on")
    plt.show()


def average(lst):
    return sum(lst) / len(lst)


__main__()
