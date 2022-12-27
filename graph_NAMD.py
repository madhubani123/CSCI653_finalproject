import networkx as nx
import matplotlib.pyplot as plt
from math import *
import scipy
import pandas as pd
import numpy as np


def plot_graph(G,source,target,path_idx=0):
    H = nx.subgraph(G, [i for i in range(source,target+1)])
    path = nx.single_source_shortest_path(H, source)
    print(path)
    # sp = [p for p in nx.all_shortest_paths(G,source=1054,target=1061,method="dijkstra",weight="use_weight")]
    sp = [p for p in nx.shortest_path(H, source=source, target=target, method="dijkstra")]
    if len(np.shape(sp)) == 1:
        sp1 = sp
    else:
        sp1 = sp[path_idx]

    col = []
    sizes = []
    posit = {}
    for i in range(source-1,target):
        posit[i + 1] = [H.nodes[i + 1]["d31"], H.nodes[i + 1]["Energy"]]
        if i + 1 in sp1:
            col.append("red")
            sizes.append(300)
        else:
            col.append("blue")
            sizes.append(5)
    col[0] = "green"
    col[-1] = "green"

    # print([p for p in nx.all_shortest_paths(G, source=1054, target=1061)])  # All shortest paths if more than 1
    print("here is fine 2")
    ##############
    ### Plots ####
    ##############
    HOMO_e = []
    dihedral = []

    for i in sp1:
        HOMO_e.append(H.nodes[i]["Energy"])
        dihedral.append(H.nodes[i]["d31"])

    subax1 = plt.subplot(121)
    nx.draw(H, with_labels=False, font_weight='bold', node_size=sizes, font_size=5, node_color=col, ax=subax1,
            pos=posit)
    subax1.set(xlabel="Degrees", ylabel="HOMO energy (eV)")
    # nx.draw(G,nodelist=sp1, with_labels=True, font_weight='bold',node_size=50,font_size=5, node_color="red")
    subax2 = plt.subplot(122)
    subax2.plot(dihedral, HOMO_e)
    subax2.set(xlabel="Degrees", ylabel="HOMO energy (eV)")
    plt.savefig("Graph_and_energy_profile_"+str(source)+"_"+str(target)+".png", format='png', dpi=300, bbox_inches='tight')
    print("Function is done")

    #for (u, v, wt) in H.edges.data('weight'):
    #    print(f"({u}, {v}, {wt:.3})")


df = pd.read_csv("NAMD_data_frame.csv")
df.sort_values("d31",ascending=True,inplace=True,ignore_index=True)

##########################
### Nodes construction ###
##########################

G = nx.Graph()
#

for i in range(1,len(df)+1):
    G.add_node(i)
    G.nodes[i]["Energy"] = df["HOMO"][i-1]
    G.nodes[i]["d31"] = df["d31"][i-1]
    G.nodes[i]["d30"] = df["d30"][i - 1]
    G.nodes[i]["d13"] = df["d13"][i - 1]
    G.nodes[i]["d20"] = df["d20"][i - 1]

MI_v = [0.9000083480090394, 0.8923605415661721,0.8902862872998463,0.8881563161017649]

##########################
### Edges construction ###
##########################
count = 0
for i in range(1, len(G.nodes)):
    for j in range(i + 1, len(G.nodes) + 1):
        if i in [10000,20000,30000,40000,50000]:
            print(str(i)+" nodes have been evaluated")
        if abs(G.nodes[j]["d31"] == G.nodes[i]["d31"]):
            continue
        if abs(G.nodes[i]["d31"] - G.nodes[j]["d31"]) < 3.0 and abs(G.nodes[j]["d31"] - G.nodes[i]["d31"]) > 0.0 :#and (abs(G.nodes[i]["Energy"]-G.nodes[j]["Energy"]) < 0.0001) and (abs(G.nodes[i]["Energy"]-G.nodes[j]["Energy"]) > 0.0):
            #print(i, j, G.nodes[i], G.nodes[j], abs(G.nodes[i]["d31"] - G.nodes[j]["d31"]))
            w = 1/((abs(G.nodes[i]["d31"] - G.nodes[j]["d31"]))*MI_v[0] +  (abs(G.nodes[i]["d30"] - G.nodes[j]["d30"]))*MI_v[1] + (abs(G.nodes[i]["d13"] - G.nodes[j]["d13"]))*MI_v[2] + (abs(G.nodes[i]["d20"] - G.nodes[j]["d20"]))*MI_v[3])
            G.add_edge(i, j, weight=w)
            count += 1
        else:
            break

######################
### Shortest paths ###
######################
print("here is fine 1")

plot_graph(G,1,1200)

#path = nx.single_source_shortest_path(G, 1)
#print(path)
##sp = [p for p in nx.all_shortest_paths(G,source=1054,target=1061,method="dijkstra",weight="use_weight")]
#sp = [p for p in nx.shortest_path(G,source=1,target=12559,method="dijkstra")]
#print(len(sp))  # One shortest path
#print(sp)
#
##col[1053] = "green"
##col[1060] = "green"
#
#sp1 = sp
#
#col = []
#sizes = []
#posit = {}
#for i in range(len(G.nodes)):
#    posit[i+1] = [G.nodes[i+1]["d31"],G.nodes[i+1]["Energy"]]
#    if i+1 in sp1:
#        col.append("red")
#        sizes.append(300)
#    else:
#        col.append("blue")
#        sizes.append(50)
#col[1] = "green"
#col[12559] = "green"
#
#
##print([p for p in nx.all_shortest_paths(G, source=1054, target=1061)])  # All shortest paths if more than 1
#print("here is fine 2")
###############
#### Plots ####
###############
#HOMO_e = []
#dihedral = []
#
#for i in sp1:
#    HOMO_e.append(G.nodes[i]["Energy"])
#    dihedral.append(G.nodes[i]["d31"])
#
#
#
#subax1 = plt.subplot(121)
#nx.draw(G, with_labels=False, font_weight='bold',node_size=sizes,font_size=5,node_color=col, ax=subax1, pos=posit)
#subax1.set(xlabel="Degrees", ylabel="HOMO energy (eV)")
##nx.draw(G,nodelist=sp1, with_labels=True, font_weight='bold',node_size=50,font_size=5, node_color="red")
#subax2 = plt.subplot(122)
#subax2.plot(dihedral,HOMO_e)
#subax2.set(xlabel="Degrees", ylabel="HOMO energy (eV)")
#plt.savefig("Graph_and_energy_profile.png", format='png', dpi=300, bbox_inches='tight')
#plt.show()





