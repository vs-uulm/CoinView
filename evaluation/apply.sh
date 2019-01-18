#!/bin/sh
for i in $(ls $1/*.csv)
do
    ./btcmon < $i > $i.res.csv
    python3 filter.py $i.res.csv > $i.filter.csv
    tail -n +30 $i.filter.csv > $i.filter-100.csv
done

find ./$1/ -size  0 -print0 | xargs -0 rm --

cat $1/*.res.csv > $1.all.csv
python3 results.py $1.res.csv $1/*.filter.csv
python3 results.py $1.res-100.csv $1/*.filter-100.csv

python3 resultsParse.py $1.res.csv > $1.stats.csv
python3 resultsParse.py $1.res-100.csv > $1.stats-100.csv