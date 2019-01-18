import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pathlib
from config import *

if len(sys.argv) < 2:
    addon = ""
else:
    addon = sys.argv[1]

prefix = "results"+addon+"/"

filename = "pdf-params.csv"


def readdata(folder):
    every = 1000
    c = 0
    fdata = []
    with open(folder + "/all-data.csv", "r") as csvfile:
        datareader = csv.reader(csvfile, delimiter=',')
        for row in datareader:
            if len(row) > 1:
                c += 1
                if c % every == 0:
                    data = [int(_) for _ in row]
                    fdata.extend(list(filter(lambda y: y > 0, data)))
                    c = 0
    return fdata



def normplot(maindata1, maindata2, maindata3):
    print("Normplot start.")
    plt.xlabel("Time Difference in ms (Log scale)")
    plt.ylabel("Quantiles of the Distribution")
    # Calculate quantiles and least-square-fit curve
    (quantiles, values), (slope, intercept, r) = stats.probplot(maindata1, dist='norm')
    (quantiles2, valid2), (_, _, _) = stats.probplot(maindata2, dist='norm')
    (quantiles3, valid3), (_, _, _) = stats.probplot(maindata3, dist='norm')
    print("Least square fit curve and quantiles done.")

    # plot results
    plt.plot(values, quantiles, color='#003c9e', marker='o', label="Great Britain Data")
    plt.plot(valid3, quantiles3, color='#177244', marker='o', label="South East Asia Data")
    plt.plot(valid2, quantiles2, color='#EF4F00', marker='o', label="USA Data")
    plt.plot(quantiles * slope + intercept, quantiles, '#003c9e', label="Linear Fit Great Britain")
    print("Plotting done.")

    # define ticks
    ticks_perc = [1, 5, 10, 20, 50, 80, 90, 95, 99]

    # transfrom them from precentile to cumulative density
    ticks_quan = [stats.norm.ppf(i / 100.) for i in ticks_perc]

    # assign new ticks
    plt.yticks(ticks_quan, ticks_perc)
    locs, labels = plt.xticks()

    locs = list(filter(lambda x: x >= 0, locs))

    plt.xticks(locs, ["$10^{:.0f}$".format(i) for i in locs])
    print("Ticks done.")

    # show plot
    plt.grid()
    plt.legend()
    plt.savefig("normplot.png", bbox_inches='tight', dpi=dpi)
    plt.clf()


def normplot2(maindata1, maindata2):
    print("Normplot start.")
    plt.xlabel("Time Difference in ms (Log scale)")
    plt.ylabel("Quantiles of the Distribution")
    # Calculate quantiles and least-square-fit curve
    (quantiles, values), (slope, intercept, r) = stats.probplot(maindata1, dist='norm')
    (quantiles2, valid2), (_, _, _) = stats.probplot(maindata2, dist='norm')
    print("Least square fit curve and quantiles done.")

    # plot results
    plt.plot(values, quantiles, color='#003c9e', marker='o', label="Great Britain 2 Data")
    plt.plot(valid2, quantiles2, color='#EF4F00', marker='o', label="Great Britain 1 Data")
    plt.plot(quantiles * slope + intercept, quantiles, '#003c9e', label="Linear Fit Great Britain 2")
    print("Plotting done.")

    # define ticks
    ticks_perc = [1, 5, 10, 20, 50, 80, 90, 95, 99]

    # transfrom them from precentile to cumulative density
    ticks_quan = [stats.norm.ppf(i / 100.) for i in ticks_perc]

    # assign new ticks
    plt.yticks(ticks_quan, ticks_perc)
    locs, labels = plt.xticks()

    locs = list(filter(lambda x: x >= 0, locs))

    plt.xticks(locs, ["$10^{:.0f}$".format(i) for i in locs])
    print("Ticks done.")

    # show plot
    plt.grid()
    plt.legend()
    plt.savefig("normplot2.png", bbox_inches='tight', dpi=dpi)
    plt.clf()


usa = np.log10(readdata("resultsUSA"))
gbs = np.log10(readdata("resultsGBS"))
sea = np.log10(readdata("resultsSEA"))
uks = np.log10(readdata("resultsUKS"))

normplot(gbs, usa, sea)
normplot2(gbs, uks)