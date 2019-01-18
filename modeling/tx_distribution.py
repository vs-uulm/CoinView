import os
import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from config import *

if len(sys.argv) < 2:
    addon = ""
else:
    addon = sys.argv[1]

def linecount(fname):
    if not fname.endswith("-acc-data.csv"):
        return None
    with open("results" + addon + "/" + fname) as f:
        count = 0
        datareader = csv.reader(f, delimiter=',')
        for row in datareader:
            if len(row) > 10:
                count += 1
    return count

_, _, fn = next(os.walk("results" + addon))
counts = list(filter(lambda x: x is not None, [linecount(f) for f in fn]))

loc, scale = stats.expon.fit(counts)

print("{} {}".format(loc, scale))

x = np.linspace(0, max(counts), 5000)
plt.hist(counts, bins=100, density=1)
plt.plot(x, stats.expon.pdf(x, loc, scale))
plt.savefig("plots"+addon+"/tx-distribution."+filetype, bbox_inches='tight', dpi=dpi)
#plt.show()
