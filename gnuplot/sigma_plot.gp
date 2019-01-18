set datafile separator ","
set term png size 870,653 font "Times, 12"
set key font ",12"
set output ARG1."sigma.png"
set xrange [0:]
set xlabel "time [ms]"
set ylabel "sigma"
set key nobox right bottom
set title "Adaption of sigma over time"
set grid xtics mxtics ytics mytics

Maincolor = "#177244"
Shadecolor = "#8040c080"

Maincolor2 = "#EF4F00"
Shadecolor2 = "#80E0A080"

Truthcolor = "#003c9e"

filename = ARG1
filename2 = ARG2
stats filename.".stats.csv" using 1

plot filename.".stats.csv" using ($1-STATS_min):($8+$10):($8-$10) with filledcurve fc rgb Shadecolor title "Standard deviation of sigma Guesses",\
     '' using ($1-STATS_min):8 pointtype 4 lc rgb Maincolor title "Average of sigma Guesses",\
     filename.".stats-100.csv" using ($1-STATS_min):($8+$10):($8-$10) with filledcurve fc rgb Shadecolor2 title "Standard deviation of sigma Guesses (30 warmup steps filtered)",\
     '' using ($1-STATS_min):8 lc rgb Maincolor2 title "Average of sigma Guesses (30 warmup steps filtered)",\
     filename2 using ($1-STATS_min):3 lc rgb Truthcolor title "SciPy parameter estimation per transaction of full data"
#pause -1
