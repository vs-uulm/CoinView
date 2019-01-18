"""
aggregates bins of txresults results
"""

import csv
import sys
import statistics as stat

def output(ts,mu,si):
    if len(mu) == 0:
        return
    print(str(ts)+","+str(min(mu))+","+str(stat.mean(mu))+","+str(stat.median(mu))+","+str(max(mu))+","
                     +str(min(si))+","+str(stat.mean(si))+","+str(stat.median(si))+","+str(max(si)))

ts = 0
bsize = 100

mu = []
si = []

with open(sys.argv[1], "r") as csvfile:
    datareader = csv.reader(csvfile, delimiter=',')
    for row in datareader:
        time = int(row[0])
        ctime = time-(time%bsize)
        if ctime != ts:
            output(ts, mu, si)
            ts = ctime
            mu = []
            si = []
        mu.append(float(row[1]))
        si.append(float(row[2]))

output(ts, mu, si)