import traci, Vehicle, os, random

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
		#	routes[r] -> route id and all vehicles on route r
		r =', '.join(traci.vehicle.getRoute(vhId))
		if r in routes:
			if vhId not in routes[r]:
				routes[r][1].append(vhId)
		else:
			routes[r] = [traci.vehicle.getRouteID(vhId),[vhId]]
			
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
\\caption{%i percent diving with GSC on route $%s$}
\\label{tik:%s:%i:%s}
\\end{figure}"""

	#Ensure directory Test/percent exist
	try:
		os.makedirs("Test/"+str(percent))
	except OSError as exception:
		print "Test/"+str(percent) + " already exist"
	
	routeChart = open("Test/"+str(percent)+ "/0routes.tex", "w")
	routeAvgFuelTimeChart = open("Test/"+str(percent)+ "/RouteAvgFuelTime", "w")
	stopChart = open("Test/"+str(percent)+ "/stop.tex", "w")
	avgChart = open("Test/"+str(percent)+"/avgValues", "w")
	
	for r in routes:
		rId = routes[r][0]
		speedChart = open("Test/"+str(percent)+ "/speed_" + str(rId) + ".tex", "w")
		distanceChart = open("Test/"+str(percent)+ "/distance_" + str(rId) + ".tex", "w")
		fuelChart = open("Test/"+str(percent)+ "/fuel_" + str(rId) + ".tex", "w")
		timeChart = open("Test/"+str(percent)+ "/time_" + str(rId) + ".tex", "w")
		
		print >> routeChart, str(rId) + ": " + r
		print >> speedChart, initText % ("Time (s)", "Speed (m/s)",)
		print >> distanceChart, initText % ("Time (s)", "Distance (m)",)
		print >> fuelChart, "VehicleId\tFuel"
		print >> timeChart, initTimeText % ("Vehicles", "Time (s)")
		print >> timeChart, "\\addplot coordinates {"
		
		vehicles = routes[r][1]
		random.shuffle(vehicles)

		v = 0 #Number of vehicles
		for vh in vehicles:
			if v < 10:
				print >> speedChart, "\\addplot[] coordinates {"
			print >> distanceChart, "\\addplot[] coordinates {"
		
			t = 0 #Time step
			for i in vehicleData[vh]:
				if v < 10:
					print >> speedChart, "(" + str(t) + ", " + str(i[1]) + ")"
				print >> distanceChart, "(" + str(t) + ", " + str(i[0]) + ")"
				t+=1
			
			print >> fuelChart, vh + " " + str(vehicleData[vh][len(vehicleData[vh])-1][2])
			
			if v < 10:
				print >> speedChart, "};"
			print >> distanceChart, "};"

			travelTime = (vehicleTime[vh][1]-vehicleTime[vh][0])/1000
			print >> timeChart, "(" + vh + ", " + str(travelTime) + ")"
		
			if r in avgValues:
				avgValues[rId][0]+= 1 #Number of records
				avgValues[rId][1]+= travelTime # Avg. travel time
				avgValues[rId][2]+= vehicleData[vh][len(vehicleData[vh])-1][2] #Avg. fuel
			else:
				avgValues[rId]= [1,travelTime, vehicleData[vh][len(vehicleData[vh])-1][2]]
				
			v+=1 #Next vehicle

		print >> timeChart, "};"
		print >> speedChart, endText % (percent, rId, "speed", percent, rId)
		print >> distanceChart, endText % (percent, rId, "distance", percent, rId)
		print >> timeChart, endText % (percent, rId, "time", percent, rId)
		
		speedChart.close()
		distanceChart.close()
		fuelChart.close()
		timeChart.close()


	#Printing average values
	print >> routeAvgFuelTimeChart, "Route\t" + "Time\t" + "Fuel"
	avgFuel = 0
	for rId in avgValues:
		print >> routeAvgFuelTimeChart, str(rId) + "\t" +str(avgValues[rId][1]/avgValues[rId][0]) + "\t" + str(avgValues[rId][2]/avgValues[rId][0])
		avgFuel +=avgValues[rId][2]/avgValues[rId][0]
	print >> avgChart, "Fuel\t"+str(avgFuel/len(avgValues))


	#Printing stops at traffic lights
	if len(VhStops) > 0:
		print >> stopChart, "\\begin{figure}\\begin{tikzpicture}\\begin{axis}[width=9.5cm]"
		vhIds = sorted(VhStops, key=lambda e: len(VhStops[e]))
		length = 0
		first = True

		for vh in vhIds:
			if (len(VhStops[vh])> length):
				if first==False:
					print >> stopChart, "};"
				first=False
				print >> stopChart, "\\addplot+[ycomb] coordinates{"
				length = len(VhStops[vh])
			
			for d in VhStops[vh]:
				print >> stopChart, "(" + str(vh) + ", " + str(d) + ")"	
			
			#print >> stopChart, "};"
		print >> stopChart, "};\\end{axis}\\end{tikzpicture}\\caption{Stops}\\label{tik:stops}\\end{figure}"
	
	routeChart.close()
	routeAvgFuelTimeChart.close()
	stopChart.close()
	avgChart.close()
