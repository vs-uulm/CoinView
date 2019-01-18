import csv
import sys
import hashlib
import secrets

key = secrets.token_hex(16)

def anonymize(entry):
    return hashlib.sha256((entry+key).encode('utf-8')).hexdigest()

with open(sys.argv[2], "w") as output:
    with open(sys.argv[1], "r") as csvfile:
        datareader = csv.reader(csvfile, delimiter=',')
        for row in datareader:
            output.write(row[0]+","+anonymize(row[1])+","+row[2]+"\n")
