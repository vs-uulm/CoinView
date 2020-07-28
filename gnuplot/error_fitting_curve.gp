set datafile separator ";"
#set term png size 1739,1306
set term png size 1560,800 font "Times, 28"
set output "pe_error_curve.png"
set xlabel "sigma"
set ylabel "deviation"
set xrange [0.2:5]
set key nobox left bottom

set title "Error Correction of Lognormal Adaption Parameter µ"
set grid xtics mxtics ytics mytics

Maincolor = "#177244"

Maincolor2 = "#EF4F00"
Shadecolor2 = "#80E0A080"

Truthcolor = "#003c9e"

filename = "..\\datasets\\pos_data_stats.csv"
filename2 = "..\\datasets\\pos_data_errcorr_stats.csv"

f(si) = -0.207898 * si * si + 0.083586 * si - 0.032573

set object 1 rectangle from "0.7",graph 0 to "1.3",graph 1 fs solid noborder fc rgb "#AAAAAAAA" behind


plot f(x) lw 5 lc rgb Maincolor title "fitted error correction curve",\
     filename using 1:3:2:6 with errorbars pt 4 lw 3 lc rgb Maincolor2 title "deviation",\
     filename2 using 1:3 pt 1 lw 3 lc rgb Truthcolor title "difference of deviation and error correction"

#pause -1
