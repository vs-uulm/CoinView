#!/bin/bash
for ((i=1;i<=$1;i++));
do
    shuf -n $2 -e $3/*.csv -z | xargs -r0 python3 merge.py random_$2_$i.csv
done
