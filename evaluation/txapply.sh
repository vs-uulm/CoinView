#!/bin/sh
for i in $(ls $1/*.csv)
do
    python3 txresults.py $i >> truth.csv
done

# not necessary anymore as using scatter plot
# sort --field-separator=',' --key=1 truth.csv > truth.sort.csv