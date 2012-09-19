import traci

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

def processDataCollection():
	return








