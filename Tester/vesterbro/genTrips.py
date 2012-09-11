import sys,random

if sys.argv[1] == "":
	print "Please enter the name of your files"
	sys.exit()

noTrips = 1000
#-7778341, 8166502, 10061498, 9719736, 27442784, 10061498
places = [['-7778341', '8166502'],['26180719#0', '8166502'], ['9719736#0', '26180719#0'], ['8166502', '26180719#0']]

trips = open(sys.argv[1]+".xml", "w")

print >> trips, "<trips>"
TID=0 
for i in range(0,noTrips):
	placeID = int(random.uniform(0,len(places)))
	
	print >> trips, '	<trip id="%i" from="%s" to="%s" depart="%i"/>' % (TID,places[placeID][0], places[placeID][1], i)
	TID += 1

print >> trips, '</trips>'
trips.close()
