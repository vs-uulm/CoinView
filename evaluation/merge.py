"""
Merge csv files ordered by row 1 into one file.
"""

import csv
import sys


# generator to read csv files rowwise
def csvreader(file):
    data = csv.reader(file, delimiter=',')
    for row in data:
        yield [int(row[0]), row[1], row[2]]


files = []
csvs = []

addon = sys.argv[1]

# open all files
for arg in sys.argv[2:]:
    f = open(arg, "r")
    files.append(f)
    csvs.append(csvreader(f))

# main part
current = [next(_) for _ in csvs]
with open(sys.argv[1], "w") as output:
    while len(csvs) > 0:
        value = min(current)
        pos = current.index(value)
        output.write(str(value[0])+","+value[1]+","+value[2]+"\n")
        try:
            current[pos] = next(csvs[pos])
        except StopIteration:
            del current[pos]
            del csvs[pos]

# close all files
for file in files:
    file.close()
