import os, subprocess, sys, random

dataset = "default"
if(len(sys.argv) > 2):
	
	print "set terminal postscript eps color enhanced"
	print "set output \""+ sys.argv[2]+ "\""

	if sys.argv[1] == "fuel":
		for i in range(0,100):
			print "plot \"4.dat\" using 1:3 with lines, \"4.dat\" using 1:3 with lines"
	elif sys.argv[1] == "speed":
		for i in range(0,100):
			print "plot \"4.dat\" using 1:3 with lines, \"4.dat\" using 1:3 with lines"
	elif sys.argv[1] == "distance_0":
		fileIN = open("TestResults/" + dataset+ "/0/routeList.dat", "r")
		line = fileIN.readline()
		route = ""
		while line:
			if(line.find("18_N, 18_N.-60, 17_N, 15_S, 15_S.-30, 13_N, 13_N.-40, 11_N, 8_N, 7_N, 7_N.-60, 5_N, 4_N, 4_N.-60, 1_N") >=0):			
				route = line[0:line.find(":")]
			line = fileIN.readline()
		plots = ""
		for i in range(0,10):
			if i != 0:
				plots += ","
			datafile = "TestResults/" + dataset+ "/0/"+ route+ "/"+ str(i) + ".dat"
			plots += "\"" + datafile + "\" using 1:4 with lines"	
		print "plot" + plots
else:
	print "to few arg"

