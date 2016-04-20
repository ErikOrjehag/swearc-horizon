set terminal svg enhanced size 1000 1000 fname "Times" fsize 20
unset parametric
#set encoding iso_8859_5
set output "traces.svg"
#set terminal png
#set output "avg_metric.png"
set grid
#set format y "$%3.1t \\cdot 10^{%L}$"
set border 3
#set xtics 0,1 nomirror
#set ytics 0,1 nomirror
set lmargin at screen 0.1
#set xlabel "$n, \\text{ а}$" 241.5
#set ylabel "$\epsilon, \\text{ }$" 17,11 rotate by 0
set arrow from graph 0,0 to graph 1,0 filled
set arrow from graph 0,0 to graph 0,1 filled
set key bottom
#set xrange [0:20]
#set yrange [20:0]
plot "r1d1" using 1:2 with lines t "r1d1"
