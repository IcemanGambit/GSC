ODfile = open("OD_out.txt", "r")
line = ODfile.readline()
s = ""

frommap = {}
tomap = {}

frommap["kong_christian"] = "2_O"
frommap["Vesterbro"] = "1_S"
frommap["kong_christian"] = "2_O"
frommap["ostre_alle"] = "3_V"
frommap["Sondre_skovvej"] = "6_O"
frommap["Romersvej_1"] = "9_V"
frommap["Romersvej_2"] = "9_V"
frommap["Mollerparkvej"] = "12_O"
frommap["parkvej"] = "16_O"
frommap["Vestre_alle"] = "19_O"
frommap["hobrovej"] = "18_N"
frommap["ny_kervej"] = "21_V"


tomap["kong_christian"] = "2_V"
tomap["Vesterbro"] = "1_N"
tomap["kong_christian"] = "2_V"
tomap["ostre_alle"] = "3_O"
tomap["Sondre_skovvej"] = "6_V"
tomap["Romersvej_1"] = "10_O"
tomap["Romersvej_2"] = "10_O"
tomap["Mollerparkvej"] = "12_V"
tomap["parkvej"] = "16_V"
tomap["Vestre_alle"] = "19_V"
tomap["hobrovej"] = "18_S"
tomap["ny_kervej"] = "21_O"

l = frommap.values()
l += tomap.values()
OD = []
print "places = " + str(l)
for i in range(0,len(l)):
	OD.append([])
	for j in range(0,len(l)):
		OD[i].append(0)


line = ODfile.readline()
while line:
	
	temp = line.split(";")
	if temp[0] == temp[1]:
		line = ODfile.readline()
		continue
	e= l.index(frommap[temp[0]])
	r = l.index(tomap[temp[1]])
	OD[e][r] = int(temp[3])
	#print frommap[temp[0]] + tomap[temp[1]]

	line = ODfile.readline()
s = "ODmatrix = ["
firstI = True
for i in OD:
	if not firstI:
		s+= ","
	firstI = False
	s+= "["
	firstJ = True
	for j in i:
		if not firstJ:
			s+= ","
		s+= str(j)
		firstJ = False
	s+= "]"
s+= "]"
print s












	
