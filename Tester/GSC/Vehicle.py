import sys, os, math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import traci
import TrafficLight, Route

"""
	getRecommentedSpeed(string, int, int) -> int

	Returns the recommented speed to reach a green light for the next connection within mindistance and maxtime simulation steps
"""
def getRecommentedSpeed(vhId,minDistance, maxtime):
	distance = _getDistanceNextTrafficLight(vhId)
	spans = _getGreenSpans(vhId, maxtime)

	t = traci.simulation.getCurrentTime()
	maxSpeed = traci.lane.getMaxSpeed(traci.vehicle.getLaneID(vhId))
	
	#Vehicle is on a connection or there is an induction loop ahead. 
	if traci.vehicle.getRoadID(vhId).find("Ju_") >= 0 or TrafficLight.inductionLoopAhead(vhId):
		return maxSpeed
		

	#If there are no more traffic lights on route or the traffic light is too far away
	# -> drive at max speed
	if distance == None or distance >= minDistance:
		return maxSpeed

	#Calculate recommended speed
	smax = 0 #Reaching just as light changes to green
	smin = 0 #Reaching just before light changes to red
	
	for span in spans:
		deltaTbegin = (span[0] - t)
		deltaTend =  (span[1] - t)
				
		#If slowest speed is larger than max speed
		# -> look at next span
		smin = distance/(deltaTend/1000)
		if smin > maxSpeed:
			continue

		#If light is green
		if(deltaTbegin <= 0):
			smax = maxSpeed 					#Drive as fast possible
		else:
			smax = distance/(deltaTbegin/1000)	#Set speed to reach connection when it changes
		
		#Only drive at max speed
		if smax > maxSpeed:
			smax = maxSpeed
					
		#Always recommend at least 15 km/h ~ 4.1 m/s
		if smax < 4.1:
			return 4.1
			
		return smax

	#No traffic light ahead
	return maxSpeed

"""
	_getGreenSpans(string, int) -> [[int,int],[int,int],]

	Gets the next connection (traffic light) on route, and returns the time spans when it is green.
	Returned result is a list of pairs og start and end times represended as seconds since the simulation started.
"""
def _getGreenSpans(vhId, maxtime):	
	TL = _getNextTrafficLight(vhId)
	if TL:
		return TrafficLight.getNextGreen(TL[0],TL[1], TL[2], maxtime)
	return []


"""
	getNextTrafficLight(string) > [string, string, string]

	Returns the next traffic light id, the incomming and outgoing edges on the route
	The traffic light is visisted to reduce the complexity of getTrafficLightsOnRoute(vhId)

"""
def _getNextTrafficLight(vhId):
	edge = traci.vehicle.getRoadID(vhId)
	nextTL = Route.getTrafficLightsOnRoute(vhId)
	if len(nextTL)== 0:
		return None
	if edge == nextTL[0][2]:
		Route.visitTrafficLight(vhId)
	if len(nextTL)== 0: 
		return None
	return nextTL[0]
	
"""
	getDistanceNextTraficLight(string) -> int

	Returns the euclidean distance to the next traffic light, None if no light ahead.
"""
def _getDistanceNextTrafficLight(vhId):
	TL = _getNextTrafficLight(vhId)
	if not TL:
		return None
	TL_cord = traci.junction.getPosition(TL[0]) #Note that junction and traffic light is not the same but have identical id's
	Vh_cord = traci.vehicle.getPosition(vhId)

	return math.sqrt(((TL_cord[0]-Vh_cord[0])**2) + ((TL_cord[1]-Vh_cord[1])**2)) - TrafficLight.getRadius(TL[0])  #-20

"""
	getTotalDistanceDriven(string) -> int

	Note: This is not avaiable through TraCI, and we therefore made a hack. 
		This function must be called at each simulation step in order to function.
	
	The total distance driven is recoded in _previousDistance for each vehicle where first element is the distance, the second is the previous edge and the third is the previous lane.
	The route contain road ids, and only lanes have a length.
	getLanePosition(vhId) returns how far the vehicle has driven on this lane.
"""
_previousDistance = {}
def getTotalDistanceDriven(vhId):
	laneID = traci.vehicle.getLaneID(vhId)
	roadID = traci.vehicle.getRoadID(vhId)

	if not vhId in _previousDistance:
		_previousDistance[vhId] = [0,roadID, laneID]	
	
	if _previousDistance[vhId][1] != roadID:
		_previousDistance[vhId][0] += traci.lane.getLength(_previousDistance[vhId][2])
		_previousDistance[vhId][1] = roadID
		_previousDistance[vhId][2] = laneID

	return _previousDistance[vhId][0] + traci.vehicle.getLanePosition(vhId)
