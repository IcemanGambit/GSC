import math
from datetime import datetime, date, time
tjfile = open("ture3.sql", "r")
line = tjfile.readline()

data = {}
parsing ="Header"


def distance(x1,y1,x2,y2):
	return math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )

linec = 0
while (line ):
	linec+=1
	if line.find("COPY ture3 (st_makepoint, rtime, carid, trajid, xcoord, ycoord, dir, segmentkey, unixtime) FROM stdin;") >= 0:
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
		temp3 = line.split("\t")	
		temp = temp3[1:len(temp3)]
		
		if not temp[2] in data:
			temp2 = temp[0].split(" ")
			dt = temp2[0].split("-")
			d = date(int(dt[0]), int(dt[1]), int(dt[2]))
			tt = temp2[1].split(":")
			t = time(int(tt[0]), int(tt[1]))
			mydate = datetime.combine(d, t)
			
			if( not mydate.weekday == 5 and not mydate.weekday == 6 ) and mydate.hour >= 10 and mydate.hour <= 14:
				data[temp[2]] = [int(temp[7]),[int(temp[3]),int(temp[4])],0,[]]  #[lasttime, [lastX,lastY], lastdist ,[]] 
	
		if temp[2] in data:
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

