import os, subprocess, sys, random

if(len(sys.argv) > 2):
	
	print "set terminal postscript eps color enhanced"
	print "set output \""+ sys.argv[2]+ "\""

	if sys.argv[1] == "fuel":
		for i in range(0,100):
			print "plot \"4.dat\" using 1:3 with lines, \"4.dat\" using 1:3 with lines"
	elif sys.argv[1] == "speed":
			for i in range(0,100):
		print "plot \"4.dat\" using 1:3 with lines, \"4.dat\" using 1:3 with lines"
else:
	print "to few arg"


n
