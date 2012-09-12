set -e

if [ ${2-""} == "-n" ]
then
	echo "Regenerating network file"
	if [ -f $1"/"Data.con.xml ]
	then
		netconvert --node-files=$1"/"Data.nod.xml --edge-files=$1"/"Data.edg.xml --connection-files=$1"/"Data.con.xml --output-file=$1"/"Data.net.xml
	else
		netconvert --node-files=$1"/"Data.nod.xml --edge-files=$1"/"Data.edg.xml --output-file=$1"/"Data.net.xml
	fi
else
	echo "Reusing network file"
fi

if [ -f $1"/"trips.xml ]
then
	echo "Reuses routes"
else
	echo "Generate new routes"
	python $1"/"genTrips.py $1
	duarouter --net-file $1"/Data".net.xml --trip-files $1"/"trips.xml --output-file $1"/Data".rou.xml
fi

echo "<?xml version='1.0' encoding='iso-8859-1'?>
<configuration xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:noNamespaceSchemaLocation='http://sumo.sf.net/xsd/sumoConfiguration.xsd'>
    <input>
        <net-file value='Data.net.xml'/>
        <route-files value='Data.rou.xml'/>
    </input>
    <time>
       <begin value='0'/>
    </time>
    <report>
        <no-step-log value='true'/>
    </report>
    <traci_server>
        <remote-port value='8813'/>
    </traci_server>
</configuration>" > $1"/Data.sumocfg"

echo "run SUMO"
python $1"/"simulate.py $1
