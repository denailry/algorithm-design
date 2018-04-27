n = 0;
adjacencymatrix = [];
distancematrix = [];

def init(nVertex, distance, adjacency):
	global n, adjacencymatrix, distancematrix;
	n = nVertex;
	adjacencymatrix = adjacency;
	distancematrix = distance;

def solve(start, goal):
	candidateList = [];

	j = 0;
	for adjacency in adjacencymatrix[start]:
		if (adjacency == 1):
			candidateList.append({"vertex": j, "costSoFar": distancematrix[start][j], "routes": [start, j]});
		j = j + 1;
	chosen = min(candidateList, key = lambda candidate : (candidate['costSoFar'] + distancematrix[candidate['vertex']][goal]));
	candidateList.remove(chosen);

	while(distancematrix[chosen['vertex']][goal] != 0):
		j = 0;
		for adjacency in adjacencymatrix[chosen['vertex']]:
			if ((adjacency == 1) and (j not in chosen['routes'])):
				cRoutes = [];
				for vertex in chosen["routes"]:
					cRoutes.append(vertex); 
				cRoutes.append(j);
				candidateList.append({"vertex": j, "costSoFar": chosen['costSoFar'] + distancematrix[start][j], "routes": cRoutes});
			j = j + 1;
		chosen = min(candidateList, key = lambda candidate: (candidate['costSoFar'] + distancematrix[candidate['vertex']][goal]));
		candidateList.remove(chosen);

	result = {'routes': chosen['routes'], 'distance': chosen['costSoFar']};

	return result;
