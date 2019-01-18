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
plotsfix = "plots"+addon+"/"

filename = "pdf-params.csv"

pathlib.Path(plotsfix + filename).parent.mkdir(parents=True, exist_ok=True)

bins = 50

def pandcdf(fulldata, includeFullPDF = False):
    pdfs = []
    linecounts = []
    print("Read pdfs")
    with open(prefix + "pdf-params.csv", "r") as pdffile:
        datareader = csv.reader(pdffile, delimiter=',')
        for row in datareader:
            linecounts.append(int(row[3]))
            pdfs.append((float(row[0]), float(row[1]), float(row[2])))

    lc2 = []
    gpdfs = []
    with open(prefix + "gamma-pdf-params.csv", "r") as pdffile:
        datareader = csv.reader(pdffile, delimiter=',')
        for row in datareader:
            lc2.append(int(row[3]))
            gpdfs.append((float(row[0]), float(row[1]), float(row[2])))

    x = np.linspace(0, 100000, 5000)

    ## PDF Plot
    def pdfplot(pdfs, linecounts, name):
        import heapq
        largest10 = heapq.nlargest(10, zip(linecounts, pdfs), lambda x: x[0])
        _, toppdfs = zip(*largest10)

        print("PDF Plot start.")
        plt.xlabel("Time Difference in ms")
        for sigma, loc, scale in pdfs:
            pdf = stats.lognorm.pdf(x, sigma, scale=scale)
            plt.plot(x, pdf, color="grey")

        for sigma, loc, scale in toppdfs:
            pdf = stats.lognorm.pdf(x, sigma, scale=scale)
            plt.plot(x, pdf, color="blue")

        if includeFullPDF:
            print("Actual pdf plot.")
            sigma, loc, scale = stats.lognorm.fit(fulldata, floc=0)
            pdf = stats.lognorm.pdf(x, sigma, scale=scale)
            plt.plot(x, pdf, color="darkorange")

        plt.savefig(plotsfix + "pdf-summary-" + name + "." + filetype, bbox_inches='tight', dpi=dpi)
        plt.clf()
        return toppdfs

    toppdfs = pdfplot(pdfs, linecounts, "lognormal")
    pdfplot(gpdfs, lc2, "gamma")

    ## CDF Plot
    print("CDF Plot start.")
    plt.xlabel("Time Difference in ms")
    for sigma, loc, scale in pdfs:
        cdf = stats.lognorm.cdf(x, sigma, scale=scale)
        plt.plot(x, cdf, color="grey")

    for sigma, loc, scale in toppdfs:
        cdf = stats.lognorm.cdf(x, sigma, scale=scale)
        plt.plot(x, cdf, color="blue")

    cdf = stats.lognorm.cdf(x, sigma, scale=scale)
    plt.plot(x, cdf, color="darkorange")

    plt.savefig(plotsfix + "cdf-summary." + filetype, bbox_inches='tight', dpi=dpi)
    plt.clf()
    del pdfs

def powerlaw(logall):
    ## PowerLaw Test
    print("Powerlaw plot.")
    plt.xlabel("Time Difference in ms (Log scale)")

    plt.hist(logall, bins, density=1, histtype='step', cumulative=-1, log=True)

    locs, labels = plt.xticks()

    locs = list(filter(lambda y: y >= 0, locs))

    plt.xticks(locs, ["$10^{:.0f}$".format(i) for i in locs])

    plt.savefig(plotsfix + "cdf-powerlaw." + filetype, bbox_inches='tight', dpi=dpi)
    plt.clf()

def exptest(fulldata):
    ## Exp Test
    print("Exp plot.")
    plt.xlabel("Time Difference in ms (Log scale)")

    plt.hist(fulldata, bins, density=1, histtype='step', cumulative=-1, log=True)

    locs, labels = plt.xticks()
    locs = list(filter(lambda y: y >= 0, locs))
    plt.xticks(locs, ["$10^{:.0f}$".format(i) for i in locs])

    plt.savefig(plotsfix + "cdf-exptest." + filetype, bbox_inches='tight', dpi=dpi)
    plt.clf()

def loghist(fulldata):
    ## distribution of log
    print("Log histogram plot.")
    plt.xlabel("Time Difference in ms (Log scale)")

    plt.hist(np.log10(fulldata), bins, density=1, histtype='bar')

    locs, labels = plt.xticks()

    locs = list(filter(lambda x: x >= 0, locs))

    plt.xticks(locs, ["$10^{:.0f}$".format(i) for i in locs])

    plt.savefig(plotsfix + "distribution-log." + filetype, bbox_inches='tight', dpi=dpi)
    plt.clf()

def histhist(fulldata):
    ## distribution of log
    print("Histogram plot.")
    plt.xlabel("Time Difference in ms")

    iqr = stats.iqr(fulldata)

    a, b, c = stats.lognorm.fit(fulldata)
    pa, ploc, pscale = stats.powerlaw.fit(fulldata)
    ga, gb, gc = stats.gamma.fit(fulldata)
    pa, pb, pc = stats.genpareto.fit([fulldata])
    print("Fitting done.")

    x = np.linspace(0, 3*iqr)
    pdf = stats.lognorm.pdf(x, a, scale=c)

    plt.hist(fulldata, bins, range=(0, 3*iqr), density=1, histtype='bar', color='lightgrey')

    plt.plot(x, pdf, color="#EF4F00", label="Lognormal")

    pldf = stats.powerlaw.pdf(x, pa, loc=ploc, scale=pscale)
    plt.plot(x, pldf, color="#177244", label="Power law")

    gpdf = stats.gamma.pdf(x, ga, gb, gc)
    plt.plot(x, gpdf, color="red", label="Gamma")

    gpdf = stats.genpareto.pdf(x, pa, pb, pc)
    plt.plot(x, gpdf, color="#003c9e", label="Generalized Pareto")

    plt.legend()
    plt.savefig(plotsfix + "distribution." + filetype, bbox_inches='tight', dpi=dpi)
    plt.clf()

every = 1000
c = 0

print("Full data input.")
fulldata = []
with open(prefix+"all-data.csv", "r") as csvfile:
    datareader = csv.reader(csvfile, delimiter=',')
    for row in datareader:
        if len(row) > 1:
            c += 1
            if c % every == 0:
                data = [int(_) for _ in row]
                fulldata.extend(list(filter(lambda y: y > 0, data)))
                c = 0

print("Amount of data points: "+str(len(fulldata)))

try:
    histhist(fulldata)
except:
    print("Histhist failed.")
#try:
#    pandcdf(fulldata)
#except:
#    print("pdf and cdf plots fails.")
try:
    exptest(fulldata)
except:
    print("exptest failed.")
#try:
#    loghist(fulldata)
#except:
#    print("Loghist failed.")

from random import shuffle
## log preparation
shuffle(fulldata)
print("Log preparation.")
logall = np.log10(fulldata[0:int(len(fulldata)*9/10)])
validation = np.log10(fulldata[int(len(fulldata)*9/10):])


try:
    powerlaw(logall)
except:
    print("Powerlaw failed.")