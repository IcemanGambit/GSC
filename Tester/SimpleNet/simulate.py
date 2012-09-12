import os, subprocess, sys, StringIO
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import traci 
import GSC
sumoBinary = "sumo-gui"
PORT = 8813

#Run SUMO and TraCI
process = subprocess.Popen("%s -c %s" % (sumoBinary, sys.argv[1] + "/Data.sumocfg"), shell=True, stdout=sys.stdout)
traci.init(PORT)

step = 0





while step==0 or traci.simulation.getMinExpectedNumber() > 0:
	traci.simulationStep()
	print GSC.Vehicle.getRecommentedSpeed(1)
	"""
	#TraCI control
	
	#Get lane id of vehicle
	j=0
	print traci.vehicle.getLaneID("0")
	for i in traci.trafficlights.getControlledLinks("Ju1"):
		j+=1
		if traci.vehicle.getLaneID("0") in i[0]:
			print j
			
	
	#Get next time the traffic ligts switch
	next = traci.trafficlights.getNextSwitch("Ju1")
	#print "next " + str(next)

	f = StringIO.StringIO(traci.trafficlights.getCompleteRedYellowGreenDefinition("Ju1"))
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
	
	"""
	
	step+=1

#Clean up
traci.close()
sys.stdout.flush()








