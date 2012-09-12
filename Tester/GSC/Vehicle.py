import sys ,os
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

	distance = _getDistanceNextTraficLight(vhId)
	spans = _getGreenSpans(vhId, maxtime)

	t = traci.simulation.getCurrentTime()
	maxSpeed = traci.lane.getMaxSpeed(traci.vehicle.getLaneID(vhId))

	smax = 0
	smin = 0

	for span in spans:

		deltaTbegin = span[0] - t
		if(deltaTbegin <= 0):
			deltaTbegin = 0
			smax = maxSpeed	#light is green drive as fast as we want
		else
			smax = distance/deltaTbegin

		deltaTend =  span[1] - t
		smin = distance/deltaTend
		
		if smin <= maxSpeed: # we have a timespan we can reach before it go red
			if smax > maxSpeed:	#we can drive max speed
				return maxSpeed 
			else				
				return smax	#if we drive max speed i will not be green in time slow down!
	
	return maxSpeed

"""
	getNextTraficLight(string) > string

	returns the next intersection
"""
def _getNextTraficLight(vhId):
	raise NotImplementedError
"""
	getDistanceNextTraficLight(int) > int

	returns the euclidean distance to next intersection %TODO this might need fix to road length 
"""
def _getDistanceNextTraficLight(vhId):
	#first we want the TL cordinate
	TL = _getNextTraficLight(vhId)
	TL_cord = traci.junction.getPosition(TL) #note that Junction and traficlight is not the same but have identical id
	Vh_cord = traci.vehicle.getPosition(vhId)
	return sqrt(((TL_cord[0]-Vh_cord[0])**2) + ((TL_cord[1]-Vh_cord[1])**2))
		

