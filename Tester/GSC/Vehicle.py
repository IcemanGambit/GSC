import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import traci
import TrafficLight 

"""
	getGreenSpans(string, int) -> [[int,int],[int,int],...]

	returns the timeframes of green light for the next intersection
"""
def _getGreenSpans(vhId, maxtime):	
	raise NotImplementedError
	#Get the next traffic light
	#Get next time the traffic light switch to green
	print TrafficLight.getNextGreen(vhID, "Ju1")	

	
"""
	getRecommentedSpeed(string, int) -> int

	returns the recommented speed to reach the green light for next intersection within maxtime simulation steps
"""
def getRecommentedSpeed(vhId, maxtime):
	print getGreenSpans(vhId, maxtime)
	return 0

"""
	getNextTrafficLight(string) > string

	returns the next intersection
"""
def _getNextTrafficLight(vhId):
	route = traci.vehicle.getRoute(vhId)
	egde = traci.vehicle.getRoadID(vhId)
	startId = -1
	if egde in route:
		startId = route.index(egde)
	else:
		return None
		
	print "startid"
	print startId
		
	for egdeId in range(startId, len(route)):
		for tl in traci.trafficlights.getIDList():
			for i in traci.trafficlights.getControlledLinks(tl):
				for TLlane in i[0]:
					if route[egdeId] == TLlane.split("_")[0]:
						if (egdeId > 0 and not route[egdeId-1]==TLlane.split("_")[0]) or egdeId==0:
							return tl
	
"""
	getNextTraficLight(string) > string

	returns the next intersection
"""
def _getDistanceNextTraficLight(vhId):
	raise NotImplementedError

