import traci, Vehicle, os, random, shutil

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
			if vhId not in routes[r][1]:
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
def flushDataCollection(percent, path = "default"):		
	print "Flusing test results"
	
	outputPath = "Test/" + str(path) + "/"+str(percent)
	try:
		shutil.rmtree(outputPath)
	except:
		print "Creating new folder"
		
	os.makedirs(outputPath)
	
	totalTravelTime = 0;
	totalFuel = 0;
	total_no_vehicles = 0
	
	routeChart = open(outputPath + "/routeList.dat", "w")
	for r in routes:
		routeId = str(routes[r][0])
		os.makedirs(outputPath + "/" + str(routeId))
		totalFuelChart = open(outputPath + "/" + str(routeId)+ "/totalFuel.dat", "w")
		
		travelTime = 0;
		fuel = 0;
		
		#Print vehicle data		
		for vh in routes[r][1]:
			#travel distance, speed and fuel
			vehicleChart = open(outputPath + "/" + str(routeId)+ "/" + vh + ".dat", "w")
			t = 0
			for i in vehicleData[vh]:
				print >> vehicleChart, str(t) + "\t" + str(i[0])+ "\t" + str(i[1]*3.6)+ "\t" + str(i[2])
				t+=1
			vehicleChart.close()
			
			#total fuel
			totalFuel = vehicleData[vh][len(vehicleData[vh])-1][2]
			print >> totalFuelChart, str(vh) + "\t" + str(totalFuel)
			
			#Record average travel time and fuel for route
			travelTime += (vehicleTime[vh][1]-vehicleTime[vh][0])/1000
			fuel += totalFuel
			totalTravelTime += travelTime
			totalFuel += fuel
			total_no_vehicles += 1
			
		totalFuelChart.close()
		
		#Print average travel time and fuel for route
		no_vehicles = len(routes[r][1])
		avgChart = open(outputPath + "/" + str(routeId)+ "/avg.dat", "w")
		print >> avgChart, str(travelTime/no_vehicles) + "\t" + str(fuel/no_vehicles)
		avgChart.close()
									
		#Print route list
		print >> routeChart, routeId + ": " + r
		
	#Print average travel time and fuel
	avgChart = open(outputPath + "/avg.dat", "w")
	print >> avgChart, str(travelTime/no_vehicles) + "\t" + str(fuel/no_vehicles)
	avgChart.close()
		
	#Printing stops at traffic lights
	if len(VhStops) > 0:
		stopChart = None
		vhIds = sorted(VhStops, key=lambda e: len(VhStops[e]))
		length = 0
		first = True

		for vh in vhIds:
			if (len(VhStops[vh])> length):
				length = len(VhStops[vh])
				if(stopChart):
					stopChart.close()
				stopChart = open(outputPath + "/stops" + str(length) + ".dat", "w")
			
			for d in VhStops[vh]:
				print >> stopChart, str(vh) + "\t" + str(d)
		if(stopChart):
			stopChart.close()
