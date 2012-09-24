import sys, os, StringIO, math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import traci 

lights = {}

"""
	_getNextGreen(string, string, string, int) -> [[int, int],]

	returns the interval of simulation steps where tlID has a green light at the specified connection within maxtime
"""

def getNextGreen(tlId, inEgdeId, outEgdeId, maxtime):
	cur = traci.simulation.getCurrentTime()

	#If phase already recorded then
	#return calculate next green time span
	if (tlId, inEgdeId, outEgdeId) in lights:
		m = lights[tlId, inEgdeId, outEgdeId][0]
		if not m == 0:
			d = math.floor(cur/m)
		greenSpan = []
		i=0
		while True:
			for t in lights[tlId, inEgdeId, outEgdeId][1]:
				greenSpan.append([t[0]+((d+i)*m), t[1]+((d+i)*m)])
	
			if greenSpan[len(greenSpan)-1][1]>=cur+maxtime:
				break
			i+=1
		return greenSpan
	
	#Get light position in phase description
	p=0
	for i in traci.trafficlights.getControlledLinks(tlId):
		if (inEgdeId == i[0][0].split("_")[0] and outEgdeId == i[0][1].split("_")[0]):
			break
		p+=1
	
	PhaseDefinition = traci.trafficlights.getCompleteRedYellowGreenDefinition(tlId)	
	f = StringIO.StringIO(PhaseDefinition)
	
	step = 0
	parsingGreen = False
	startGreen = step
	lights[tlId, inEgdeId, outEgdeId] = [0, []]
	
	#Record green phases
	while True:
		line = f.readline()
		if not line:
			break
		if line == "Phase:\n":
			#Get red, yellow, green description at this phase
			line = f.readline()
			duration = int(line.split(": ")[1])
			f.readline()
			f.readline()
			line = f.readline()
			redGreen = line.split(": ")[1]

			#Record interval
			if parsingGreen and not redGreen[p].lower() == "g":#Light turns yellow or red
				lights[tlId, inEgdeId, outEgdeId][1].append([startGreen, step])
				parsingGreen = False
			if not parsingGreen and redGreen[p].lower() == "g":#Light turns green
				startGreen = step
				parsingGreen = True
				
			step += duration
	f.close()
	
	#Record and call function again
	lights[tlId, inEgdeId, outEgdeId][0] = step
	return getNextGreen(tlId, inEgdeId, outEgdeId, maxtime)
	
	

