#!/bin/bash

#find "$1" -maxdepth 1 -type f -exec sh -c 'python3 stat.py "$1"' _ {} \;

find "$1" -name '*.csv' -maxdepth 1 -type f | xargs -0 -P 8 python3 stat.py "$1"

echo "Done."
