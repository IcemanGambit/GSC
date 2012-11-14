import os, subprocess, sys, random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import traci 
import GSC
if len(sys.argv) < 5:
	print "Simulate: to few arguments"
	sys.exit(1)


sumoBinary = "sumo"
if sys.argv[2] == "gui":
	sumoBinary = "sumo-gui"
	print "running sumo with gui and " + sys.argv[3] + "% using system"
else:
	print "running sumo with " + sys.argv[3] + "% using system"
PORT = 8813


#Run SUMO and TraCI
process = subprocess.Popen("%s -c %s  --lanechange.allow-swap " % (sumoBinary, sys.argv[1]  + "/Data.sumocfg"), shell=True, stdout=sys.stdout)
traci.init(PORT)

#Get total number of vehicles TODO: This is an ugly hack
with open(sys.argv[1] + "/trips.xml") as f:
	for i, l in enumerate(f):
		pass
noVehicles = i -1
f.close()

#Insert string integers of vehicles to test specically. Set tesPercet to False.
GSCvehIds = ['253']

#Finding the vehicles to test
testPercent = True
percent = int(sys.argv[3])
print "Save to Test/"+sys.argv[4]+"/"+str(percent)+""
controlledVehicles = random.sample(xrange(noVehicles), noVehicles*percent/100)

step = 0
while step==0 or traci.simulation.getMinExpectedNumber() > 0:
	traci.simulationStep()
	for v in traci.vehicle.getIDList():
		if (testPercent and int(v) in controlledVehicles) or v in GSCvehIds:
			speed = GSC.Vehicle.getRecommentedSpeed(v, 2000, 400000)
			traci.vehicle.setSpeed(v, speed)
	GSC.Test.processDataCollection()
	step+=1

GSC.Test.flushDataCollection(percent,sys.argv[4])

#Clean up
traci.close()
sys.stdout.flush()








