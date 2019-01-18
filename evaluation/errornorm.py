"""
applies error correction to data of probsim
"""

import csv
import sys
import sys
import statistics as stat


def data(values):
    return [min(values),stat.mean(values),stat.median(values),stat.pstdev(values),max(values)]


delim = ";"

with open(sys.argv[1], "r") as csvfile:
    datareader = csv.reader(csvfile, delimiter=delim)
    for row in datareader:
        if row[0] == "si\µ":
            continue
        s = float(row[0])
        print(delim.join([str(_) for _ in [s]+data([float(_) for _ in row[1:]])]))
