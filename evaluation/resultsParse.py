"""
Takes a csv of the format:
t,m1,s1,m2,s2,...,mi,si
t,m1,s1,m2,s2,...,mj,sj
t,m1,s1,m2,s2,...,mk,sk

and creates:
1    2       3        4         5         6      7       8           9      10      11       12
t,min(mi),avg(mi),median(mi),pstdev(),max(mi),min(si),avg(si),median(si),pstdev(),max(si),#amount
"""

import csv
import sys
import statistics as stat


def data(values):
    return (min(values),stat.mean(values),stat.median(values),stat.pstdev(values),max(values))


def tocsv(t):
    return str(t[0]) + "," + str(t[1]) + "," + str(t[2]) + "," + str(t[3]) + "," + str(t[4])


with open(sys.argv[1], "r") as csvfile:
    datareader = csv.reader(csvfile, delimiter=',')
    for row in datareader:
        mus = [float(_) for _ in row[1::2]]
        sis = [float(_) for _ in row[2::2]]
        print(str(row[0]) + "," + tocsv(data(mus)) + "," + tocsv(data(sis)) + "," + str(len(mus)))
