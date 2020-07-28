set datafile separator ","
set term png size 1560,800 font "Times, 28"
set output P1.".png"
set xrange [0:]
set xlabel "time [ms]"
set ylabel "µ"
set key nobox right bottom
set title "Adaption of µ over time"
set grid xtics mxtics ytics mytics

Maincolor = "#177244"
Shadecolor = "#8040c080"

Maincolor2 = "#EF4F00"
Shadecolor2 = "#80E0A080"

Truthcolor = "#003c9e"

# base file to compare
# large version example: random--1m-ULM
filename = "../datasets/random-".P1

# ground truth via scipy
# large version example: txsplit--1m-ULM.truth.sort.csv
filename2 = "../datasets/txsplit-1m-".P1.".truth.sort.csv"

stats filename.".stats.csv" using 1

plot filename.".stats.csv" using ($1-STATS_min):($3+$5):($3-$5) with filledcurve fc rgb Shadecolor title "Standard deviation of µ Guesses",\
     '' using ($1-STATS_min):3 pointtype 4 lc rgb Maincolor title "Average of µ Guesses",\
     filename.".stats-100.csv" using ($1-STATS_min):($3+$5):($3-$5) with filledcurve fc rgb Shadecolor2 title "Standard deviation of µ Guesses (30 warmup steps filtered)",\
     '' using ($1-STATS_min):3 lc rgb Maincolor2 title "Average of µ Guesses (30 warmup steps filtered)",\
     filename2 using ($1-STATS_min):2 lc rgb Truthcolor title "SciPy parameter estimation per transaction of full data"

#pause -1
