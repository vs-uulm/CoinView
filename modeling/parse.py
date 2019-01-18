import csv
import sys
import time
from collections import defaultdict
from tqdm import *

start = time.time()

time_type = 10**6
time_unit = "ms"

tx = defaultdict(list)
us = defaultdict(int)
unique = set()

with open(sys.argv[1],"r") as csvfile:
    datareader = csv.reader(csvfile, delimiter=',')
    for row in tqdm(datareader):
        if (row[1], row[2]) not in unique:
            tx[row[2]].append(int(row[0]))
            us[row[1]] += 1
            unique.add((row[1], row[2]))

counter = defaultdict(int)
maxtimes = []
avgtimes = []
datasamples = []
for t in tqdm(tx.values()):
    counter[len(t)] += 1
    if len(t) > 1:
        maxtimes.append(max(t)-min(t))
        avgtimes.append(sum([_-min(t) for _ in t])/len(t))
    if len(t) > 100:
        datasamples.append(list(map(lambda x: x-min(t), t)))

print("Writing output.")

with open(sys.argv[1][0:-4]+"-data.csv","w") as csvout:
    writer = csv.writer(csvout, delimiter=',')
    for sample in datasamples:
        writer.writerow(sample[1:])

with open(sys.argv[1][0:-4]+"-results.txt","w") as resultsout:
    resultsout.write("Statistics:\n")
    resultsout.write(str(len(us))+" different participants\n")
    resultsout.write(str(len(tx))+" different transactions\n")

    resultsout.write("")
    resultsout.write("Global max max: "+str(max(maxtimes)/time_type)+time_unit+"\n")
    resultsout.write("Global min max: "+str(min(maxtimes)/time_type)+time_unit+"\n")
    resultsout.write("Global max avg: "+str(max(avgtimes)/time_type)+time_unit+"\n")
    resultsout.write("Global min avg: "+str(min(avgtimes)/time_type)+time_unit+"\n")
    resultsout.write("Global average of max: "+str(sum(maxtimes)/len(maxtimes)/time_type)+time_unit+"\n")
    resultsout.write("Global average of avg: "+str(sum(avgtimes)/len(avgtimes)/time_type)+time_unit+"\n")

end = time.time()

print("Runtime of evaluation script: {:2.2}s".format(end-start))