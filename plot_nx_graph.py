import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

################## Functions for plotting graphs ##################

def plot_graph(G,source,target,var1,var2,step=1,path_idx=0):
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
    print(len(np.shape(sp)))
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
        posit1[i] = [G.nodes[i][var1], G.nodes[i][var2]]
    for i in subnodes:
        posit2[i] = [G.nodes[i][var1], G.nodes[i][var2]]
    for i in [source,target]:
        posit3[i] = [G.nodes[i][var1], G.nodes[i][var2]]

    print("Graphs are ready, starting plot section")

    ##############
    ### Plots ####
    ##############

    HOMO_e = []   # Store the HOMO energy of nodes in shortest path for 2D energy profile
    dihedral = [] # Store the dihedral angle of nodes in shortest path for 2D energy profile
    for i in sp1:
        HOMO_e.append(G.nodes[i][var2])
        dihedral.append(G.nodes[i][var1])

    # Plot 3 graphs on top of each other: start with othernodes, add subnodes, finish with [source,target]
    fig, subax1 = plt.subplots()

    nx.draw(H1, with_labels=False, font_weight='bold', node_size=5, font_size=5, node_color="blue", ax=subax1,
            pos=posit1)
    nx.draw(H2, with_labels=False, font_weight='bold', node_size=10, font_size=5, node_color="red", ax=subax1,
            pos=posit2)
    nx.draw(H3, with_labels=False, font_weight='bold', node_size=10, font_size=5, node_color="green", ax=subax1,
            pos=posit3)
    limits = plt.axis('on')  # turns on axis
    subax1.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    subax1.set(xlabel=var1, ylabel=var2)
    # Export picture to png
    plt.savefig("Graph_" + str(source) + "_" + str(target) + "_" + str(step) + ".png", format='png', dpi=300,
                bbox_inches='tight')
    plt.clf() # clear image for next plot
    # Plot 2D energy profile
    subax2 = plt.subplot()
    subax2.plot(dihedral, HOMO_e)
    subax2.set(xlabel=var1, ylabel=var2)
    # Export picture to png
    plt.savefig("Energy_profile_"+var1+"_"+var2+"_"+str(source)+"_"+str(target)+".png", format='png', dpi=300, bbox_inches='tight')
    plt.clf()
    plt.close()

    return print("Function 'plot_graph' is done")

def plot_all_nodes(G,var1,var2,string=""):
    '''
    :param G: a networkx graph
    :param var1: the internal coordinate for which the HOMO energy is plotted against
    :return: png image of all nodes in the graph positioned on a xy axis (x: internal coordinate, y: HOMO energy)
    '''

    # Dictionaries for positions of nodes as described in the documentation for networkx.draw()
    posit1 = {}

    for i in list(G):
        posit1[i] = [G.nodes[i][var1], G.nodes[i][var2]]

    ##############
    ### Plots ####
    ##############

    fig, subax1 = plt.subplots()
    nx.draw_networkx_nodes(G, node_size=5,  node_color="blue", ax=subax1, pos=posit1)
    limits = plt.axis('on')  # turns on axis
    subax1.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    subax1.set(xlabel=var1, ylabel=var2)
    # Export to png
    plt.savefig("All_nodes_"+var1+"_"+var2+string+".png", format='png', dpi=300,
                bbox_inches='tight')
    plt.clf()
    plt.close()
    print("Function 'plot_all_nodes' is done")


################## End of functions ##################
