import graphviz as gv


def createmapgraph(distance, adjacency):
	#Creates undirected graph with weight

	g = gv.Graph(format = 'svg');
	for i in range(0,len(distance)):
		g.node(chr(ord('A') + i));

	for i in range(0,len(adjacency)):
		for j in range(0,len(adjacency[i])):
			if(i < j and adjacency[i][j] == 1):
				g.edge(chr(ord('A') + i),chr(ord('A') + j), label = str(distance[i][j]));

	filename = g.render(filename = "mapgraph");
	print(filename);

	return;