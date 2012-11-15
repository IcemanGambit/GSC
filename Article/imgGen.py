import os, subprocess, sys, random

dataset = "default"
if(len(sys.argv) > 2):
	
	print "set terminal postscript eps color enhanced"
	print "set output \""+ sys.argv[2]+ "\""
	print "unset key"
	if sys.argv[1] == "fuel":
		for i in range(0,100):
			print "plot \"4.dat\" using 1:3 with lines, \"4.dat\" using 1:3 with lines"
	elif sys.argv[1] == "speed":
		for i in range(0,100):
			print "plot \"4.dat\" using 1:3 with lines, \"4.dat\" using 1:3 with lines"
	elif sys.argv[1].find("distance") == 0:
		fileIN = open("TestResults/" + dataset+ "/0/routeList.dat", "r")
		line = fileIN.readline()
		route = ""
		datasetPercentage = sys.argv[1][sys.argv[1].find("_")+1:]
		while line:
			if(line.find("18_N, 18_N.-60, 17_N, 15_S, 15_S.-30, 13_N, 13_N.-40, 11_N, 8_N, 7_N, 7_N.-60, 5_N, 4_N, 4_N.-60, 1_N") >=0):			
				route = line[0:line.find(":")]
			line = fileIN.readline()
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

else:
	print "to few arg"

