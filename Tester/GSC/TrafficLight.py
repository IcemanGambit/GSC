import sys, os, StringIO
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import traci 

"""
_getNextGreen(string, string, string, int) -> [[int, int],]

returns the interval of simulation steps where tlID has a green light at the specified connection within maxtime
"""

def getNextGreen(tlID, inEgdeId, outEgdeId, maxtime):

	# Next time the traffic light switch
	next = traci.trafficlights.getNextSwitch(tlID)
	
	#Get light position
	p=0
	for i in traci.trafficlights.getControlledLinks(tlID):
		if (inEgdeId == i[0][0].split("_")[0] and outEgdeId == i[0][1].split("_")[0]):
			break
		p+=1
	#TODO: check if p is too large

	#get redGreen string for next switch
	f = StringIO.StringIO(traci.trafficlights.getCompleteRedYellowGreenDefinition(tlID))
	step = 0
	parsingGreen = False
	startGreen = step
	lights = []
	while True:
		line = f.readline()
		#Reload file as EOF has been reached
		if not line:
			f = StringIO.StringIO(traci.trafficlights.getCompleteRedYellowGreenDefinition(tlID))
		if line == "Phase:\n":
			line = f.readline()
			step += int(line.split(": ")[1])
			if step > maxtime:
				break
			if step >= next:
				f.readline()
				f.readline()
				line = f.readline()
				redGreen = line.split(": ")[1]
				if parsingGreen and not redGreen[p].lower() == "g":
					lights.append([startGreen, step])
					parsingGreen = False
				if not parsingGreen and redGreen[p].lower() == "g":
					startGreen = step
					parsingGreen = True
				
	f.close()
	
	return lights
	
	

