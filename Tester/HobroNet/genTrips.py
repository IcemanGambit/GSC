import sys,random

if sys.argv[1] == "":
	print "Please enter the name of your files"
	sys.exit()

if sys.argv[2] == "":
	print "missing percent Trucks"
	sys.exit()

places = ['16_O', '18_N', '9_V', '9_V', '1_S', '3_V', '12_O', '2_O', '6_O', '19_O', '21_V', '16_V', '18_S', '10_O', '10_O', '1_N', '3_O', '12_V', '2_V', '6_V', '19_V', '21_O']
ODmatrix = [[0,0,0,0,0,0,0,0,0,0,0,0,153,2,0,32,24,14,13,5,266,9],[0,0,0,0,0,0,0,0,0,0,0,118,0,33,0,2638,761,2482,813,454,356,256],[0,0,0,0,0,0,0,0,0,0,0,0,22,162,0,70,50,6,10,26,8,93],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,91,3320,81,0,0,1359,3364,733,746,632,412],[0,0,0,0,0,0,0,0,0,0,0,39,609,31,0,1200,0,1504,1734,235,273,82],[0,0,0,0,0,0,0,0,0,0,0,17,1732,12,0,1323,1379,0,327,477,206,545],[0,0,0,0,0,0,0,0,0,0,0,13,770,10,0,131,1526,380,0,51,144,120],[0,0,0,0,0,0,0,0,0,0,0,9,274,5,0,224,278,438,63,0,35,79],[0,0,0,0,0,0,0,0,0,0,0,114,367,4,0,426,224,171,158,56,0,780],[0,0,0,0,0,0,0,0,0,0,0,12,225,79,0,185,64,483,80,81,751,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
i = 0
mod = 2
for il in ODmatrix:
	ODmatrix[i] = [(x*mod) / 100 for x in il]
	i+=1

#places = ['18_N', '1_N', '1_S', '18_S']
#ODmatrix = [[0,20,0,0],[0,0,0,0],[0,0,0,20],[0,0,0,0]]

noTrips = 0
for o in ODmatrix:
	for d in o:
		noTrips += d

departTimes = random.sample(xrange(0,noTrips*2), noTrips)


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



