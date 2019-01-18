"""
filter a 3 row csv file by unique first row entries, only the last one will be kepts. assumes sorted file.
"""

import csv
import sys

prow = [0, 0, 0]

with open(sys.argv[1], "r") as csvfile:
    datareader = csv.reader(csvfile, delimiter=',')
    for row in datareader:
        time = int(row[0])
        if int(prow[0]) != time and int(prow[0]) != 0:
            print(str(prow[0]) + "," + prow[1] + "," + prow[2])
        prow = row

if int(prow[0]) > 0:
    print(str(prow[0]) + "," + prow[1] + "," + prow[2])
