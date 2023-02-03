import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from plot_nx_graph import *

################## Main code starts here ##################

#df = pd.read_csv("NAMD_data_frame_S2.csv")  # complete data frame from NAMD simulations on S2 state
df = pd.read_csv("NAMD_data_frame.csv")  # complete data frame from NAMD simulations
#df = pd.read_csv("AIMD_data_frame.csv")  # complete data frame from AIMD simulations
#df = pd.read_csv("NAMD_data_frame_reduced.csv") # smaller data frame for testing
df.sort_values("d31",ascending=True,inplace=True,ignore_index=True)

##########################
### Nodes construction ###
##########################

G = nx.Graph()

# Here nodes are added to the graph with a few attributes

for i in range(1,len(df)+1):
    G.add_node(i)
    for j in list(df.columns):
        G.nodes[i][j] = df[j][i-1]




# only a few attributes
#for i in range(1,len(df)+1):
#    G.add_node(i)
#    G.nodes[i]["HOMO"] = df["HOMO"][i-1]
#    G.nodes[i]["d31"] = df["d31"][i-1]
#    G.nodes[i]["d30"] = df["d30"][i - 1]
#    G.nodes[i]["d13"] = df["d13"][i - 1]
#    G.nodes[i]["d20"] = df["d20"][i - 1]
#print(len(df))
#for i in list(df.columns):
#    plot_all_nodes(G,i,"HOMO")
#quit()
MI_v = [0.9000083480090394, 0.8923605415661721,0.8902862872998463,0.8881563161017649] # Mutual Inf. values based on AIMD

##########################
### Edges construction ###
##########################

# Here is where edges are built. The criteria used in adding edges with a weight will alter the shortest paths between nodes

count = 0
for i in range(1, len(G.nodes)):
    for j in range(i + 1, len(G.nodes) + 1):
        if i in [10000,20000,30000,40000,50000]:
            print(str(i)+" nodes have been evaluated")
        if abs(G.nodes[j]["d31"] == G.nodes[i]["d31"]):
            continue
        if abs(G.nodes[i]["d31"] - G.nodes[j]["d31"]) < 3.0 and abs(G.nodes[j]["d31"] - G.nodes[i]["d31"]) > 0.0 :#and (abs(G.nodes[i]["HOMO"]-G.nodes[j]["HOMO"]) < 0.0001) and (abs(G.nodes[i]["HOMO"]-G.nodes[j]["HOMO"]) > 0.0):
            if G.nodes[j]["HOMO"]-G.nodes[i]["HOMO"] < 0.002 and G.nodes[j]["HOMO"]-G.nodes[i]["HOMO"] > 0.0:
                #print(i, j, G.nodes[i], G.nodes[j], abs(G.nodes[i]["d31"] - G.nodes[j]["d31"]))
                w = 1/((abs(G.nodes[i]["d31"] - G.nodes[j]["d31"]))*MI_v[0] +  (abs(G.nodes[i]["d30"] - G.nodes[j]["d30"]))*MI_v[1] + (abs(G.nodes[i]["d13"] - G.nodes[j]["d13"]))*MI_v[2] + (abs(G.nodes[i]["d20"] - G.nodes[j]["d20"]))*MI_v[3])
                G.add_edge(i, j, weight=w)
                count += 1
            else:
                continue
        else:
            break

for i in range(len(G.nodes), 1):
    for j in range(i - 1, 0):
        if i in [10000,20000,30000,40000,50000]:
            print(str(i)+" nodes have been evaluated")
        if abs(G.nodes[j]["d31"] == G.nodes[i]["d31"]):
            continue
        if abs(G.nodes[i]["d31"] - G.nodes[j]["d31"]) < 3.0 and abs(G.nodes[j]["d31"] - G.nodes[i]["d31"]) > 0.0 :#and (abs(G.nodes[i]["HOMO"]-G.nodes[j]["HOMO"]) < 0.0001) and (abs(G.nodes[i]["HOMO"]-G.nodes[j]["HOMO"]) > 0.0):
            if G.nodes[j]["HOMO"]-G.nodes[i]["HOMO"] < 0.002 and G.nodes[j]["HOMO"]-G.nodes[i]["HOMO"] > 0.0:
                #print(i, j, G.nodes[i], G.nodes[j], abs(G.nodes[i]["d31"] - G.nodes[j]["d31"]))
                w = 1/((abs(G.nodes[i]["d31"] - G.nodes[j]["d31"]))*MI_v[0] +  (abs(G.nodes[i]["d30"] - G.nodes[j]["d30"]))*MI_v[1] + (abs(G.nodes[i]["d13"] - G.nodes[j]["d13"]))*MI_v[2] + (abs(G.nodes[i]["d20"] - G.nodes[j]["d20"]))*MI_v[3])
                G.add_edge(i, j, weight=w)
                count += 1
            else:
                continue
        else:
            break


print("All edges are built")

plot_graph(G,11,50000,"d31","HOMO",2)

#for i in range(100,1000,100):
#    for j in range(40000,50000,1000):
#        plot_graph(G, i, j, "d31", "HOMO", 2)
