"""
applies error correction to data of probsim
"""

import csv
import sys


def err(si):
    return -0.207898 * si * si + 0.083586 * si - 0.032573


delim = ";"

with open(sys.argv[1], "r") as csvfile:
    datareader = csv.reader(csvfile, delimiter=delim)
    for row in datareader:
        if row[0] == "si\µ":
            print(delim.join(row))
            continue
        s = float(row[0])
        print(delim.join([str(_) for _ in [s]+[float(r)-err(s) for r in row[1:]]]))
