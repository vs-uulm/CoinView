set datafile separator ";"
set term png size 1560,800 font "Times, 28"
set output "pe_heat-map.png"
set ylabel "σ"
set xlabel "µ"
set zlabel "deviation"
set xrange [5:19]
set yrange [0.2:5]
#set key nobox right top

set palette defined (0 "black", 0.2 "#003c9e", 2.5 "white", 5 "#EF4F00")

set title "Absolute Deviation of Lognormal Adaption Parameter µ Dependent on Hidden Parameters µ and sigma"
set xtics out nomirror
set ytics out nomirror
set grid xtics mxtics ytics mytics

set view map

filename = "..\\datasets\\pos_data.csv"
filename2 = "..\\datasets\\pos_data_errcorr.csv"

splot filename nonuniform matrix using 1:2:(abs($3)) with pm3d title "Absolute deviation of approaching value from hidden distribution"

#pause -1
