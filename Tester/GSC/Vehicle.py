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
		return TrafficLight.getNextGreen(TL[0],TL[1], TL[2], maxtime)
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

	if distance == None:
		return maxSpeed
	if distance >= minDistance:
		return maxSpeed

	smax = 0
	smin = 0

	for span in spans:
		deltaTbegin = span[0] - t
		#print deltaTbegin
		if t > span[1]:
			continue

		if(deltaTbegin <= 0):
			return maxSpeed	#light is green drive as fast as we want
		else:
			smax = distance/(deltaTbegin/1000)

		deltaTend =  span[1] - t
		smin = distance/(deltaTend/1000)
		
		if smin <= maxSpeed: # we have a timespan we can reach before it go red
			if smax > maxSpeed:	#we can drive max speed
				return maxSpeed 
			else:		
				return smax	#if we drive max speed I will not be green in time slow down!
	
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
	getDistanceNextTraficLight(int) -> int

	returns the euclidean distance to next intersection %TODO this might need fix to road length 
"""
def _getDistanceNextTrafficLight(vhId):
	#first we want the TL cordinate
	TL = _getNextTrafficLight(vhId)
	if not TL:
		return None
	TL_cord = traci.junction.getPosition(TL[0]) #note that Junction and traficlight is not the same but have identical id
	Vh_cord = traci.vehicle.getPosition(vhId)
	return math.sqrt(((TL_cord[0]-Vh_cord[0])**2) + ((TL_cord[1]-Vh_cord[1])**2)) - 20



