set -e

echo "Generate routes"
python genTrips.py $2
duarouter --net-file $1.net.xml --trip-files $2.xml --output-file $1.rou.xml

echo "run SUMO"
python simulate.py $1
