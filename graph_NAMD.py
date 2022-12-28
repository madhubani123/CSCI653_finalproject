import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

################## Functions for plotting graphs ##################

def plot_graph(G,source,target,step=1,path_idx=0):
    '''
    :param G: a networkx graph
    :param source: the node from which a shortest path begins
    :param target: the node to which a shortest path ends
    :param step: controls how many other nodes between source and target are plotted, default is all nodes (step=1)
    :param path_idx: specifies which shortest path to plot between source and target. Ignored if only 1 path is found
    :return: png images of shortest path between source and target and the 2D energy profile related to it
    '''
    ################## Find shortest path between source and target ##################
    sp = [p for p in nx.shortest_path(G, source=source, target=target, method="dijkstra")]
    # Check for number of shortest paths between source and target
    if len(np.shape(sp)) == 1:
        sp1 = sp
    else:
        sp1 = sp[path_idx]

    othernodes = [i for i in range(source, target, step)]  # list of other nodes that need to be plotted
    subnodes = list(sorted(set([*sp1])))                   # list of nodes in the selected shortest paths


    # Creating subgraphs for nodes in 'subnodes', 'othernodes' and for [source,target], to be used for plotting
    H1 = nx.subgraph(G, othernodes)       # other nodes will be blue and size 5
    H2 = nx.subgraph(G, subnodes)         # nodes on path will be red and size 300
    H3 = nx.subgraph(G, [source,target])  # source and target nodes will be green and size 300

    # Dictionaries for positions of nodes as described in the documentation for networkx.draw()
    posit1 = {}
    posit2 = {}
    posit3 = {}
    for i in othernodes:
        posit1[i] = [G.nodes[i]["d31"], G.nodes[i]["Energy"]]
    for i in subnodes:
        posit2[i] = [G.nodes[i]["d31"], G.nodes[i]["Energy"]]
    for i in [source,target]:
        posit3[i] = [G.nodes[i]["d31"], G.nodes[i]["Energy"]]

    print("Graphs are ready, starting plot section")

    ##############
    ### Plots ####
    ##############

    HOMO_e = []   # Store the HOMO energy of nodes in shortest path for 2D energy profile
    dihedral = [] # Store the dihedral angle of nodes in shortest path for 2D energy profile
    for i in sp1:
        HOMO_e.append(G.nodes[i]["Energy"])
        dihedral.append(G.nodes[i]["d31"])

    # Plot 3 graphs on top of each other: start with othernodes, add subnodes, finish with [source,target]
    fig, subax1 = plt.subplots()

    nx.draw(H1, with_labels=False, font_weight='bold', node_size=5, font_size=5, node_color="blue", ax=subax1,
            pos=posit1)
    nx.draw(H2, with_labels=True, font_weight='bold', node_size=300, font_size=5, node_color="red", ax=subax1,
            pos=posit2)
    nx.draw(H3, with_labels=True, font_weight='bold', node_size=300, font_size=5, node_color="green", ax=subax1,
            pos=posit3)
    limits = plt.axis('on')  # turns on axis
    subax1.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    subax1.set(xlabel="Degrees", ylabel="HOMO energy (eV)")
    # Export picture to png
    plt.savefig("Graph_" + str(source) + "_" + str(target) + "_" + str(step) + ".png", format='png', dpi=300,
                bbox_inches='tight')
    plt.clf() # clear image for next plot
    # Plot 2D energy profile
    subax2 = plt.subplot()
    subax2.plot(dihedral, HOMO_e)
    subax2.set(xlabel="Degrees", ylabel="HOMO energy (eV)")
    # Export picture to png
    plt.savefig("Energy_profile_"+str(source)+"_"+str(target)+".png", format='png', dpi=300, bbox_inches='tight')
    plt.clf()

    return print("Function 'plot_graph' is done")

def plot_all_nodes(G,int_coord="d31"):
    '''
    :param G: a networkx graph
    :param int_coord: the internal coordinate for which the HOMO energy is plotted against
    :return: png image of all nodes in the graph positioned on a xy axis (x: internal coordinate, y: HOMO energy)
    '''

    # Dictionaries for positions of nodes as described in the documentation for networkx.draw()
    posit1 = {}

    for i in list(G):
        posit1[i] = [G.nodes[i][int_coord], G.nodes[i]["Energy"]]

    ##############
    ### Plots ####
    ##############

    fig, subax1 = plt.subplots()
    nx.draw_networkx_nodes(G, node_size=5,  node_color="blue", ax=subax1, pos=posit1)
    limits = plt.axis('on')  # turns on axis
    subax1.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    subax1.set(xlabel="Degrees", ylabel="HOMO energy (eV)")
    # Export to png
    plt.savefig("All_nodes.png", format='png', dpi=300,
                bbox_inches='tight')
    plt.clf()
    print("Function 'plot_all_nodes' is done")


################## End of functions ##################

################## Main code starts here ##################

#df = pd.read_csv("NAMD_data_frame.csv")  # complete data frame
df = pd.read_csv("NAMD_data_frame_reduced.csv") # smaller data frame for testing
df.sort_values("d31",ascending=True,inplace=True,ignore_index=True)

##########################
### Nodes construction ###
##########################

G = nx.Graph()

# Here nodes are added to the graph with a few attributes

for i in range(1,len(df)+1):
    G.add_node(i)
    G.nodes[i]["Energy"] = df["HOMO"][i-1]
    G.nodes[i]["d31"] = df["d31"][i-1]
    G.nodes[i]["d30"] = df["d30"][i - 1]
    G.nodes[i]["d13"] = df["d13"][i - 1]
    G.nodes[i]["d20"] = df["d20"][i - 1]

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
        if abs(G.nodes[i]["d31"] - G.nodes[j]["d31"]) < 3.0 and abs(G.nodes[j]["d31"] - G.nodes[i]["d31"]) > 0.0 :#and (abs(G.nodes[i]["Energy"]-G.nodes[j]["Energy"]) < 0.0001) and (abs(G.nodes[i]["Energy"]-G.nodes[j]["Energy"]) > 0.0):
            if G.nodes[j]["Energy"]-G.nodes[i]["Energy"] < 0.002 and G.nodes[j]["Energy"]-G.nodes[i]["Energy"] > 0.0:
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
        if abs(G.nodes[i]["d31"] - G.nodes[j]["d31"]) < 3.0 and abs(G.nodes[j]["d31"] - G.nodes[i]["d31"]) > 0.0 :#and (abs(G.nodes[i]["Energy"]-G.nodes[j]["Energy"]) < 0.0001) and (abs(G.nodes[i]["Energy"]-G.nodes[j]["Energy"]) > 0.0):
            if G.nodes[j]["Energy"]-G.nodes[i]["Energy"] < 0.002 and G.nodes[j]["Energy"]-G.nodes[i]["Energy"] > 0.0:
                #print(i, j, G.nodes[i], G.nodes[j], abs(G.nodes[i]["d31"] - G.nodes[j]["d31"]))
                w = 1/((abs(G.nodes[i]["d31"] - G.nodes[j]["d31"]))*MI_v[0] +  (abs(G.nodes[i]["d30"] - G.nodes[j]["d30"]))*MI_v[1] + (abs(G.nodes[i]["d13"] - G.nodes[j]["d13"]))*MI_v[2] + (abs(G.nodes[i]["d20"] - G.nodes[j]["d20"]))*MI_v[3])
                G.add_edge(i, j, weight=w)
                count += 1
            else:
                continue
        else:
            break


print("All edges are built")

plot_graph(G,11,133,2)
plot_all_nodes(G)


