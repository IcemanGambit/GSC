
#!/bin/sh
python imgGen.py fuel fuelgraph.png | gnuplot

python imgGen.py stops_0 stops0.png | gnuplot
python imgGen.py stops_10 stops10.png | gnuplot
python imgGen.py stops_50 stops50.png | gnuplot
python imgGen.py stops_100 stops100.png | gnuplot


python imgGen.py distance_0 distance0.png | gnuplot
python imgGen.py distance_10 distance10.png | gnuplot
python imgGen.py distance_50 distance50.png | gnuplot
python imgGen.py distance_100 distance100.png | gnuplot

python imgGen.py speed_0 speed0.png | gnuplot
python imgGen.py speed_10 speed10.png | gnuplot
python imgGen.py speed_50 speed50.png | gnuplot
python imgGen.py speed_100 speed100.png | gnuplot
