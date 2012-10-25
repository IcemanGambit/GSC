import traci, Vehicle, os

vehicleData = {}
vehicleTime = {} # [[depart, end], ]
routes = {}
avgValues = {}

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
			
		#Process speed, distance and fuel data
		if vhId in vehicleData:
			vehicleData[vhId].append([Vehicle.getTotalDistanceDriven(vhId), traci.vehicle.getSpeed(vhId), vehicleData[vhId][len(vehicleData[vhId])-1][2] + traci.vehicle.getFuelConsumption(vhId)])
		else:
			vehicleData[vhId] = [[Vehicle.getTotalDistanceDriven(vhId), traci.vehicle.getSpeed(vhId), traci.vehicle.getFuelConsumption(vhId)]]

		#Process time
		if vhId in vehicleTime:
			vehicleTime[vhId][1] = traci.simulation.getCurrentTime()
		else:
			vehicleTime[vhId] = [traci.simulation.getCurrentTime(), 0]
		
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
legend style={anchor=west},
axis x line=bottom,
axis y line=left,
ymin=-1,
xlabel=%s,
ylabel=%s,
]"""

	initTimeText = """
\\begin{figure}
\\begin{tikzpicture}
\\begin{axis}[
legend style={anchor=west},
xlabel=%s,
ylabel=%s,
ymin=0,
ybar,
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
		print "Test/"+str(percent) + "already exist"
	rId = 0
	for r in routes:
		speedChart = open("Test/"+str(percent)+ "/speed_" + str(rId) + ".tex", "w")
		distanceChart = open("Test/"+str(percent)+ "/distance_" + str(rId) + ".tex", "w")
		fuelChart = open("Test/"+str(percent)+ "/fuel_" + str(rId) + ".tex", "w")
		timeChart = open("Test/"+str(percent)+ "/time_" + str(rId) + ".tex", "w")
		avgChart = open("Test/"+str(percent)+ "/avg.tex", "w")
		
		print >> speedChart, initText % ("Time (s)", "Speed (m/s)",)
		print >> distanceChart, initText % ("Time (s)", "Distance (m)",)
		print >> fuelChart, initText % ("Time (s)", "Fuel (mL)",)
		print >> timeChart, initTimeText % ("Vehicles", "Time (s)")
		print >> timeChart, "\\addplot coordinates {"
		v = 0
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

				travelTime = (vehicleTime[vh][1]-vehicleTime[vh][0])/1000
				print >> timeChart, "(" + str(v) + ", " + str(travelTime) + ")"
				v+=1
				
				if r in avgValues:
					avgValues[r][0]+= 1
					avgValues[r][1]+= travelTime
				else:
					avgValues[r]= [1,travelTime]

		print >> timeChart, "};"# \\addlegendentry{"+ vh + "}"
		print >> speedChart, endText % (percent, r, percent, r)
		print >> distanceChart, endText % (percent, r, percent, r)
		print >> fuelChart, endText % (percent, r, percent, r)
		print >> timeChart, endText % (percent, r, percent, r)
		rId += 1

		#TODO:Not tested yet
		avgChart.write("Routes\t")
		for r in avgValues:
			avgChart.write(r+ "\t")
		avgChart.write("\nTravel time\t")
		for r in avgValues:
			avgChart.write(str(avgValues[r][1]/avgValues[r][0]) + "\t")
		avgChart.write("\n")



