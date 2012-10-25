import sys, os, math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import traci
import TrafficLight, Route 

"""
	getGreenSpans(string, int) -> [[int,int],[int,int],...]

	returns the timeframes of green light for the next intersection
"""
def _getGreenSpans(vhId, maxtime):	
	TL = _getNextTrafficLight(vhId)
	if TL:
		g =TrafficLight.getNextGreen(TL[0],TL[1], TL[2], maxtime)
		return g
	return []
	
"""
	getRecommentedSpeed(string, int) -> int

	returns the recommented speed to reach the green light for next intersection within maxtime simulation steps
"""
def getRecommentedSpeed(vhId,minDistance, maxtime):
	distance = _getDistanceNextTrafficLight(vhId)
	spans = _getGreenSpans(vhId, maxtime)

	t = traci.simulation.getCurrentTime()
	maxSpeed = traci.lane.getMaxSpeed(traci.vehicle.getLaneID(vhId))
	
	if traci.vehicle.getRoadID(vhId).find("Ju_") >= 0:
		return maxSpeed


	#If there are no more traffic lights on route or
	#traffic light too far away
	# -> drive at max speed of the road
	if distance == None or distance >= minDistance:
		return maxSpeed

	#Calculate optimal speed
	smax = 0 #Reaching just as light changes to green
	smin = 0 #Reaching just before light changes to red

	for span in spans:
		deltaTbegin = (span[0] - t) + 1
		deltaTend =  (span[1] - t) - 1
		
		#If first span has passed
		# -> look at next span
		if t > span[1] or deltaTend <= 0:
			continue
		
		#If slowest speed is larger than max speed
		# -> look at next span
		smin = distance/(deltaTend/1000)
		if smin > maxSpeed:
			continue

		#If light is green
		if(deltaTbegin <= 0):
			smax = maxSpeed 					#Drive as fast possible
		else:
			smax = distance/(deltaTbegin/1000)	#Set speed to reach when it changes

		#print  str(deltaTbegin) + "\t" +  str(deltaTend)
		#print str(smin) + "\t" + str(smax)
		
		#Only drive at max speed and not slower than 0
		if smax > maxSpeed:
			smax = maxSpeed
		if smax < 0:
			smax = 0
		
		#We can reace the timespan before it goes red
		return smax

	#No traffic light ahead
	return maxSpeed

"""
	getNextTrafficLight(string) > [string, string, string]

	returns the next intersection puls the incomming and outgoing egdes on the route
"""
def _getNextTrafficLight(vhId):
	egde = traci.vehicle.getRoadID(vhId)
	nextTL = Route.getTrafficLightsOnRoute(vhId)
	if len(nextTL)== 0:
		return None
	if egde == nextTL[0][2]:
		Route.visitTrafficLight(vhId)
	if len(nextTL)== 0: 
		return None
	return nextTL[0]
	
"""
	getDistanceNextTraficLight(string) -> int

	returns the euclidean distance to next intersection  
"""
#TODO this might need fix to road length
def _getDistanceNextTrafficLight(vhId):
	TL = _getNextTrafficLight(vhId)
	if not TL:
		return None
	TL_cord = traci.junction.getPosition(TL[0]) #note that Junction and traficlight is not the same but have identical id
	Vh_cord = traci.vehicle.getPosition(vhId)
	#print TL[0]
	#print TrafficLight.getRadius(TL[0])
	return math.sqrt(((TL_cord[0]-Vh_cord[0])**2) + ((TL_cord[1]-Vh_cord[1])**2)) - TrafficLight.getRadius(TL[0])

"""
	getTotalDistanceDriven(string) -> int

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







