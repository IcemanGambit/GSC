import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import traci
import TrafficLight 

"""
	getGreenSpans(string, int) -> [[int,int],[int,int],...]

	returns the timeframes of green light for the next intersection
"""
def _getGreenSpans(vhId, maxtime):	

	#Get the next traffic light
	#Get next time the traffic light switch to green
	print TrafficLight.getNextGreen(vhID, "Ju1")
	

	return [[0,0],[0,0]]
	

	
"""
	getRecommentedSpeed(string, int) -> int

	returns the recommented speed to reach the green light for next intersection within maxtime simulation steps
"""
def getRecommentedSpeed(vhId, maxtime):
	print getGreenSpans(vhId, maxtime)
	return 0

"""
	getNextTraficLight(string) > string

	returns the next intersection
"""
def _getNextTraficLight(vhId):
	raise NotImplementedError
"""
	getNextTraficLight(string) > string

	returns the next intersection
"""
def _getDistanceNextTraficLight(vhId):
	raise NotImplementedError

