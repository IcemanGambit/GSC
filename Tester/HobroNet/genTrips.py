import sys,random

if sys.argv[1] == "":
	print "Please enter the name of your files"
	sys.exit()

if sys.argv[2] == "":
	print "missing percent Trucks"
	sys.exit()

places = ['16_O', '18_N', '9_V', '9_V', '1_S', '3_V', '12_O', '2_O', '6_O', '19_O', '21_V', '16_V', '18_S', '10_O', '10_O', '1_N', '3_O', '12_V', '2_V', '6_V', '19_V', '21_O']
ODmatrix = [[0,0,0,0,0,0,0,0,0,0,0,1163,172,187,0,136,86,21,22,54,1017,260],[0,0,0,0,0,0,0,0,0,0,0,140,7072,4179,0,2632,760,2472,810,2591,355,253],[0,0,0,0,0,0,0,0,0,0,0,39,805,4041,0,2877,1364,349,889,1122,99,187],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,213,3309,999,0,13284,1341,3348,730,5305,632,410],[0,0,0,0,0,0,0,0,0,0,0,117,600,240,0,1188,6360,1491,1725,2200,271,80],[0,0,0,0,0,0,0,0,0,0,0,12,1719,2145,0,1319,1374,6424,326,2573,204,543],[0,0,0,0,0,0,0,0,0,0,0,43,767,162,0,127,1511,379,4809,606,144,120],[0,0,0,0,0,0,0,0,0,0,0,243,2114,595,0,1724,1883,3441,351,15795,606,506],[0,0,0,0,0,0,0,0,0,0,0,860,367,632,0,426,224,170,157,252,2989,776],[0,0,0,0,0,0,0,0,0,0,0,210,223,323,0,185,64,481,80,467,751,2363],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
i = 0
mod = 6
for il in ODmatrix:
	ODmatrix[i] = [(x*mod) / 100 for x in il]
	i+=1

print ODmatrix
#places = ['18_N', '1_N', '1_S', '18_S']
#ODmatrix = [[0,20,0,0],[0,0,0,0],[0,0,0,20],[0,0,0,0]]

noTrips = 0
for o in ODmatrix:
	for d in o:
		noTrips += d

departTimes = random.sample(xrange(0,noTrips), noTrips)


vehicleTypes = ["car", "truck"]
types = open(sys.argv[1]+"/Data.rou.xml", "w")
print >> types, """
	<routes>
	    <vType id="car" accel="1.8" decel="6" sigma="0.5" length="4" minGap="2" maxSpeed="41"/>
	    <vType id="truck" accel="0.3" decel="3" sigma="0.5" length="10" minGap="2" maxSpeed="25"/>
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
	if(random.randint(0,100)< int(sys.argv[2])):
		vehType = 1
	print >> trips, '	<trip id="%i" from="%s" to="%s" depart="%i" type="%s" departSpeed="max"/>' % (i[0],i[1], i[2], i[3], vehicleTypes[vehType])
print >> trips, '</trips>'
trips.close()



