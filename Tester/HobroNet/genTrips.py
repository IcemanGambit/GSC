import sys,random

if sys.argv[1] == "":
	print "Please enter the name of your files"
	sys.exit()

noTrips = 0
places = [['Main1toJu1', 'Ju3toOst1']]

trips = open(sys.argv[1]+"/trips.xml", "w")

print >> trips, "<trips>"
TID=0 
interval = 2
for i in range(0,noTrips*interval, interval):
	placeID = int(random.uniform(0,len(places)))
	
	print >> trips, '	<trip id="%i" from="%s" to="%s" depart="%i"/>' % (TID,places[placeID][0], places[placeID][1], i)
	TID += 1

print >> trips, '</trips>'
trips.close()
