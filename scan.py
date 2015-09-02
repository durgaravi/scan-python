import math

def make_graph():
	f = open("graph.txt","r")
	lines = f.readlines()
	graph={}

	for i in lines:
		
		l = i[:-1].split("->")
		if len(l[1])==1:
			graph[l[0]] = {l[1]}
		else:
			graph[l[0]] = set(l[1].split(","))
		graph[l[0]].add(l[0])
		

	return graph

def get_similarity(graph,u,v):
	return len(graph[u].intersection(graph[v]))/math.sqrt((len(graph[v]))*(len(graph[u])))

def get_epsilon():
	return 0.7

def get_popularity_threshold():
	return 2

def get_neighbours(graph,u):
	neighbours = set()

	for v in graph[u]:
		if get_similarity(graph,u,v)> get_epsilon():
			neighbours.add(v)
	return neighbours

def is_dir_reachable(graph,cores,u,v):
	
	# if v is a neighbour of u
	if v in get_neighbours(graph,u) or u in get_neighbours(graph,v):
		return True

	# if v can be reached by a neighbour chain and u is a core or vice versa
	elif u in cores or v in cores:
		l = set(u)
		temp = set()
		while l and temp!=l:
			temp = l
			for i in list(l):
				if v in get_neighbours(graph,i):
					return True
				else:
					l.update(get_neighbours(graph,i)) 
			
	# if u and v are not cores but are reachable by the same core				
	else:			
		for i in cores:
			if u in get_neighbours(graph,i) and v in get_neighbours(graph,i):
				return True

	
	return False

def dir_reachable(graph,cores,u):
	reachable_nodes = []
	for i in graph:
		if is_dir_reachable(graph,cores,u,i):
			reachable_nodes.append(i)
	return reachable_nodes			
			

def scan(graph):
	clusters = {}
	hubs = []
	outliers = []
	node_queue = []
	cores = []
	node_labels = dict(zip(list(graph.keys()),map(lambda x: "unclassified",graph.keys())))

	for i in node_labels:
		if node_labels[i] == "unclassified":
			if len(get_neighbours(graph,i))>get_popularity_threshold():
				# i is a core point
				cores.append(i)
				node_labels[i] = "core"
				node_queue.extend(get_neighbours(graph,i))
				cid = i
				node_labels[i]=i

				while node_queue:
					qhead = node_queue[0]
					for j in dir_reachable(graph,cores,qhead):
						if node_labels[j]=="unclassified" or node_labels[j]=="non-member":
							node_labels[j]=i
						if node_labels[j]=="unclassified":
							node_queue.append(j) 
					node_queue.remove(qhead)
			else:
				node_labels[i] = "non-member"

	# to get hubs and outliers
	for i in [k for k in node_labels if node_labels[k]=="non-member"]:
		for x in graph[i]-{i}:
			for y in graph[i]-{i,x}:
				if node_labels[x]!=node_labels[y]:
					node_labels[i] = "hub"
					break
			if node_labels[i] == "hub":
				break
		if node_labels[i]!="hub":
			node_labels[i] = "outlier"

	for i in node_labels:
		if node_labels[i] == "hub":
			hubs.append(i)
		elif node_labels[i] == "outlier":
			outliers.append(i)
		else:
			if node_labels[i] in clusters:
				clusters[node_labels[i]].add(i) 
			else:
				clusters[node_labels[i]] = {i}
	
	return clusters,hubs,outliers
			
	
		
							
def main():
	graph = make_graph()
	clusters,hubs,outliers = scan(graph)
	print("No.of clusters = ",len(clusters))
	n = 1
	for i in clusters:
		print("Cluster ",n,":",clusters[i])
		n = n+1
	print("No.of hubs = ",len(hubs),"\nHubs:",hubs)
	print("No.of outliers = ",len(outliers),"\nOutliers:",outliers)
	
if __name__ == "__main__":
	main()	
		
	
	
