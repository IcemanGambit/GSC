import os, subprocess, sys, random

dataset = "default"
if(len(sys.argv) > 2):

	fileIN = open("TestResults/" + dataset+ "/0/routeList.dat", "r")
	line = fileIN.readline()
	route = ""
	while line:
		if(line.find("18_N, 18_N.-60, 17_N, 15_S, 15_S.-30, 13_N, 13_N.-40, 11_N, 8_N, 7_N, 7_N.-60, 5_N, 4_N, 4_N.-60, 1_N") >=0):			
			route = line[0:line.find(":")]
		line = fileIN.readline()

	
	print "set terminal postscript eps color enhanced"
	print "set output \""+ sys.argv[2]+ "\""
	print "unset key"
	print "set xrange [0:]"
	if sys.argv[1] == "fuel":
		print "set boxwidth 0.5 absolute"
		print "plot \"TestResults/" + dataset + "/0/" + route+ "/totalFuel.dat\" using ($1+0.25):2 with boxes fill solid lc rgb \"red\", \"TestResults/" + dataset + "/100/" + route+ "/totalFuel.dat\" using ($1-0.25):2 with boxes fill solid lc rgb \"blue\", `head -1 \"TestResults/" + dataset + "/0/" + route+ "/avg.dat\" | awk '{print $2}'` lt 1 lw 5 lc rgb \"red\", `head -1 \"TestResults/" + dataset + "/100/" + route+ "/avg.dat\" | awk '{print $2}'` lt 1 lw 5 lc rgb \"blue\""
		print "unset boxwidth"
	elif sys.argv[1] == "speed":
		for i in range(0,100):
			print "plot \"4.dat\" using 1:3 with lines, \"4.dat\" using 1:3 with lines"
	elif sys.argv[1].find("distance") == 0:
		datasetPercentage = sys.argv[1][sys.argv[1].find("_")+1:]
		plots = ""
		for i in range(0,1000):
			datafile = "TestResults/" + dataset+ "/" +datasetPercentage+ "/"+ route+ "/"+ str(i) + ".dat"
			if(not os.path.exists(datafile)):
				break
			if i != 0:
				plots += ","
			
			plots += "\"" + datafile + "\" using 1:2 with lines"
		if(plots == ""):
			print "ERROR dataset "+datasetPercentage+" do not exist"
			sys.exit(1)
		print "plot" + plots
	elif sys.argv[1].find("speed") == 0:
		datasetPercentage = sys.argv[1][sys.argv[1].find("_")+1:]
		plots = ""
		for i in range(0,10):
			datafile = "TestResults/" + dataset+ "/" +datasetPercentage+ "/"+ route+ "/"+ str(i) + ".dat"
			if(not os.path.exists(datafile)):
				break
			if i != 0:
				plots += ","
			plots += "\"" + datafile + "\" using 1:3 with lines lt 1 lc "+ str(i+1)+" "
		if(plots == ""):
			print "ERROR dataset "+datasetPercentage+" do not exist"
			sys.exit(1)
		print "plot" + plots
else:
	print "to few arg"

