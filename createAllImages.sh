
#!/bin/sh

#array=(tp0 tp5 tp10 tp20)
mkdir -p images/Real
python imgGen.py Reald RealDistance.png Real | gnuplot
python imgGen.py acceleration acceleration.png Real |gnuplot
python imgGen.py RealSpeed RealSpeed.png Real | gnuplot

python imgGen.py fuelCongestion fuelCongestion.png | gnuplot
python imgGen.py timeCongestion timeCongestion.png | gnuplot

array=(tp0c0_4 tp0c0_6 tp0c0_8 tp0c1_0 tp0c1_2 tp0c1_4 tp0c1_6)
for i in "${array[@]}"
do
mkdir -p images/$i
python imgGen.py fuelRoute fuelRoute.png $i | gnuplot

python imgGen.py controlled_fuel_10 fuelRouteControlled10.png $i | gnuplot
python imgGen.py controlled_fuel_50 fuelRouteControlled50.png $i | gnuplot
python imgGen.py controlled_fuel_100 fuelRouteControlled100.png $i | gnuplot

python imgGen.py uncontrolled_fuel_0 fuelRouteUncontrolled0.png $i | gnuplot
python imgGen.py uncontrolled_fuel_10 fuelRouteUncontrolled10.png $i | gnuplot
python imgGen.py uncontrolled_fuel_50 fuelRouteUncontrolled50.png $i | gnuplot

python imgGen.py fuelTotal fuelTotal.png $i | gnuplot

python imgGen.py controlled_fuelTotal_10 fuelTotalControlled10.png $i | gnuplot
python imgGen.py controlled_fuelTotal_50 fuelTotalControlled50.png $i | gnuplot
python imgGen.py controlled_fuelTotal_100 fuelTotalControlled100.png $i | gnuplot

python imgGen.py uncontrolled_fuelTotal_0 fuelTotalUncontrolled0.png $i | gnuplot
python imgGen.py uncontrolled_fuelTotal_10 fuelTotalUncontrolled10.png $i | gnuplot
python imgGen.py uncontrolled_fuelTotal_50 fuelTotalUncontrolled50.png $i | gnuplot

python imgGen.py combinedFuel combinedFuel.png $i | gnuplot
python imgGen.py combinedTime combinedTime.png $i | gnuplot

#DIRS=`ls -l "TestResults/tp0/10" | egrep '^d' | awk '{print $9}'`
#for r in $DIRS
#do
#	python imgGen.py $r'_combinedRouteTime' $r'_combinedRouteTime.png' $i | gnuplot
#done

python imgGen.py _combinedRouteTime combinedRouteTime.png $i | gnuplot

python imgGen.py stops_0 stops0.png $i | gnuplot
python imgGen.py stops_10 stops10.png $i | gnuplot
python imgGen.py stops_50 stops50.png $i | gnuplot
python imgGen.py stops_100 stops100.png $i | gnuplot

python imgGen.py controlled_distance_10 distanceControlled10.png $i | gnuplot
python imgGen.py controlled_distance_50 distanceControlled50.png $i | gnuplot
python imgGen.py controlled_distance_100 distanceControlled100.png $i | gnuplot

python imgGen.py uncontrolled_distance_0 distanceUncontrolled0.png $i | gnuplot
python imgGen.py uncontrolled_distance_10 distanceUncontrolled10.png $i | gnuplot
python imgGen.py uncontrolled_distance_50 distanceUncontrolled50.png $i | gnuplot

python imgGen.py controlled_speed_10 speedControlled10.png $i | gnuplot
python imgGen.py controlled_speed_50 speedControlled50.png $i | gnuplot
python imgGen.py controlled_speed_100 speedControlled100.png $i | gnuplot

python imgGen.py uncontrolled_speed_0 speedUncontrolled0.png $i | gnuplot
python imgGen.py uncontrolled_speed_10 speedUncontrolled10.png $i | gnuplot
python imgGen.py uncontrolled_speed_50 speedUncontrolled50.png $i | gnuplot

done
