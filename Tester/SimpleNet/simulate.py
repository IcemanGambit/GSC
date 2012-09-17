import os, subprocess, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import traci 
import GSC
sumoBinary = "sumo-gui"
PORT = 8813

#Run SUMO and TraCI
process = subprocess.Popen("%s -c %s" % (sumoBinary, sys.argv[1] + "/Data.sumocfg"), shell=True, stdout=sys.stdout)
traci.init(PORT)

step = 0
GSCvehIds = ["1"]

while step==0 or traci.simulation.getMinExpectedNumber() > 0:
	traci.simulationStep()
	
	for v in traci.vehicle.getIDList():
		if v in GSCvehIds:
			speed = GSC.Vehicle.getRecommentedSpeed(v, 400000)
			print "speed " + v + " " + str(speed)
			traci.vehicle.setMaxSpeed(v, speed)
			traci.vehicle.setColor(v, (255,0,0,0))

	step+=1

#Clean up
traci.close()
sys.stdout.flush()








