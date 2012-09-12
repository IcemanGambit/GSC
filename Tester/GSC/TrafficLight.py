import sys ,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import traci 

"""
_getNextGreen(string, string) -> int

returns the next simulation step where tlID changes to a green light
"""

def getNextGreen(tlID, inConId, outConId):
	# Get next time the traffic light switch
	# Get the lane at the traffic light 
	# Check that the lane has green


	#Get lane id of vehicle
	j=0
	print traci.vehicle.getLaneID(vhID)
	for i in traci.trafficlights.getControlledLinks(tlID):
		j+=1
		if traci.vehicle.getLaneID(vhID) in i[0]:
			print j
		

	#Get next time the traffic light switch
	next = traci.trafficlights.getNextSwitch(tlID)
	#print "next " + str(next)

	f = StringIO.StringIO(traci.trafficlights.getCompleteRedYellowGreenDefinition(tlID))
	readingPhase = False
	duration = 0
	while True:
		line = f.readline()
		if not line:
			break
		if line == "Phase:\n":
			readingPhase=True
			line = f.readline()
		if readingPhase:
			duration += int(line.split(": ")[1])
			if duration == next:
				#print "next"
				f.readline()
				f.readline()
				line = f.readline()
				redGreen = line.split(": ")[1]
				#print redGreen
			#print duration
		
			readingPhase=False

	print
	f.close()

