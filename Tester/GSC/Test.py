import traci

vehicleSpeeds = {}
routes = {}

"""
	processDataCollection([string,])->
	
	Collects the vehicles speeds in vehicleSpeeds and the vehicles routes in routes
"""
def processDataCollection(vehicles = None):
	if vehicles == None:
		vehicles = traci.vehicle.getIDList()
	
	for vhId in vehicles:
		r =','.join(traci.vehicle.getRoute(vhId))
		if vhId in vehicleSpeeds:
			vehicleSpeeds[vhId].append(traci.vehicle.getSpeed(vhId))
		else:
			vehicleSpeeds[vhId] = [traci.vehicle.getSpeed(vhId)]
		if r in routes:
			if vhId not in routes[r]:
				routes[r].append(vhId)
		else:
			routes[r] = [vhId]

"""
	flushDataCollection() ->
	
	print content of vehicleSpeeds to mulitiple files, one for each route type
"""
def flushDataCollection():
	print "Flusing test results"
	rId =0
	for r in routes:
		speedChart = open("Test/speedChart_" + str(rId), "w")
		i = 0
		a = 0
		for vh in vehicleSpeeds:
			if vh in routes[r]:
				speedChart.write(str(vh) + "\t ")
		speedChart.write("\n")
		while a < len(vehicleSpeeds): #TODO: +1?
			for vh, speeds in vehicleSpeeds.iteritems():
				if vh in routes[r]:
					if(len(speeds)> i):
						speedChart.write(str(speeds[i]) + "\t ")
					else:
						a += 1
			i+=1
			speedChart.write("\n")
		speedChart.close()
		rId +=1


## Unused functions

totalSpeedAll = 0
divSpeed = 0

"""
	printSpeed(file, string) ->
	
	Prints the speed of given vehicle to file
"""
def printSpeed(outputFile, vhId):
	print >> outputFile, "Speed, "+ vhId +": " + str(traci.vehicle.getSpeed(vhId))
	
"""
	printSpeed(file, [string,]) ->
	
	Prints the speed of the given vehicles to file. 
	If parameter is None, all vehicles in the net are used.
"""
def printSpeeds(outputFile, vehicles = None):
	if vehicles == None:
		vehicles = traci.vehicle.getIDList()
	
	for v in vehicles:
		printSpeed(outputFile,v)

"""
	printAverageSpeed(file, [string,]) ->
	
	Prints the average speed of the given vehicles to file. 
	If parameter is None, all vehicles in the net are used.
"""
def printAverageSpeed(outputFile, vehicles = None):
	if vehicles == None:
		vehicles = traci.vehicle.getIDList()
	
	totalSpeed = 0
	for v in vehicles:
		totalSpeed += traci.vehicle.getSpeed(v)
	print >> outputFile, "Avg. speed: " + str(totalSpeed/len(vehicles))

def collectAvgerageSpeed(vehicles = None):
	if vehicles == None:
		vehicles = traci.vehicle.getIDList()
	totalSpeedAll += traci.vehicle.getSpeed(vhId)
	divSpeed += 1

def printOverallAvgerageSpeed(outputFile):
	print >> outputFile, "Avg. speed: " +  str(totalSpeedAll/divSpeed)







