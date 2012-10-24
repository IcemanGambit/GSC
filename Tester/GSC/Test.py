import traci, Vehicle, os

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
			vehicleData[vhId].append([Vehicle.getTotalDistanceDriven(vhId), traci.vehicle.getSpeed(vhId), vehicleData[vhId][len(vehicleData[vhId])-1][2] + traci.vehicle.getFuelConsumption(vhId)])
		else:
			vehicleData[vhId] = [[Vehicle.getTotalDistanceDriven(vhId), traci.vehicle.getSpeed(vhId), traci.vehicle.getFuelConsumption(vhId)]]
		
"""
	flushDataCollection() ->
	
	print content of vehicleSpeeds to mulitiple files, one for each route type
"""
def flushDataCollection(percent):
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
\\label{tik:%i:%s}
\\caption{%i percent diving with GSC on route $%s$}
\\end{figure}"""

	try:
		os.makedirs("Test/"+str(percent))
	except OSError as exception:
		print "Test/"+str(percent) + " already exist"

	rId = 0
	for r in routes:
		speedChart = open("Test/"+str(percent)+ "/speed_" + str(rId) + ".tex", "w")
		distanceChart = open("Test/"+str(percent)+ "/distance_" + str(rId) + ".tex", "w")
		fuelChart = open("Test/"+str(percent)+ "/fuel_" + str(rId) + ".tex", "w")
		print >> speedChart, initText % ("Time (s)", "Speed (m/s)")
		print >> distanceChart, initText % ("Time (s)", "Distance (m)")
		print >> fuelChart, initText % ("Time (s)", "Fuel (mL)")
		for vh, data in vehicleData.iteritems():
			if vh in routes[r]:
				print >> speedChart, "\\addplot[] coordinates {"
				print >> distanceChart, "\\addplot[] coordinates {"
				print >> fuelChart, "\\addplot[] coordinates {"
				t = 0
				for i in data:
					print >> speedChart, "(" + str(t) + ", " + str(i[1]) + ")"
					print >> distanceChart, "(" + str(t) + ", " + str(i[0]) + ")"
					print >> fuelChart, "(" + str(t) + ", " + str(i[2]) + ")"
					t+=1
				print >> speedChart, "};"# \\addlegendentry{"+ vh + "}"
				print >> distanceChart, "};"# \\addlegendentry{"+ vh + "}"
				print >> fuelChart, "};"# \\addlegendentry{"+ vh + "}"
		print >> speedChart, endText % (percent, r, percent, r)
		print >> distanceChart, endText % (percent, r, percent, r)
		print >> fuelChart, endText % (percent, r, percent, r)
		rId += 1





