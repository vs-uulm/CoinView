import csv
import sys
import pathlib

addon = sys.argv[2]

pathlib.Path("results"+addon+"/"+sys.argv[1]).parent.mkdir(parents=True, exist_ok=True)

time_type = 1
time_unit = "ms"
originator = "unknown"

tx = []
unique = set()

with open(sys.argv[1], "r") as csvfile:
    datareader = csv.reader(csvfile, delimiter=',')
    minv = 999999999999999
    for row in datareader:
        value = int(row[0])
        if value < minv:
            minv = value
            originator = row[1]
        if row[1] not in unique:
            tx.append(value)
            unique.add(row[1])

maxtimes = []
avgtimes = []
datasamples = []

if len(tx) <= 3:
    quit()
#if len(tx) > 10:
maxtimes.append(max(tx)-min(tx))
avgtimes.append(sum([_-min(tx) for _ in tx])/len(tx))
#if len(tx) > 100:
#    datasamples = (list(map(lambda x: x-min(tx), tx)))
datasamples = (list(map(lambda x: x-min(tx), tx)))

if len(datasamples) > 1:
    # data file for this transaction
    with open("results"+addon+"/"+sys.argv[1][0:-4]+"-tx-data.csv", "w") as csvout:
        writer = csv.writer(csvout, delimiter=',')
        writer.writerow(datasamples[1:])
    # accumulator file for this originator, append data
    with open("results"+addon+"/"+originator+"-acc-data.csv", "a") as csvout:
        writer = csv.writer(csvout, delimiter=',')
        writer.writerow(datasamples[1:])

with open("results"+addon+"/results.csv", "a") as resultsout:
    resultsout.write(str(len(tx))+","+
                     str(max(maxtimes))+","+
                     str(min(maxtimes))+","+
                     str(max(avgtimes))+","+
                     str(min(avgtimes))+","+
                     str(sum(maxtimes) / len(maxtimes))+","+
                     str(sum(avgtimes) / len(avgtimes))+"\n")
