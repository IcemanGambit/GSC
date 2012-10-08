import sys,random

if sys.argv[1] == "":
	print "Please enter the name of your files"
	sys.exit()


#places = [['Main1toJu1', 'Ju3toOst1'],['Main1toJu1', 'Ju3toOst1'],['Main1toJu1', 'Ju2toS2'],['Main1toJu1', 'Ju1toS1'],['Ost1toJu3', 'Ju1toMain1'],['Ost1toJu3', 'Ju1toMain1'],['Ost1toJu3', 'Ju1toS1'],['N1toJu1', 'Ju1toS1'],['N2toJu2', 'Ju2toS2'],['S1toJu1', 'Ju1toN1']]

places = ['Main1toJu1', 'Ju3toOst1', 'Ju2toS2', 'Ju1toS1', 'Ost1toJu3', 'Ju1toMain1', 'N1toJu1', 'N2toJu2', 'S1toJu1', 'Ju1toN1']
ODmatrix = [[0,10, 10, 10, 0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,10,0,10,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,10,0,0,0,0,0,0], [0,0,10,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,10], [0,0,0,0,0,0,0,0,0,0]]

noTrips = 0
for o in ODmatrix:
	for d in o:
		noTrips += d
departTimes = random.sample(xrange(0,noTrips*5), noTrips)

vehicleTypes = ["car", "truck"]
types = open(sys.argv[1]+"/Data.rou.xml", "w")
print >> types, """
	<routes>
	    <vType id="car" accel="2.5" decel="6" sigma="0.5" length="5" minGap="2" maxSpeed="41"/>
	    <vType id="truck" accel="0.8" decel="4.5" sigma="0.5" length="10" minGap="6" maxSpeed="25"/>
    </routes>"""

types.close()

details = []
TID=0
for fromID in range(0, len(places)):
	for toID in range(0, len(places)):	
		while ODmatrix[fromID][toID] > 0:
			details.append([TID, places[fromID], places[toID], departTimes[TID]])
			TID += 1
			ODmatrix[fromID][toID] -= 1
details.sort(key=lambda d: d[3])



trips = open(sys.argv[1]+"/trips.xml", "w")
print >> trips, "<trips>"
for i in details:
	vehType = 0
	if(random.randint(0,10)> 8):
		vehType = 1
	print >> trips, '	<trip id="%i" from="%s" to="%s" depart="%i" type="%s"/>' % (i[0],i[1], i[2], i[3], vehicleTypes[vehType])
print >> trips, '</trips>'
trips.close()



