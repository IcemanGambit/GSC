"""
This file is used only for recording the testresults and do only pull data from the simulater
"""
import traci, Vehicle, os, random, shutil
from sets import Set

vehicleData = {} #{key vhid, value [43,54,644]}
vehicleTime = {} # [[depart, end], ]
routes = {}
controlledVehicles = Set() # set of vehicles controlled by system

TSSegments = ["1_S_1","1_S_1.-60"]
VhStops = {}
SpeedStop = 0.5
MinStopRange = 10


"""
	recordVehiclesOnRoutes([string, ]) ->
"""

def recordVehiclesOnRoute(vehicles = None):
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

			
"""
	processDataCollection([string,bool])->
	
	Collects the vehicles speeds in vehicleSpeeds and the vehicles routes in routes
"""
def processDataCollection(vhId, controlled):
	if controlled :
		controlledVehicles.add(vhId)
	
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
	

	#Process stopped vehicles
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
		print "Creating new folder: " + outputPath
		
	os.makedirs(outputPath)
	os.makedirs(outputPath + '/controlled')
	os.makedirs(outputPath + '/uncontrolled')
	
	totalTravelTime = 0;
	totalFuel = 0;
	totalControlledTravelTime = 0;
	totalControlledFuel = 0;
	totalUncontrolledTravelTime = 0;
	totalUncontrolledFuel = 0;
	
	total_no_vehicles = 0
	total_controlled_no_vehicles = 0
	total_uncontrolled_no_vehicles = 0
	
	routeChart = open(outputPath + "/routeList.dat", "w")
	allFuelChart = open(outputPath + "/totalFuel.dat", "w")
	controlledAllFuelChart = open(outputPath + "/controlled/totalFuel.dat", "w")
	uncontrolledAllFuelChart = open(outputPath + "/uncontrolled/totalFuel.dat", "w")
	
	for r in routes:
		routeId = str(routes[r][0])
		os.makedirs(outputPath + "/" + str(routeId) + "/controlled")
		os.makedirs(outputPath + "/" + str(routeId) + "/uncontrolled")
		controlledTotalFuelChart = open(outputPath + "/" + str(routeId)+ "/controlled/totalFuel.dat", "w")
		uncontrolledTotalFuelChart = open(outputPath + "/" + str(routeId)+ "/uncontrolled/totalFuel.dat", "w")
		totalFuelChart = open(outputPath + "/" + str(routeId)+ "/totalFuel.dat", "w")
		
		controlledTravelTime = 0;
		controlledFuel = 0;
		uncontrolledTravelTime = 0;
		uncontrolledFuel = 0;

		controlledVhCounter = 0;
		uncontrolledVhCounter = 0;
		vhCounter = 0
		#Print vehicle data		
		for vh in routes[r][1]:
			fuel = vehicleData[vh][len(vehicleData[vh])-1][2]
			travelTime = (vehicleTime[vh][1]-vehicleTime[vh][0])/1000
			if vh in controlledVehicles:
				vehicleChart = open(outputPath + "/" + str(routeId)+ "/controlled/" + vh + ".dat", "w")
				print >> controlledTotalFuelChart, str(controlledVhCounter) + "\t" + str(fuel)
				print >> controlledAllFuelChart, str(total_controlled_no_vehicles) + "\t" + str(fuel)
				
				controlledTravelTime += travelTime
				controlledFuel += fuel
				
				controlledVhCounter += 1
				total_controlled_no_vehicles += 1
			else:
				vehicleChart = open(outputPath + "/" + str(routeId)+ "/uncontrolled/" + vh + ".dat", "w")
				print >> uncontrolledTotalFuelChart, str(uncontrolledVhCounter) + "\t" + str(fuel)
				print >> uncontrolledAllFuelChart, str(total_uncontrolled_no_vehicles) + "\t" + str(fuel)
				
				uncontrolledTravelTime += travelTime
				uncontrolledFuel += fuel
				
				uncontrolledVhCounter += 1
				total_uncontrolled_no_vehicles += 1
			
			print >> totalFuelChart, str(vhCounter) + "\t" + str(fuel)
			print >> allFuelChart, str(vh) + "\t" + str(fuel)
			vhCounter += 1
			
			#travel distance, speed and fuel
			t = 0
			for i in vehicleData[vh]:
				print >> vehicleChart, str(t) + "\t" + str(i[0])+ "\t" + str(i[1]*3.6)+ "\t" + str(i[2])
				t+=1
			vehicleChart.close()
					
			totalTravelTime += travelTime
			totalFuel += fuel
			
			total_no_vehicles += 1
			
		totalControlledTravelTime += controlledTravelTime
		totalControlledFuel += controlledFuel
		totalUncontrolledTravelTime += uncontrolledTravelTime
		totalUncontrolledFuel += uncontrolledFuel
			
		totalFuelChart.close()
		controlledTotalFuelChart.close()
		uncontrolledTotalFuelChart.close()
		
		#Print average travel time and fuel for route
		no_vehicles = len(routes[r][1])
		avgChart = open(outputPath + "/" + str(routeId)+ "/avg.dat", "w")
		print >> avgChart, str((controlledTravelTime+uncontrolledTravelTime)/no_vehicles) + "\t" + str((controlledFuel+uncontrolledFuel)/no_vehicles)
		avgChart.close()

		temp = Set(routes[r][1])
		temp.intersection_update(controlledVehicles)
		controlled_no_vehicles = len(temp)
		if controlled_no_vehicles > 0:
			controlledAvgChart = open(outputPath + "/" + str(routeId)+ "/controlled/avg.dat", "w")
			print >> controlledAvgChart, str(controlledTravelTime/controlled_no_vehicles) + "\t" + str(controlledFuel/controlled_no_vehicles)
			controlledAvgChart.close()

		uncontrolled_no_vehicles = no_vehicles - controlled_no_vehicles
		if uncontrolled_no_vehicles > 0:	
			uncontrolledAvgChart = open(outputPath + "/" + str(routeId)+ "/uncontrolled/avg.dat", "w")
			print >> uncontrolledAvgChart, str(uncontrolledTravelTime/uncontrolled_no_vehicles) + "\t" + str(uncontrolledFuel/uncontrolled_no_vehicles)
			uncontrolledAvgChart.close()
									
		#Print route list
		print >> routeChart, routeId + ": " + r
		
	allFuelChart.close()
	controlledAllFuelChart.close()
	uncontrolledAllFuelChart.close()
		
	#Print average travel time and fuel
	avgChart = open(outputPath + "/avg.dat", "w")
	print >> avgChart, str(totalTravelTime/total_no_vehicles) + "\t" + str(totalFuel/total_no_vehicles)
	avgChart.close()
	
	controlled_total_no_vehicles = len(controlledVehicles)	
	if controlled_total_no_vehicles > 0:
		avgChart = open(outputPath + "/controlled/avg.dat", "w")
		print >> avgChart, str(totalControlledTravelTime/controlled_total_no_vehicles) + "\t" + str(totalControlledFuel/controlled_total_no_vehicles)
		avgChart.close()
	
	uncontrolled_total_no_vehicles = total_no_vehicles-len(controlledVehicles)
	if uncontrolled_total_no_vehicles > 0:
		avgChart = open(outputPath + "/uncontrolled/avg.dat", "w")
		print >> avgChart, str(totalUncontrolledTravelTime/uncontrolled_total_no_vehicles) + "\t" + str(totalUncontrolledFuel/uncontrolled_total_no_vehicles)
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
