import traci

TLOnRoute = {}

"""
	getTrafficLightsOnRoute(string) -> [[string, string],]
	
	Returns all future traffic lights.
	Format is: id, incomming edges, outgoing edges.
	
	Note: Requires visitTrafficLight(vhId) to be called afterwards.
"""
def getTrafficLightsOnRoute(vhId):
	#If already recorded
	if vhId in TLOnRoute:
		return TLOnRoute[vhId]

	route = traci.vehicle.getRoute(vhId)
	edge = traci.vehicle.getRoadID(vhId)

	#Find where to start in the route, such that we only find future traffic lights
	startId = -1
	if edge in route:
		startId = route.index(edge)
	else:
		return None
	
	TLs = []
	for edgeId in range(startId, len(route)): #Loop over edges in route
		for tl in traci.trafficlights.getIDList(): #Loop over all traffic lights
			for i in traci.trafficlights.getControlledLinks(tl): #Loop over all links at traffic light
				lanes = []	
				for lane in i[0]: #Loop over lanes in link		
					lanes.append(lane[:lane.rfind('_')]) #Add first part of lane id which is the same as the road id. A hack as routes are edges and traffic lights are lanes.
				#If incomming edge and outgoing edge is in a link for this traffic light
				# -> add and loop at next traafic light
				if len(route) > edgeId + 1 and route[edgeId] in lanes and route[edgeId+1] in lanes :
					TLs.append([tl, route[edgeId], route[edgeId+1]])
					break

	#Record result in order to reduce complexity of the next call.
	TLOnRoute[vhId] = TLs
	return TLOnRoute[vhId]

"""
	visitTrafficLight(string) ->
	
	Pops first traffic light from traffic lights on route.
"""
def visitTrafficLight(vhId):
	if len(TLOnRoute[vhId]) > 0:
		TLOnRoute[vhId].pop(0)
