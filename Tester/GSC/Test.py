import traci, Vehicle

vehicleData = {}
routes = {}

"""
	processDataCollection([string,])->
	
	Collects the vehicles speeds in vehicleSpeeds and the vehicles routes in routes
"""
def processDataCollection(vehicles = None):
	if vehicles == None:
		vehicles = traci.vehicle.getIDList()
	
	for vhId in vehicles:
		#Process routes
		r =', '.join(traci.vehicle.getRoute(vhId))
		if r in routes:
			if vhId not in routes[r]:
				routes[r].append(vhId)
		else:
			routes[r] = [vhId]
			
		#Process speed and distance data
		if vhId in vehicleData:
			vehicleData[vhId].append([Vehicle.getTotalDistanceDriven(vhId), traci.vehicle.getSpeed(vhId)])
		else:
			vehicleData[vhId] = [[Vehicle.getTotalDistanceDriven(vhId), traci.vehicle.getSpeed(vhId)]]
		
"""
	flushDataCollection() ->
	
	print content of vehicleSpeeds to mulitiple files, one for each route type
"""
def flushDataCollection(vehicles = None):
	print "Flusing test results"
	
	initText = """
\\begin{figure}
\\begin{tikzpicture}
\\begin{axis}[
legend style={
	anchor=west
},
axis x line=bottom,
axis y line=left,
ymin=-1,
point meta=explicit symbolic,
xlabel=%s,
ylabel=%s
]"""
	endText = """
\\end{axis}
\\end{tikzpicture}
\\label{tik:%s}
\\caption{%s}
\\end{figure}"""

	rId = 0
	for r in routes:
		speedChart = open("Test/speedChart_" + str(rId), "w")
		distanceChart = open("Test/distanceChart_" + str(rId), "w")
		print >> speedChart, initText % ("Time", "Speed")
		print >> distanceChart, initText % ("Time", "Distance")
		for vh, data in vehicleData.iteritems():
			if vh in routes[r]:
				print >> speedChart, "\\addplot[] coordinates {"
				print >> distanceChart, "\\addplot[] coordinates {"
				t = 0
				for i in data:
					print >> speedChart, "(" + str(t) + ", " + str(i[1]) + ")"
					print >> distanceChart, "(" + str(t) + ", " + str(i[0]) + ")"
					t+=1
				print >> speedChart, "};"# \\addlegendentry{"+ vh + "}"
				print >> distanceChart, "};"# \\addlegendentry{"+ vh + "}"
		print >> speedChart, endText % (r, r)
		print >> distanceChart, endText % (r,r)
		rId += 1
				
		

'''
def flushDataCollection(vehicles = None):
	print "Flusing test results"
	
	rId =0
	for r in routes:
		speedChart = open("Test/speedChart_" + str(rId), "w")
		distanceChart = open("Test/distanceChart_" + str(rId), "w")

		i = 0
		a = 0
		for vh in vehicleData:
			if vh in routes[r]:
				speedChart.write(str(vh) + "\t ")
				distanceChart.write(str(vh) + "\t ")
		speedChart.write("\n")
		distanceChart.write("\n")
		while a < len(vehicleData): #TODO: +1?
			for vh, data in vehicleData.iteritems():
				if vh in routes[r]:
					if(len(data)> i):
						speedChart.write(str(data[i][1]) + "\t ")
						distanceChart.write(str(data[i][0]) + "\t ")
					else:
						a += 1
			i+=1
			speedChart.write("\n")
			distanceChart.write("\n")
		speedChart.close()
		distanceChart.close()
		rId +=1
		'''
	


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







