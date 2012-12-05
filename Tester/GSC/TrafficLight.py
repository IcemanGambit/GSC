import sys, os, StringIO, math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import traci 
import xml.parsers.expat
from types import *
import os
lights = {}  
lightSize = {}
inductionLoopsOnRoute = {} # vhId -> [position, boolean] - True if induction loop lead

timer = 0
vh_counter = 0

# 'string' -> [timer, vh_counter, [allow phases], timeout]
inductionLoopCounters = {'cluster_Ju_Hobrovej_sonderSkov_O_Ju_Hobrovej_sonderSkov_OS_Ju_Hobrovej_sonderSkov_V_Ju_Hobrovej_sonderSkov_VS' :[0,0,[[0,0,True],[1,1,False]], 5,False,[2]] ,'cluster_Ju_Hobrovej_MollerPark_Ju_Hobrovej_MollerPark_NO': [0,0,[[0,0,True],[1,1,False]], 5,False,[2]]  }

#
#'
"""
	_getNextGreen(string, string, string, int) -> [[int, int],]

	lights[tlID, egdeId, egdeId] -> (omloeb, (t1, t2), (t3, t_4), )
	
	returns the interval of simulation steps where tlID has a green light at the specified connection within maxtime
"""

def getNextGreen(tlId, inEgdeId, outEgdeId, maxtime):
	cur = traci.simulation.getCurrentTime()
	#If phase already recorded then
	#return calculate next green time span
	if (tlId, inEgdeId, outEgdeId) in lights:
		m = lights[tlId, inEgdeId, outEgdeId][0]
		if not m == 0:
			omloeb = math.floor(cur/m)
		else:
			omloeb = cur
			print "m is zerro"

		greenSpan = []
		i=0
		while True:
			for t in lights[tlId, inEgdeId, outEgdeId][1]:
				if t[1]+((omloeb+i)*m) > cur:
					greenSpan.append([t[0]+((omloeb+i)*m), t[1]+((omloeb+i)*m)])
	
			if len(greenSpan) > 0 and greenSpan[len(greenSpan)-1][1]>=cur+maxtime:
				break
			i+=1
		return greenSpan
	
	#Get light position in phase description
	p=0
	for i in traci.trafficlights.getControlledLinks(tlId):
		pos0 = i[0][0].rfind('_')
		pos1 = i[0][1].rfind('_')
		if (inEgdeId == i[0][0][:pos0] and outEgdeId == i[0][1][:pos1]):
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
	if(parsingGreen == True):
		lights[tlId, inEgdeId, outEgdeId][1].append([startGreen, step])
	
	#Record and call function again
	lights[tlId, inEgdeId, outEgdeId][0] = step
	return getNextGreen(tlId, inEgdeId, outEgdeId, maxtime)
	

def processTrafficLights():
	for n,i  in inductionLoopCounters.items():
		i[0] +=1 
		no = traci.inductionloop.getLastStepVehicleNumber("il_" + n)
		if no > 0:
			i[1]+= 1

		if i[1] > 0 and traci.trafficlights.getProgram(n)== "1":
			phase = traci.trafficlights.getPhase(n)
			remaningdur = (traci.trafficlights.getNextSwitch(n)- traci.simulation.getCurrentTime()) /1000

			for jumps in i[2]:
				if phase == jumps[0]:
					traci.trafficlights.setProgram(n, "2")
					i[4] = False
					traci.trafficlights.setPhase(n,  jumps[1])

				if jumps[2]:
					traci.trafficlights.setPhaseDuration(n,remaningdur)


		if traci.trafficlights.getPhase(n) in i[5] and traci.trafficlights.getProgram(n) == "2":
			i[1] = 0
			i[0] = 0
				
		if traci.trafficlights.getPhase(n) == i[3] and traci.trafficlights.getProgram(n) == "2":
			i[4] = True
			
		if  i[4] and  traci.trafficlights.getPhase(n) == 0 and traci.trafficlights.getProgram(n) == "2":
			traci.trafficlights.setProgram(n,"1")
			traci.trafficlights.setPhase(n, 0)


def getRadius(tlId):	
	assert type(tlId) is StringType, "tlId is not a string: %r" % id

	if tlId in lightSize:
		return lightSize[tlId]

	#math function to calculate the radius
	def _calculateSize(x,y,points):
		r = 0
		for ps in points:
			p = ps.split(",")
			r += math.sqrt(pow(float(x)-float(p[0]),2)+pow(float(y)-float(p[1]),2))
		return (r / len(points))

	#xml handler functions
	def _start_element(name, attrs):		
		if name == "junction" and "shape" in attrs and "id" in attrs and "x" in attrs and "y" in attrs:
			lightSize[attrs["id"]] = _calculateSize(attrs["x"],attrs["y"],attrs["shape"].split(" "))
			
		
	p = xml.parsers.expat.ParserCreate()

	p.StartElementHandler = _start_element

	if sys.argv[1][-1:] == "/":
		f = open( sys.argv[1] + "Data.net.xml")
	else:
		f = open( sys.argv[1] + "/Data.net.xml")
		
	p.ParseFile(f)
	return 0

def inductionLoopAhead(vhId):
	if vhId not in inductionLoopsOnRoute:
		route = traci.vehicle.getRoute(vhId)
		ilIds = traci.inductionloop.getIDList()
		inductionLoopEdges = {}
		
		for l in ilIds:
			lane = traci.inductionloop.getLaneID(l)
			inductionLoopEdges[lane[:lane.rfind('_')]] = [lane, traci.inductionloop.getPosition(l)]

		for e in route:
			if e in inductionLoopEdges:
				if vhId not in inductionLoopsOnRoute:
					inductionLoopsOnRoute[vhId] = [[inductionLoopEdges[e][0], inductionLoopEdges[e][1]]]
				else:
					inductionLoopsOnRoute[vhId].insert(0, [inductionLoopEdges[e][0], inductionLoopEdges[e][1]])

	
	
	if vhId in inductionLoopsOnRoute:
		vhLane = traci.vehicle.getLaneID(vhId)
		
		if vhLane == inductionLoopsOnRoute[vhId][0][0]:
			vhPosition = traci.vehicle.getLanePosition(vhId)

			if vhPosition < inductionLoopsOnRoute[vhId][0][1]:
				return True
			else:
				inductionLoopsOnRoute[vhId].pop(0)
				if len(inductionLoopsOnRoute[vhId]) == 0:
					inductionLoopsOnRoute.pop(vhId)
	return False



