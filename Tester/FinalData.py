import os, subprocess, sys, random

temp = []

for i in range(1,30):
	if os.path.exists(sys.argv[1] + "tp0c"+str((float(i)/10)).replace(".","_")):
		temp.append(i)

for j in [0,10,50,100]:
	f = open(sys.argv[1] + "avg" + str(j) + ".dat",'w')
	for i in temp:
		op = open(sys.argv[1]  + "tp0c"+str((float(i)/10)).replace(".","_") + "/" + str(j) +"/avg.dat",'r')
		f.write(str(float(i)/10) +" " + op.read())
		op.close()
	f.close()
