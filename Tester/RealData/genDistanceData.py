import math, random, os
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
		line = temp3[1:len(temp3)]
		tId = line[2]
		
		xCoord = int(line[3])
		yCoord = int(line[4])
		
		if not tId in data:
			mydatetime = line[0].split(" ")
			dt = mydatetime[0].split("-")
			d = date(int(dt[0]), int(dt[1]), int(dt[2]))
			tt = mydatetime[1].split(":")
			t = time(int(tt[0]), int(tt[1]))
			mydate = datetime.combine(d, t)
			
			if( not mydate.weekday == 5 and not mydate.weekday == 6 ) and mydate.hour >= 10 and mydate.hour <= 14:
				data[tId] = [int(line[7]),[xCoord,yCoord],[],[],[],[]]  
				#[firsttime, 
				#[lastX,lastY], 
				#[[time1, distance1], [time2, distance2], ], 
				#[[time1, diffDistance1], [time2,diffDistance2], ], 
				#[[time1, acc1], [time2,acc2], ]
				#[[time1, speed1], [time2,speed2], ]]

		if tId in data:
			diffdistance = distance(data[tId][1][0],data[tId][1][1], xCoord,yCoord)

			data[tId][1] = [xCoord,yCoord]

			newTotalDist= 0
			if(len(data[tId][2]) > 0):
				newTotalDist = data[tId][2][len(data[tId][2]) - 1][1] + diffdistance

			data[tId][2].append([int(line[7])-data[tId][0], newTotalDist])
		
			data[tId][3].append([int(line[7])-data[tId][0], diffdistance])
			sum1 = 0
			if len(data[tId][3][-6:]) > 0:
				for i in data[tId][3][-6:]:
					sum1+=i[1]
				sum1 = sum1/len(data[tId][3][-6:])

			sum2 = 0
			if len(data[tId][3][-7:-1])> 0:
				for i in data[tId][3][-7:-1]:
					sum2+=i[1]
				sum2 = sum2/len(data[tId][3][-7:-1])

			acc = (sum1 - sum2)
			
			data[tId][4].append([int(line[7])-data[tId][0]- 3, acc ])
			
			speed = 0
			sixlast = data[tId][3][-6:]
			if len(sixlast)> 0:
				for i in sixlast:
					speed+=i[1]
				speed = speed/len(sixlast)

			data[tId][5].append([int(line[7]) - data[tId][0] - 3, speed*3.6])
			

		line = tjfile.readline()
		continue
	line = tjfile.readline()

i = -1
values = random.sample(range(0,len(data)), 20)
for root, dirs, files in os.walk('speed/'):
    for f in files:
    	os.unlink(os.path.join(root, f))


for v in data.values():
	i+=1
	out = open("distance/" + str(i) + ".dat", "w")
	for j in v[2]:
		out.write(str(j[0]) + "\t" + str(j[1]) + "\n")
	out.flush()

	out = open("acc/" + str(i) + ".dat", "w")
	for j in v[4]:
		out.write(str(j[0]) + "\t" + str(j[1]) + "\n")
	out.flush()

	#if i in values:
	out = open("speed/" + str(i) + ".dat", "w")
	for j in v[5]:
		out.write(str(j[0]) + "\t" + str(j[1]) + "\n")
	out.flush()
