"""
Split a 3-row csv file by the second row into different files.
"""

import csv
import sys
import pathlib

files = {}

addon = sys.argv[1][:-4]

pathlib.Path("txsplit-"+addon).mkdir(parents=True, exist_ok=True)

with open(sys.argv[1], "r") as csvfile:
    datareader = csv.reader(csvfile, delimiter=',')
    for row in datareader:
        with open("txsplit-"+addon+"/" + row[2] + ".csv", "a") as file:
            file.write(row[0]+"\n")
