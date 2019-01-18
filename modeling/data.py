import csv
import sys
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import pathlib
from config import *

double = []
rest = []
threshhold = 5

if len(sys.argv) < 2:
    addon = ""
else:
    addon = sys.argv[2]

def plot(bins=50):
    pathlib.Path("plots"+addon+"/" + sys.argv[1]).parent.mkdir(parents=True, exist_ok=True)
    # plot specifications
    plt.xlabel("Time Difference in ms")
    # plot histogram
    plt.hist(np.log10(double), bins=bins, density=True, alpha=0.75, color="steelblue")
    plt.hist(np.log10(rest), bins=bins, density=True, alpha=0.75, color="darkorange")

    locs, labels = plt.xticks()

    locs = list(filter(lambda x: x >= 0, locs))

    plt.xticks(locs, ["$10^{:.0f}$".format(i) for i in locs])

    plt.savefig("plots"+addon+"/"+sys.argv[1][:-4]+"."+filetype, bbox_inches='tight', dpi=240,)

linecount = 0
with open(sys.argv[1], "r") as csvfile:
    datareader = csv.reader(csvfile, delimiter=',')
    for row in datareader:
        if len(row) > 100:
            linecount += 1
            data = [float(_) for _ in row]
            if any(i < threshhold for i in data):
                double.extend(filter(lambda x: x > 0, data))
            else:
                rest.extend(data)

try:
    if len(rest) > 0:
        a, b, c = stats.lognorm.fit(rest, floc=0)
        with open("results" + addon + "/pdf-params.csv", "a") as resultsout:
            resultsout.write(str(a) + "," + str(b) + "," + str(c) + "," + str(linecount) + "\n")
        d, e, f = stats.gamma.fit(rest)
        with open("results" + addon + "/gamma-pdf-params.csv", "a") as resultsout:
            resultsout.write(str(a) + "," + str(b) + "," + str(c) + "," + str(linecount) + "\n")
    if len(double) > 0:
        d, e, f = stats.lognorm.fit(double, floc=0)
        with open("results" + addon + "/pdf-params-double.csv", "a") as resultsout:
            resultsout.write(str(d) + "," + str(e) + "," + str(f) + "," + str(linecount) + "\n")
    if len(double) > 0 and len(rest) > 0:
        plot()
except ValueError as e:
    print("------------------------------------------------")
    print(str(data))
    print("FitDataError in "+sys.argv[1])
    print("------------------------------------------------")
    sys.exit()
