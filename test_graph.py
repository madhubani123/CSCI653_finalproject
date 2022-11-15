import networkx as nx
import matplotlib.pyplot as plt
from math import *

##########################
### Nodes construction ###
##########################

G = nx.Graph()
#G.add_node(1)
G.add_nodes_from([1, 5])
G.add_nodes_from([
    (1, {"Energy": 0.2}),
    (2, {"Energy": 0.03}),
    (3, {"Energy": 0.8}),
    (4, {"Energy": 5.7}),
    (5, {"Energy": 10}),
])

##########################
### Edges construction ###
##########################

for i in range(1,len(G.nodes)):
	for j in range(i+1,len(G.nodes)+1):
		if abs(G.nodes[i]["Energy"] - G.nodes[j]["Energy"]) < 5.6:
			print(i,j,G.nodes[i],G.nodes[j],abs(G.nodes[i]["Energy"] - G.nodes[j]["Energy"]))
			G.add_edge(i,j)
#####################
### Shortest path ###
#####################

sp = dict(nx.all_pairs_shortest_path(G))
print(sp[1][5])


##############
### Plots ####
##############

subax1 = plt.subplot(121)
nx.draw(G, with_labels=True, font_weight='bold')
#subax2 = plt.subplot(122)
#nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
plt.show() 
