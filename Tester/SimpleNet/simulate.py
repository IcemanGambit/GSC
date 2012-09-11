import os, subprocess, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import traci

if len(sys.argv) > 1:
	example = sys.argv[1]
else:
	print "Please enter the name of your files"
	sys.exit()
	
sumoBinary = "../sumo-gui"
PORT = 8813

#Run SUMO and TraCI
process = subprocess.Popen("%s -c %s" % (sumoBinary, example+".sumocfg"), shell=True, stdout=sys.stdout)
traci.init(PORT)

step = 0
while step==0 or traci.simulation.getMinExpectedNumber() > 0:
	traci.simulationStep()
	
	#TraCI control
	print traci.trafficlights.getCompleteRedYellowGreenDefinition("Ju1")
	print 
	
	
	
	step+=1

#Clean up
traci.close()
sys.stdout.flush()








