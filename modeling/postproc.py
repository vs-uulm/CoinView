import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

filetype = "png"
dpi = 300

if len(sys.argv) < 2:
    addon = ""
else:
    addon = sys.argv[1]

bins = 500

def loghist(fulldata, name):
    ## distribution of log
    print("Log histogram plot.")
    plt.xlabel("Time Difference in ms (Log scale)")

    plt.hist(np.log10(fulldata), bins, density=1, histtype='bar')

    locs, labels = plt.xticks()

    locs = list(filter(lambda x: x >= 0, locs))

    plt.xticks(locs, ["$10^{:.0f}$".format(i) for i in locs])

    plt.savefig(addon + "-" + name + "-log." + filetype, bbox_inches='tight', dpi=dpi)
    plt.clf()

def histhist(fulldata, name):
    ## distribution of log
    print("Histogram plot.")
    plt.xlabel("Time Difference in ms")

    iqr = stats.iqr(fulldata)

    a, b, c = stats.lognorm.fit(fulldata)
    pa, ploc, pscale = stats.powerlaw.fit(fulldata)
    ga, gb, gc = stats.gamma.fit(fulldata)
    print("Fitting done.")

    x = np.linspace(0, 3*iqr)
    pdf = stats.lognorm.pdf(x, a, scale=c)

    plt.hist(fulldata, bins, range=(0, 3*iqr), density=1, histtype='bar')

    plt.plot(x, pdf, color="darkorange", label="Lognormal")

    pldf = stats.powerlaw.pdf(x, pa, loc=ploc, scale=pscale)
    plt.plot(x, pldf, color="green", label="power law")

    gpdf = stats.gamma.pdf(x, ga, gb, gc)
    plt.plot(x, gpdf, color="red", label="Gamma")

    plt.legend()
    plt.savefig(addon + "-" + name + "." + filetype, bbox_inches='tight', dpi=dpi)
    plt.clf()

print("Min data input.")
fulldata = []
with open(addon+"/min_peer.csv", "r") as csvfile:
    datareader = csv.reader(csvfile, delimiter=',')
    for row in datareader:
        if len(row) > 1:
            data = [int(_) for _ in row]
            fulldata.extend(list(filter(lambda y: y > 0, data)))
print("Amount of data points: "+str(len(fulldata)))
try:
    loghist(fulldata, "min")
except:
    print("Loghist failed.")
try:
    histhist(fulldata, "min")
except:
    print("Histhist failed.")

print("Peer data input.")
fulldata = []
with open(addon+"/all_peer.csv", "r") as csvfile:
    datareader = csv.reader(csvfile, delimiter=',')
    for row in datareader:
        if len(row) > 1:
            data = [int(_) for _ in row]
            fulldata.extend(list(filter(lambda y: y > 0, data)))
print("Amount of data points: "+str(len(fulldata)))

try:
    loghist(fulldata, "all")
except:
    print("Loghist failed.")
try:
    histhist(fulldata, "all")
except:
    print("Histhist failed.")
