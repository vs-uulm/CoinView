import csv
import sys
import time
from tqdm import *
import pathlib

start = time.time()

files = {}

addon = sys.argv[2]

pathlib.Path("data"+addon).mkdir(parents=True, exist_ok=True)

with open(sys.argv[1], "r") as csvfile:
    datareader = csv.reader(csvfile, delimiter=',')
    for row in tqdm(datareader):
        with open("data"+addon+"/" + row[2] + ".csv", "a") as file:
            file.write(row[0]+","+row[1]+"\n")

end = time.time()

print("Runtime of splitting: {:2.2}s".format(end-start))