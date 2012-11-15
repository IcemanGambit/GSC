
#!/bin/sh

array=(tp0 tp5 tp10 tp20)
for i in "${array[@]}"
do
mkdir -p images/$i
python imgGen.py fuelRoute fuelRoute.png $i | gnuplot

#python imgGen.py fuelTotal fuelTotal.png | gnuplot

python imgGen.py stops_0 stops0.png $i | gnuplot
python imgGen.py stops_10 stops10.png $i | gnuplot
python imgGen.py stops_50 stops50.png $i | gnuplot
python imgGen.py stops_100 stops100.png $i | gnuplot


python imgGen.py distance_0 distance0.png $i | gnuplot
python imgGen.py distance_10 distance10.png $i | gnuplot
python imgGen.py distance_50 distance50.png $i | gnuplot
python imgGen.py distance_100 distance100.png $i | gnuplot

python imgGen.py speed_0 speed0.png $i | gnuplot
python imgGen.py speed_10 speed10.png $i | gnuplot
python imgGen.py speed_50 speed50.png $i | gnuplot
python imgGen.py speed_100 speed100.png $i | gnuplot
done
