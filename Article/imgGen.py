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
	print "set output \"images/"+ sys.argv[2]+ "\""
	print "unset key"

	if sys.argv[1] == "fuel":
		print "set ylabel 'Fuel Consumption (ml)'"
		print "set xlabel 'Vehicles'"
		print "set xrange [0:]"
		print "set boxwidth 0.5 absolute"
		datafile1 = "\"TestResults/" + dataset + "/0/" + route+ "/totalFuel.dat\""
		datafile2 = "\"TestResults/" + dataset + "/100/" + route+ "/totalFuel.dat\""
		
		print "plot "+ datafile1 + " using ($1+0.25):2 with boxes fill solid lc 1, "+ datafile2 + " using ($1-0.25):2 with boxes fill solid lc 2, `head -1 "+ datafile1 + " | awk '{print $2}'` lt 1 lw 5 lc 1, `head -1 "+ datafile2 + " | awk '{print $2}'` lt 1 lw 5 lc 2"
	elif sys.argv[1].find("distance") == 0:
		print "set xrange [0:300]"
		print "set yrange [0:1400]"
		datasetPercentage = sys.argv[1][sys.argv[1].find("_")+1:]
		print "set ylabel 'Distance (m)'"
		print "set xlabel 'Time (s)'"
		plots = ""
		for i in range(0,1000):
			datafile = "TestResults/" + dataset+ "/" +datasetPercentage+ "/"+ route+ "/"+ str(i) + ".dat"
			if(not os.path.exists(datafile)):
				break
			if i != 0:
				plots += ","
			
			plots += "\"" + datafile + "\" using 1:2 with lines lt 1 lc "+ str(i+1)+" "
		if(plots == ""):
			print "ERROR dataset "+datasetPercentage+" do not exist"
			sys.exit(1)
		print "plot" + plots
	elif sys.argv[1].find("speed") == 0:
		print "set xrange [0:300]"
		print "set yrange [0:20]"
		datasetPercentage = sys.argv[1][sys.argv[1].find("_")+1:]
		print "set ylabel 'Speed (km/h)'"
		print "set xlabel 'Time (s)'"
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
	elif sys.argv[1].find("stops") == 0:
		datasetPercentage = sys.argv[1][sys.argv[1].find("_")+1:]
		print "set yrange [0:]"
		print "set ylabel 'Distance (m)'"
		print "set xlabel 'Vehicles'"
		plotstring = "plot "
		for i in range(0,10):
			datafile = "TestResults/" + dataset+ "/" +datasetPercentage + "/stops" + str(i) + ".dat"
			if(os.path.exists(datafile)):
				plotstring += "\"" + datafile + "\" with impulses lt 1 lw 3 lc " + str(i+1) + ", \"" + datafile + "\" with points pt " + str(i+1) + " lc " + str(i+1) + ","
		print plotstring[:len(plotstring)-1]
else:
	print "to few arg"

