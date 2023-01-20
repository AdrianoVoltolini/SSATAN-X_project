#import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

#Crea graph iniziale
G = nx.Graph()

num_nodes = 20
num_edges = 30 # WARNING: non mettere più di N(N-1)/2 edges!

status_list = [0]*round(num_nodes*0.9) + [1]*round(num_nodes*0.1) # 0:Sano, 1:Infetto, 2:Diagnosticato, 3:Morto
random.shuffle(status_list)

nodes = [(x,{
 "ass_rate": random.uniform(0.5,2.5),
 "dis_rate": random.uniform(0.4,2.0),
 "status" : status_list[x]
 })
 for x in range(num_nodes)] # nodi creati casualmente

G.add_nodes_from(nodes)

edges = []
for i in range(num_nodes): # crea lista di tutti gli edge possibili
    for j in range(num_nodes):
        if i<j:
            edges.append((i,j))


G.add_edges_from(random.choices(edges,k=num_edges)) # sceglie edges a caso tra quelli possibili

if __name__ == "__main__": # parte solo quando fai partire questo script da qui. Disegna il graph

    sane_nodes = []
    infected_nodes = []
    diagnosed_nodes = []
    morti_nodes = []

    pos = nx.circular_layout(G) # determina come vengono disposti i nodi nel plot

    for i in G.nodes(): # smista i nodi in base allo status per colorarli dopo
        match nx.get_node_attributes(G,"status")[i]: 
            case 0: # modo figo per fare if/elif/else in python 3.10+
                sane_nodes.append(i)
            case 1:
                infected_nodes.append(i)
            case 2:
                diagnosed_nodes.append(i)
            case 3:
                morti_nodes.append(i)

    nx.draw_networkx_nodes(G, pos, nodelist=sane_nodes, node_color="blue") # disegna e colora i nodi
    nx.draw_networkx_nodes(G, pos, nodelist=infected_nodes, node_color="red")
    nx.draw_networkx_nodes(G, pos, nodelist=diagnosed_nodes, node_color="brown")
    nx.draw_networkx_nodes(G, pos, nodelist=morti_nodes, node_color="black")

    nx.draw_networkx_edges(G,pos) # disegna gli edge
    
    plt.show()

