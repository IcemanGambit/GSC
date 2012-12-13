import os, sys ,math

stopList = []
speedList = []
timeList = []
FreeFlow = 1550/(60/3.6)
for f in os.listdir(sys.argv[1]):

	if f.find("avg") >= 0 or f.find("total") >=0:
		continue
	data = open(sys.argv[1] + f)

	speed = 0
	stopping = False
	stopCount = 0
	avgSpeed = 0
	linecount = 0
	line = data.readline()
	time = 0
	i = 0
	while line:
		line = line.strip()
		line2 = line.split("\t")
		
		
		if (len(line2) > 2): 
			i = 2	#sumo
		else:
			i = 1	#real data
			
		if int(line2[0]) >= 0:
			avgSpeed += float(line2[i])
			linecount+= 1
			time +=1
			if float(line2[i]) < 10 and stopping == False:
				stopping = True
				stopCount += 1
			if float(line2[i]) > 15 and stopping == True:
				stopping = False
		line = data.readline()

	if i == 1:
		time -= 3 #fix for the smoothing of real data
	time -=FreeFlow
	speedList.append(avgSpeed/linecount)
	stopList.append(float(stopCount))
	timeList.append(float(time))


stopavg = sum(stopList)/len(stopList)

print "avg stop " + str(stopavg)
stdStopList = []
for i in stopList:
	stdStopList.append((i-stopavg) **2)
Stdiv = math.sqrt(sum(stdStopList)/(len(stopList)))
print "STDEV stop " + str(Stdiv)

speedavg = sum(speedList)/len(speedList)
print "avg speed " + str(speedavg)

stdspeedList = []
for i in speedList:
	stdspeedList.append((i-speedavg) **2)
Stdiv = math.sqrt(sum(stdspeedList)/(len(speedList)))
print "STDEV speed " + str(Stdiv)

timeavg = sum(timeList)/len(timeList)
print "avg time " + str(timeavg)

stdtimeList = []
for i in timeList:
	stdtimeList.append((i-timeavg) **2)
Stdiv = math.sqrt(sum(stdtimeList)/(len(timeList)))
print "STDEV time " + str(Stdiv)

print "FreeFlow "+str(FreeFlow)
