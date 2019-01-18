"""
Merge result files of btcmon:
Create buckets of bucketsize ms size
output file is determined by first argument
"""

import csv
import sys
import os

# generator to read csv files rowwise
def csvreader(file):
    data = csv.reader(file, delimiter=',')
    for row in data:
        yield [int(row[0]), row[1], row[2]]


files = []
csvs = []

addon = sys.argv[1]

bucketsize = 100

# open all files
for arg in sys.argv[2:]:
    if os.stat(arg).st_size > 0:
        f = open(arg, "r")
        files.append(f)
        csvs.append(csvreader(f))

# main part
current = [next(_) for _ in csvs]
with open(sys.argv[1], "w") as output:
    while len(csvs) > 0:
        row = min(current)
        time = int(row[0]) // bucketsize
        output.write(str(time*bucketsize))
        while time == int(min(current)[0]) // bucketsize:
            row = min(current)
            pos = current.index(row)
            output.write(","+row[1]+","+row[2])
            try:
                current[pos] = next(csvs[pos])
            except StopIteration:
                del current[pos]
                del csvs[pos]
            if len(current) == 0:
                break
        output.write("\n")

# close all files
for file in files:
    file.close()
