import sys,random

if sys.argv[1] == "":
	print "Please enter the name of your files"
	sys.exit()


places = ['1_S','2_O','3_V','6_O','9_V','12_O','14_V','16_O','18_N','19_O','21_V',      '1_N','2_V','3_O','6_V','10_O','12_V','14_O','16_V','18_S','19_V','21_O']
ODmatrix = [
[0,0,0,0,0,0,0,0,0,0,0, 00,20,50,10,05,10,05,10,99,40,50],
[0,0,0,0,0,0,0,0,0,0,0, 20,00,40,03,02,02,02,02,40,10,20],
[0,0,0,0,0,0,0,0,0,0,0, 20,40,00,05,03,05,02,05,60,20,25],
[0,0,0,0,0,0,0,0,0,0,0, 10,02,02,00,01,01,01,01,14,03,03],
[0,0,0,0,0,0,0,0,0,0,0, 05,01,01,00,00,00,01,01,05,03,03],
[0,0,0,0,0,0,0,0,0,0,0, 10,02,02,01,01,00,01,01,14,03,03],
[0,0,0,0,0,0,0,0,0,0,0, 10,02,02,01,01,01,00,01,14,03,03],
[0,0,0,0,0,0,0,0,0,0,0, 10,02,02,01,01,01,01,00,14,03,03],
[0,0,0,0,0,0,0,0,0,0,0, 50,20,20,10,05,10,05,10,00,40,50],
[0,0,0,0,0,0,0,0,0,0,0, 30,15,15,03,02,02,04,04,14,00,12],
[0,0,0,0,0,0,0,0,0,0,0, 30,15,15,02,01,03,05,03,14,14,00],

[0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0]]

#places = ['18_N', '1_N', '1_S', '18_S']
#ODmatrix = [[0,10,0,0],[0,0,0,0],[0,0,0,10],[0,0,0,0]]

noTrips = 0
for o in ODmatrix:
	for d in o:
		noTrips += d
departTimes = random.sample(xrange(0,noTrips), noTrips)

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
	if(random.randint(0,10)> 10):
		vehType = 1
	print >> trips, '	<trip id="%i" from="%s" to="%s" depart="%i" type="%s" departSpeed="max"/>' % (i[0],i[1], i[2], i[3], vehicleTypes[vehType])
print >> trips, '</trips>'
trips.close()



