import os, subprocess, sys, random

fuelRouteYMax = "200"
fuelTotalYMax = "250"
distanceYMax = "1600"
speedMaxY = "80"

if(len(sys.argv) > 3):
	dataset = sys.argv[3]
	fileIN = open("TestResults/" + dataset+ "/0/routeList.dat", "r")
	line = fileIN.readline()
	route = ""
	while line:
		if(line.find("18_N, 18_N.-60, 17_N, 15_S, 15_S.-30, 13_N, 13_N.-40, 11_N, 8_N, 7_N, 7_N.-60, 5_N, 4_N, 4_N.-60, 1_N") >=0):			
			route = line[0:line.find(":")]
		line = fileIN.readline()

	
	print "set terminal png size 700,400"
	print "set output \"images/"+sys.argv[3]+"/"+ sys.argv[2]+ "\""
	print "unset key"

	if sys.argv[1] == "fuelRoute":
		print "set ylabel 'Fuel Consumption (ml)'"
		print "set xlabel 'Vehicles'"
		print "set yrange[0:" + fuelRouteYMax + "]"
		print "set boxwidth 0.5 absolute"
		print "unset xtics"
		datafile1 = "\"TestResults/" + dataset + "/0/" + route
		datafile2 = "\"TestResults/" + dataset + "/100/" + route
		print "plot "+ datafile1 + "/totalFuel.dat\"" + " using ($1+0.25):2 with boxes fill solid lc rgb \"blue\", " + datafile2 + "/totalFuel.dat\" using ($1-0.25):2 with boxes fill solid lc rgb \"green\", `head -1 " + datafile1 + "/avg.dat\" | awk '{print $2}'` lt 1 lw 5 lc rgb \"blue\", `head -1 "+ datafile2 + "/avg.dat\" | awk '{print $2}'` lt 1 lw 5 lc rgb \"green\""
	
	elif sys.argv[1].find("fuel_") > 0:
		conType = sys.argv[1][:sys.argv[1].find("_")]
		if conType == "controlled":
			color = "\"green\""
		else:
			color = "\"blue\""
		percent = sys.argv[1][sys.argv[1].rfind("_")+1:]
		print "set ylabel 'Fuel Consumption (ml)'"
		print "set xlabel 'Vehicles'"
		print "set boxwidth 0.5 absolute"
		print "set yrange[0:" + fuelRouteYMax + "]"
		print "unset xtics"
		datafile = "\"TestResults/" + dataset + "/"+percent+"/" + route+ "/"+conType
		print "plot "+ datafile+"/totalFuel.dat\"" + " with boxes fill solid lc rgb " + color + ", `head -1 "+ datafile+"/avg.dat\"" + " | awk '{print $2}'` lt 1 lw 5 lc rgb " + color
		
	elif sys.argv[1] == "fuelTotal":
		print "set ylabel 'Fuel Consumption (ml)'"
		print "set xlabel 'Vehicles'"
		print "set xrange [0:]"
		print "set yrange [0:" + fuelTotalYMax + "]"
		print "set boxwidth 0.5 absolute"
		print "unset xtics"
		datafile = "\"TestResults/" + dataset
		print "plot "+ datafile + "/0/totalFuel.dat\"" + " using ($1+0.25):2 with boxes fill solid lc rgb \"blue\", " + datafile + "/100/totalFuel.dat\" using ($1-0.25):2 with boxes fill solid lc rgb \"green\", `head -1 " + datafile + "/0/avg.dat\" | awk '{print $2}'` lt 1 lw 5 lc rgb \"blue\", `head -1 "+ datafile + "/100/avg.dat\" | awk '{print $2}'` lt 1 lw 5 lc rgb \"green\""
	
	elif sys.argv[1].find("_fuelTotal") > 0:
		conType = sys.argv[1][:sys.argv[1].find("_")]
		if conType == "controlled":
			color = "\"green\""
		else:
			color = "\"blue\""
		percent = sys.argv[1][sys.argv[1].rfind("_")+1:]
		print "set ylabel 'Fuel Consumption (ml)'"
		print "set xlabel 'Vehicles'"
		print "set xrange [0:]"
		print "set yrange [0:" + fuelTotalYMax + "]"
		print "set boxwidth 0.5 absolute"
		print "unset xtics"
		datafile = "\"TestResults/" + dataset + "/"+percent + "/" + conType
		print "plot "+ datafile +"/totalFuel.dat\""+ " using 1:2 with boxes fill solid lc rgb " + color + ", `head -1 "+ datafile +"/avg.dat\"" + " | awk '{print $2}'` lt 1 lw 5 lc rgb " + color
		
	elif sys.argv[1].find("combinedFuel") == 0:
		print "set boxwidth 0.9"
		print "set ylabel 'Fuel Consumption (ml)'"
		print "set xlabel 'Percentage using the system'"
		print "set xtics (\"0\" 0, \"10\" 1, \"50\" 2, \"10\" 3, \"50\" 4, \"100\" 5)"
		print "set yrange [0:" + fuelRouteYMax + "]"
		print "set key default"
		output = "plot "
		output += "\"TestResults/" + dataset + "/0/" + route + "/uncontrolled/avg.dat\" using (0):2 with boxes fill solid lc rgb 'blue' title 'Vehicles without system',"
		output += "\"TestResults/" + dataset + "/10/" + route + "/uncontrolled/avg.dat\" using (1):2 with boxes fill solid lc rgb 'blue' notitle,"
		output += "\"TestResults/" + dataset + "/50/" + route + "/uncontrolled/avg.dat\" using (2):2 with boxes fill solid lc rgb 'blue' notitle,"
		output += "\"TestResults/" + dataset + "/10/" + route + "/controlled/avg.dat\" using (3):2 with boxes fill solid lc rgb 'green' title 'Vehicles with system',"
		output += "\"TestResults/" + dataset + "/50/" + route + "/controlled/avg.dat\" using (4):2 with boxes fill solid lc rgb 'green' notitle,"
		output += "\"TestResults/" + dataset + "/100/" + route + "/controlled/avg.dat\" using (5):2 with boxes fill solid lc rgb 'green' notitle"
		print output
		
	elif sys.argv[1].find("combinedTime") == 0:
		print "set boxwidth 0.9"
		print "set ylabel 'Average travel time (s)'"
		print "set xlabel 'Percentage using the system'"
		print "set xtics (\"0\" 0, \"10\" 1, \"50\" 2, \"100\" 3)"
		print "set yrange [0:170]"
		output = "plot "
		output += "\"TestResults/" + dataset + "/0/avg.dat\" using (0):1 with boxes fill solid lc rgb '#778899',"
		output += "\"TestResults/" + dataset + "/10/avg.dat\" using (1):1 with boxes fill solid lc rgb '#778899',"
		output += "\"TestResults/" + dataset + "/50/avg.dat\" using (2):1 with boxes fill solid lc rgb '#778899',"
		output += "\"TestResults/" + dataset + "/100/avg.dat\" using (3):1 with boxes fill solid lc rgb '#778899'"
		print output
	elif sys.argv[1].find("_combinedRouteTime") >= 0:
		temp = sys.argv[1][:sys.argv[1].find("_")]
		if temp != "":
			route = temp
		print "set boxwidth 0.9"
		print "set ylabel 'Average travel time (s)'"
		print "set xlabel 'Percentage using the system'"
		print "set xtics (\"0\" 0, \"10\" 1, \"50\" 2, \"100\" 3)"
		print "set yrange [0:]"
		output = "plot "
		output += "\"TestResults/" + dataset + "/0/"+ route+ "/avg.dat\" using (0):1 with boxes fill solid lc rgb '#778899',"
		output += "\"TestResults/" + dataset + "/10/"+ route+ "/avg.dat\" using (1):1 with boxes fill solid lc rgb '#778899',"
		output += "\"TestResults/" + dataset + "/50/"+ route+ "/avg.dat\" using (2):1 with boxes fill solid lc rgb '#778899',"
		output += "\"TestResults/" + dataset + "/100/"+ route+ "/avg.dat\" using (3):1 with boxes fill solid lc rgb '#778899'"
		print output
		
	elif sys.argv[1].find("acceleration") == 0:
		print "set y2label 'distance (m)'"
		print "set ylabel 'Acceleration (m/s^2)'"
		print "set boxwidth 1 absolute"
		print "set y2range [0:2000]"

		print "set yrange [-5:5]"
		print "set ytics nomirror"
		print "set y2tics nomirror"
		i=8
		datafile = "TestResults/" + dataset+ "/0/"+ route+ "/distance/" + str(i) + ".dat"
		print "plot\"TestResults/" + dataset+ "/0/"+ route + "/acc/" + str(i) + ".dat" + "\" with boxes fill solid lt 1,  \"" + datafile + "\" using 1:2 with lines lt 2 axes x1y2" 
		
	elif sys.argv[1].find("distance") > 0:
		datasetPercentage = sys.argv[1][sys.argv[1].rfind("_")+1:]
		conType = sys.argv[1][:sys.argv[1].find("_")]
		print "set xrange [0:400]"
		print "set yrange [0:" + distanceYMax + "]"
		print "set ylabel 'Distance (m)'"
		print "set xlabel 'Time (s)'"
		plots = ""
		counttotal = 0
		for i in range(0,2000):
			datafile = "TestResults/" + dataset+ "/" +datasetPercentage+ "/"+ route+ "/"+ conType + "/" + str(i) + ".dat"
			if(not os.path.exists(datafile)):
				continue
			counttotal+= 1
			if counttotal != 1:
				plots += ","
			
			plots += "\"" + datafile + "\" using 1:2 with lines lt 1 lc "+ str(counttotal+1)+" "
		if(plots == ""):
			print "ERROR dataset "+datasetPercentage+" do not exist"
			sys.exit(1)
		print "plot" + plots
		
	elif sys.argv[1].find("Reald") >= 0:
		print "set xrange [0:400]"
		print "set yrange [0:" + distanceYMax + "]"
		print "set ylabel 'Distance (m)'"
		print "set xlabel 'Time (s)'"
		plots = ""
		counttotal = 0
		for i in range(0,2000):
			datafile = "TestResults/" + dataset + "/0/"+ route + "/distance/" + str(i) + ".dat"
			if(not os.path.exists(datafile)):
				continue
			counttotal+= 1
			if counttotal != 1:
				plots += ","
			
			plots += "\"" + datafile + "\" using 1:2 with lines lt 1 lc "+ str(counttotal+1)+" "
		if(plots == ""):
			print "ERROR dataset do not exist"
			sys.exit(1)
		print "plot" + plots
	
	elif sys.argv[1].find("RealSpeed") >= 0:
		print "set xrange [0:400]"
		print "set yrange [0:" + speedMaxY + "]"
		print "set ylabel 'Speed (m)'"
		print "set xlabel 'Time (s)'"
		plots = ""
		counttotal = 0
		for i in range(0,2000):
			datafile = "TestResults/" + dataset + "/0/"+ route + "/speed/" + str(i) + ".dat"
			if(not os.path.exists(datafile)):
				continue
			counttotal+= 1
			if counttotal != 1:
				plots += ","
			
			plots += "\"" + datafile + "\" using 1:2 with lines lt 1 lc "+ str(counttotal+1)+" "
		if(plots == ""):
			print "ERROR dataset do not exist"
			sys.exit(1)
		print "plot" + plots
				
	elif sys.argv[1].find("speed")> 0:
		datasetPercentage = sys.argv[1][sys.argv[1].rfind("_")+1:]
		conType = sys.argv[1][:sys.argv[1].find("_")]
		print "set xrange [0:400]"
		print "set yrange [0:" + speedMaxY + "]"
		print "set ylabel 'Speed (km/h)'"
		print "set xlabel 'Time (s)'"
		plots = ""
		counttotal = 0
		for i in range(0,2000):
			datafile = "TestResults/" + dataset+ "/" +datasetPercentage+ "/"+ route+ "/"+ conType + "/" + str(i) + ".dat"
			if(not os.path.exists(datafile)):
				continue
			counttotal+= 1
			if counttotal != 1:
				plots += ","
			
			plots += "\"" + datafile + "\" using 1:3 with lines lt 1 lc "+ str(counttotal+1)+" "
			if counttotal > 15:
				break
		if(plots == ""):
			print "ERROR dataset "+datasetPercentage+" do not exist"
			sys.exit(1)
		print "plot" + plots
		
	elif sys.argv[1].find("stops") == 0:
		datasetPercentage = sys.argv[1][sys.argv[1].find("_")+1:]
		print "set yrange [-0.5:]"
		print "set ylabel 'Distance (m)'"
		print "set xlabel 'Vehicles'"
		plotstring = ""
		for i in range(0,20):
			datafile = "TestResults/" + dataset+ "/" +datasetPercentage + "/stops" + str(i) + ".dat"
			if(os.path.exists(datafile)):
				plotstring += "\"" + datafile + "\" with impulses lt 1 lw 3 lc " + str(i+1) + ", \"" + datafile + "\" with points pt " + str(i+1) + " lc " + str(i+1) + ","
		if(plotstring != ""):
			print "plot " + plotstring[:len(plotstring)-1]
else:
	print "to few arg"

