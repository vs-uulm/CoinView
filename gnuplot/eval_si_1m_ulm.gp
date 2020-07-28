set datafile separator ","
set term png size 1560,800 font "Times, 28"
set output "fe_sigma_all-1m-ULM.png"
set xrange [0:]
set xlabel "time [ms]"
set ylabel "σ"
set key nobox right top
set title "Adaption of sigma over time"
set grid xtics mxtics ytics mytics

Maincolor2 = "#EF4F00"
Shadecolor2 = "#80E0A080"

Truthcolor = "#C0003c9e"

filename = "..\\datasets\\random--1m-ULM"
filename2 = "..\\datasets\\txsplit--1m-ULM.truth.sort.csv"
stats filename.".stats.csv" using 1

set object 1 rectangle from "20000000",graph 0 to "24000000",graph 1 fs solid noborder fc rgb "#AAAAAAAA" behind

plot filename.".stats10k.csv" using ($1-STATS_min):($8+$10):($8-$10) with filledcurve fc rgb Shadecolor2 title "Standard deviation of sigma Guesses (30 warmup steps filtered)",\
     '' using ($1-STATS_min):8 lc rgb Maincolor2 title "Average of sigma Guesses (30 warmup steps filtered)",\
     filename2 every 70 using ($1-STATS_min):3 pt 5 lc rgb Truthcolor title "Average scipy parameter estimation per transaction of full data"

#pause -1
