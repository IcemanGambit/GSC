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
				lanes = []	
				for lane in i[0]:				
					lanes.append(lane[:lane.rfind('_')])
	
				if len(route) > egdeId + 1 and route[egdeId] in lanes and route[egdeId+1] in lanes :
					TLs.append([tl, route[egdeId], route[egdeId+1]]) #TODO: Same as below. Redundant?
					break

	TLOnRoute[vhId] = TLs
	return TLOnRoute[vhId]
	
def visitTrafficLight(vhId):
	if len(TLOnRoute[vhId]) > 0:
		TLOnRoute[vhId].pop(0)
