
#!/bin/sh
python img.py fuel fuelgraph | gnuplot

python imgGen.py distance_0 distance_0 | gnuplot
python imgGen.py distance_10 distance_10 | gnuplot
python imgGen.py distance_50 distance_50 | gnuplot
python imgGen.py distance_100 distance_100 | gnuplot

python imgGen.py speed_0 speed_0 | gnuplot
python imgGen.py speed_10 speed_10 | gnuplot
python imgGen.py speed_50 speed_50 | gnuplot
python imgGen.py speed_100 speed_100 | gnuplot
