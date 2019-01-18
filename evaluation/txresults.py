"""
takes a csv of a single tx and outputs a single csv line:
t,mu,si
"""
import csv
import sys
import scipy.stats as stats
import math

values = []

with open(sys.argv[1], "r") as file:
    data = csv.reader(file, delimiter=',')
    for row in data:
        values.append(int(row[0]))

first = min(values)
last = max(values)
values = [_-first for _ in values if _-first > 0]
if len(values) > 10:
    s, loc, scale = stats.lognorm.fit(values, floc=0)
    print(str(last)+","+str(math.log(scale))+","+str(s))
