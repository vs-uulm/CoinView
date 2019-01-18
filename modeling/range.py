import csv
import sys
from tqdm import *

if len(sys.argv) < 2:
    addon = ""
else:
    addon = sys.argv[2]

minv = 2549626927069
maxv = 0

with open(sys.argv[1], "r") as csvfile:
    datareader = csv.reader(csvfile, delimiter=',')
    for row in tqdm(datareader):
        ts = int(row[0])
        if ts < minv:
            minv = ts
        if ts > maxv:
            maxv = ts

with open("ranges.csv", "a") as file:
    file.write(addon+","+str(minv)+","+str(maxv)+"\n")
