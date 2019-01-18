#!/bin/bash

function redraw_progress_bar { # int barsize, int base, int i, int top
    local barsize=$1
    local base=$2
    local current=$3
    local top=$4
    local j=0
    local progress=$(( ($barsize * ( $current - $base )) / ($top - $base ) ))
    echo -n "["
    for ((j=0; j < $progress; j++)) ; do echo -n '='; done
    echo -n '=>'
    for ((j=$progress; j < $barsize ; j++)) ; do echo -n ' '; done
    echo -n "] $(( $current )) / $top " $'\r'
}

res=$(ls "$1"/*-acc-data.csv | wc -l)
echo "found $res results"
c=1

for i in "$1"/*-acc-data.csv
do
  redraw_progress_bar 50 4 $c $res
  python3 data.py $i
  ((c++))
done
echo ""
echo "Done."
