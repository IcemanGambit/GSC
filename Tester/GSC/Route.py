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
	
	for egdeId in range(startId, len(route)): #Loop over egdes in route
		for tl in traci.trafficlights.getIDList(): #Loop over all traffic lights
			for i in traci.trafficlights.getControlledLinks(tl): #Loop over all links at traffic light
				for TLlane in i[0]: #Loop over all lanes in link
					if route[egdeId] == TLlane.split("_")[0]:#We are at this lane
						if len(TLs) > 0 and not TLs[len(TLs)-1][0] == tl:
							TLs.append([tl, route[egdeId-1], route[egdeId]]) #TODO: Same as below. Redundant?
						elif len(TLs) > 0:
							TLs[len(TLs)-1] =[tl, route[egdeId-1], route[egdeId]]
						else: 
							TLs.append([tl, route[egdeId-1], route[egdeId]])
	TLOnRoute[vhId] = TLs
	return TLOnRoute[vhId]
	
def visitTrafficLight(vhId):
	if len(TLOnRoute[vhId]) > 0:
		TLOnRoute[vhId].pop(0)
