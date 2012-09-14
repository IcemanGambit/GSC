import traci

TLOnRoute = {}

"""
	getTrafficLightsOnRoute(string) -> [[string, string],]
"""
def getTrafficLightsOnRoute(vhId):
	if vhId in TLOnRoute:
		return TLOnRoute[vhId]

	route = traci.vehicle.getRoute(vhId)
	egde = traci.vehicle.getRoadID(vhId)

	startId = -1
	if egde in route:
		startId = route.index(egde)
	else:
		return None
	
	TLs = []
	
	for egdeId in range(startId, len(route)):
		for tl in traci.trafficlights.getIDList():
			for i in traci.trafficlights.getControlledLinks(tl):
				for TLlane in i[0]:
					if route[egdeId] == TLlane.split("_")[0]:
						if len(TLs) > 0 and not TLs[len(TLs)-1][0] == tl:
							TLs.append([tl, route[egdeId-1], route[egdeId]])
						elif len(TLs) > 0:
							TLs[len(TLs)-1] =[tl, route[egdeId-1], route[egdeId]]
						else: 
							TLs.append([tl, route[egdeId-1], route[egdeId]])
	TLOnRoute[vhId] = TLs
	return TLOnRoute[vhId]
	
def visitTrafficLight(vhId):
	if len(TLOnRoute[vhId]) > 0:
		TLOnRoute[vhId].pop(0)
