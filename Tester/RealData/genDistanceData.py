import math
tjfile = open("trajectories_nykarvej_ostrealle.sql", "r")
line = tjfile.readline()

data = {}
parsing ="Header"


def distance(x1,y1,x2,y2):
	return math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )

linec = 0
while (line ):
	linec+=1
	if line.find("COPY trajectories_nykarvej_ostrealle (rtime, carid, trajid, xcoord, ycoord, dir, segmentkey, unixtime) FROM stdin;") >= 0:
		parsing = "Data"
		line = tjfile.readline()
		continue;
	
	if parsing == "Header":
		line = tjfile.readline()
		continue
	
	if parsing == "Data": 
		if line.find("\.") >= 0:
			parsing = "Footer"

	if parsing == "Data":
		temp = line.split("\t")	
		

		
		if not temp[2] in data:
			data[temp[2]] = [int(temp[7]),[int(temp[3]),int(temp[4])],0,[]]  #[lasttime, [lastX,lastY], lastdist ,[] 
	
		diffdistance = distance(data[temp[2]][1][0],data[temp[2]][1][1], int(temp[3]),int(temp[4]))

		data[temp[2]][3].append([int(temp[7])-data[temp[2]][0], data[temp[2]][2] + diffdistance ])



		line = tjfile.readline()
		continue
	line = tjfile.readline()

i = -1
for v in data.values():
	i+=1
	out = open("data/" + str(i) + ".dat", "w")
	for j in v[3]:
		out.write(str(j[0]) + "\t" + str(j[1]) + "\n")
	out.flush()

