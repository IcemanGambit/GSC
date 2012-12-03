import os, subprocess, sys, random

path = sys.argv[1]
if path[-1] != "/":
	path += "/"

pathNet = path + "Data.net.xml"

pathExtra = path + "Data.tll2.xml"

f = open(pathNet,'r')
extra = open(pathExtra,'r')
o = ""

line = f.readline()

foundIt = False
while line:
	if(line.find("<junction") >= 0 and not foundIt):
		o+=extra.read()
		foundIt = True
		extra.close()
	o+= line
	line = f.readline()
f.close()

out = open(pathNet,'w')
out.write(o)
out.close()
