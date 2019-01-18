import csv
import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from config import *

if len(sys.argv) < 2:
    addon = ""
else:
    addon = sys.argv[1]

prefix = "results"+addon+"/"
plotsfix = "plots"+addon+"/"
pdfs = []
lows = []
highs = []

percentile = 0.95

print("Read pdfs")
with open(prefix + "pdf-params.csv", "r") as pdffile:
    datareader = csv.reader(pdffile, delimiter=',')
    for row in datareader:
        pdfs.append((float(row[0]), float(row[1]), float(row[2])))

print("Plot start.")
plt.ylabel("time in ms")
for sigma, loc, scale in pdfs:
    # calculate 99th percentile
    highs.append(stats.lognorm.ppf(percentile, sigma, loc=loc, scale=scale)/1000)

#iqr = stats.iqr(highs)

#print(str(q1)+" "+str(q3))

for i in range(80, 100):
    print("{i}th percentile: {p:.0f}s".format(i=i, p=np.percentile(highs, i)))
p99 = np.percentile(highs, 99)
data = list(filter(lambda x: x < p99, highs))
p95 = np.percentile(highs, 95)
data95 = list(filter(lambda x: x < p95, highs))


plt.subplot(311)
plt.violinplot(highs, showmedians=True, vert=False)
plt.subplot(312)
plt.violinplot(data, showmedians=True, vert=False, showextrema=False)
plt.subplot(313)
plt.violinplot(data95, showmedians=True, vert=False, showextrema=False)

plt.xlabel("Time distribution until {:.0f}% of the network is reached for participants in seconds.".format(percentile*100))

plt.savefig(plotsfix+"/violins."+filetype, bbox_inches='tight', dpi=dpi)
