import traci, Vehicle, os

vehicleData = {}
vehicleTime = {} # [[depart, end], ]
routes = {}
avgValues = {} # [[number_of_vehicles_on_route, total_travel_time, total_fuel_consumption]]
TSSegments = ["1_S","1_S.-60"]
VhStops = {}
SpeedStop = 0.5
MinStopRange = 10

			#{key vhid, value [43,54,644]}
"""
	processDataCollection([string,])->
	
	Collects the vehicles speeds in vehicleSpeeds and the vehicles routes in routes
"""
def processDataCollection(vehicles = None):
	if vehicles == None:
		vehicles = traci.vehicle.getIDList()
	
	for vhId in vehicles:
		#Process routes. 
		#	routes[r] -> all vehicles on route r
		r =', '.join(traci.vehicle.getRoute(vhId))
		if r in routes:
			if vhId not in routes[r]:
				routes[r].append(vhId)
		else:
			routes[r] = [vhId]
			
		#Process speed, distance and fuel data.
		#	vehicleData[vhId] -> list of speed, travel distance and fuel consumption at each time step
		if vhId in vehicleData:
			vehicleData[vhId].append([Vehicle.getTotalDistanceDriven(vhId), traci.vehicle.getSpeed(vhId), vehicleData[vhId][len(vehicleData[vhId])-1][2] + traci.vehicle.getFuelConsumption(vhId)])
		else:
			vehicleData[vhId] = [[Vehicle.getTotalDistanceDriven(vhId), traci.vehicle.getSpeed(vhId), traci.vehicle.getFuelConsumption(vhId)]]

		#Process time
		#	vehicleTime[vhId] -> pair of depart and finish time
		if vhId in vehicleTime:
			vehicleTime[vhId][1] = traci.simulation.getCurrentTime()
		else:
			vehicleTime[vhId] = [traci.simulation.getCurrentTime(), 0]
		


		#proces Stopped Vh
		if traci.vehicle.getRoadID(vhId) in TSSegments:
			if not vhId in VhStops and Vehicle.getTotalDistanceDriven(vhId) > 30:
				VhStops[vhId] = []
			if vhId in VhStops:
				if traci.vehicle.getSpeed(vhId) < SpeedStop:
				 	if len(VhStops[vhId]) == 0 or VhStops[vhId][len(VhStops[vhId])-1] > max(0,Vehicle._getDistanceNextTrafficLight(vhId)) + MinStopRange:			
						VhStops[vhId].append(max(0,Vehicle._getDistanceNextTrafficLight(vhId)))
			
"""
	flushDataCollection() ->
	
	print content of vehicleSpeeds to mulitiple files, one for each route type
"""
def flushDataCollection(percent):
	print VhStops
		
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
\\label{tik:%s:%i:%s}
\\caption{%i percent diving with GSC on route $%s$}
\\end{figure}"""

	#Ensure directory Test/percent exist
	try:
		os.makedirs("Test/"+str(percent))
	except OSError as exception:
		print "Test/"+str(percent) + " already exist"
	
	routeChart = open("Test/"+str(percent)+ "/0routes.tex", "w")
	avgChart = open("Test/"+str(percent)+ "/avg.dat", "w")
	stopChart = open("Test/"+str(percent)+ "/stop.tex", "w")
	
	rId = 0
	for r in routes:
		speedChart = open("Test/"+str(percent)+ "/speed_" + str(rId) + ".tex", "w")
		distanceChart = open("Test/"+str(percent)+ "/distance_" + str(rId) + ".tex", "w")
		fuelChart = open("Test/"+str(percent)+ "/fuel_" + str(rId) + ".tex", "w")
		timeChart = open("Test/"+str(percent)+ "/time_" + str(rId) + ".tex", "w")
		
		print >> routeChart, str(rId) + ": " + r
		print >> speedChart, initText % ("Time (s)", "Speed (m/s)",)
		print >> distanceChart, initText % ("Time (s)", "Distance (m)",)
		print >> fuelChart, initText % ("Time (s)", "Fuel (mL)",)
		print >> timeChart, initTimeText % ("Vehicles", "Time (s)")
		print >> timeChart, "\\addplot coordinates {"

		v = 0 #Number of vehicles
		for vh, data in vehicleData.iteritems():
			if vh in routes[r]:
				print >> speedChart, "\\addplot[] coordinates {"
				print >> distanceChart, "\\addplot[] coordinates {"
				print >> fuelChart, "\\addplot[] coordinates {"
				
				t = 0 #Time step
				for i in data:
					print >> speedChart, "(" + str(t) + ", " + str(i[1]) + ")"
					print >> distanceChart, "(" + str(t) + ", " + str(i[0]) + ")"
					print >> fuelChart, "(" + str(t) + ", " + str(i[2]) + ")"
					t+=1
					
				print >> speedChart, "};"
				print >> distanceChart, "};"
				print >> fuelChart, "};"

				travelTime = (vehicleTime[vh][1]-vehicleTime[vh][0])/1000
				print >> timeChart, "(" + vh + ", " + str(travelTime) + ")"
				v+=1
				
				if r in avgValues:
					avgValues[rId][0]+= 1
					avgValues[rId][1]+= travelTime
					avgValues[rId][2]+= vehicleData[vh][len(vehicleData[vh])-1][2] #Avg. fuel
				else:
					avgValues[rId]= [1,travelTime, vehicleData[vh][len(vehicleData[vh])-1][2]]

		print >> timeChart, "};"
		print >> speedChart, endText % ("speed", percent, rId, percent, rId)
		print >> distanceChart, endText % ("distance", percent, rId, percent, rId)
		print >> fuelChart, endText % ("fuel", percent, rId, percent, rId)
		print >> timeChart, endText % ("time", percent, rId, percent, rId)
		
		speedChart.close()
		distanceChart.close()
		fuelChart.close()
		timeChart.close()

		rId += 1

	#Printing average values
	print >> avgChart, "Route\t" + "Time\t" + "Fuel"
	for rId in avgValues:
		print >> avgChart, str(rId) + "\t" +str(avgValues[rId][1]/avgValues[rId][0]) + "\t" + str(avgValues[rId][2]/avgValues[rId][0])


	#Printing stops at traffic lights
	print >> stopChart, "\\begin{tikzpicture}\\begin{axis}"
	vhIds = sorted(VhStops, key=lambda e: len(VhStops[e]))
	length = 0
	first = True

	for vh in vhIds:
		if (len(VhStops[vh])> length):
			if first:
				print >> stopChart, "};"
				first=False
			print >> stopChart, "\\addplot+[ycomb] coordinates{"
			length = len(VhStops[vh])
			
		for d in VhStops[vh]:
			print >> stopChart, "(" + str(vh) + ", " + str(d) + ")"	
	
	if length > 0:
		print >> stopChart, "};"
	print >> stopChart, "\\end{axis}\\end{tikzpicture}"
	
	routeChart.close()
	avgChart.close()
	stopChart.close()
