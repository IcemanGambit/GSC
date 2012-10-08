import os, subprocess, sys, random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import traci 
import GSC
sumoBinary = "sumo-gui"
PORT = 8813

#Run SUMO and TraCI
process = subprocess.Popen("%s -c %s" % (sumoBinary, sys.argv[1] + "/Data.sumocfg"), shell=True, stdout=sys.stdout)
traci.init(PORT)

#Insert string integers of vehicles to test specically. Set tesPercet to False.
GSCvehIds = []

#Finding the vehicles to test
testPercent = False
percent = 10
total = 500
vehicles = random.sample(xrange(total), total*percent/100)

step = 0
while step==0 or traci.simulation.getMinExpectedNumber() > 0:
	traci.simulationStep()
	for v in traci.vehicle.getIDList():
		if (testPercent and int(v) in vehicles) or v in GSCvehIds:
			speed = GSC.Vehicle.getRecommentedSpeed(v, 200, 400000)
			traci.vehicle.setMaxSpeed(v, speed)
	#GSC.Test.processDataCollection()
	step+=1
#GSC.Test.flushDataCollection()

#Clean up
traci.close()
sys.stdout.flush()








