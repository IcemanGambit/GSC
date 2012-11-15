
#!/bin/sh
python img.py fuel fulegraf | gnuplot
python img.py fuel fulegraf2 | gnuplot

python imgGen.py distance_0 distance_0 | gnuplot
python imgGen.py distance_10 distance_10 | gnuplot
python imgGen.py distance_50 distance_50 | gnuplot
python imgGen.py distance_100 distance_100 | gnuplot


