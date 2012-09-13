import sys, os
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
def getRecommentedSpeed(vhId, maxtime):
	print getGreenSpans(vhId, maxtime)
	return 0


"""
	getNextTrafficLight(string) > [string, string, string]

	returns the next intersection puls the incomming and outgoing egdes on the route
"""
def _getNextTrafficLight(vhId):
	egde = traci.vehicle.getRoadID(vhId)
	nextTL = Route.getTrafficLightsOnRoute(vhId)
	if len(nextTL)== 0:
		return None
	if egde == nextTL[0][1]:
		Route.visitTrafficLight(vhId)
	if len(nextTL)== 0:
		return None
	return nextTL[0]
	
"""
	getNextTraficLight(string) > string

	returns the next intersection
"""
def _getDistanceNextTraficLight(vhId):
	raise NotImplementedError

