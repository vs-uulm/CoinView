import sys
import os
from tqdm import *
from multiprocessing import Pool

#p = Pool(10)

# split, stat, data, pdf_printer
stages = [False, False, False, False]

if "all" in sys.argv:
    stages = [True, True, True, True]
else:
    for i in range(1, 5):
        if str(i) in sys.argv:
            stages[i-1] = True

def filedelete(fname):
    if os.path.exists(fname):
        os.remove(fname)

parameter = list(filter(lambda x: x.endswith(".csv"), sys.argv[1:]))[0]

addon = list(filter(lambda x: x != "all" and len(x) > 1 and not x.endswith(".csv"), sys.argv[1:]))[0]

# split
if stages[0]:
    os.system("python3 split.py "+parameter+" "+addon)
    print("Stage 1 (split) done.")
else:
    print("Stage 1 (split) skipped.")

# stat
if stages[1]:
    def run_stat(filename):
        os.system("python3 stat.py data" + addon + "/" + filename + " " + addon)
    _, _, fn = next(os.walk("data"+addon))
    for f in tqdm(fn):
        run_stat(f)
    #p.map(run_stat, fn)
    print("Stage 2 (stat) done.")
else:
    print("Stage 2 (stat) skipped.")

# data
if stages[2]:
    filedelete("results"+addon+"/all-data.csv")
    filedelete("results"+addon+"/pdf-params.csv")
    filedelete("results"+addon+"/pdf-params-double.csv")
    filedelete("results"+addon+"/gamma-pdf-params.csv")
    def run_data(filename):
        if "-acc-data.csv" not in filename:
            return
        os.system("python3 data.py results"+addon+"/" + filename + " " + addon)
    _, _, fn = next(os.walk("results"+addon))
    for f in tqdm(fn):
        run_data(f)
    #p.map(run_data, fn)
    os.chdir("results" + addon)
    os.system("../combine.sh")
    os.chdir("..")
    print("Stage 3 (data) done.")
else:
    print("Stage 3 (data) skipped.")

# pdf_printer
if stages[3]:
    os.system("python3 pdf_printer.py "+addon)
    print("Stage 4 (pdf_printer) done.")
else:
    print("Stage 4 (pdf_printer) skipped.")

