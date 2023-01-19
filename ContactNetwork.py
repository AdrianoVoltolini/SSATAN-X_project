import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

#Crea graph iniziale
G = nx.Graph()

num_nodes = 20
num_edges = 30 # WARNING: non mettere più di N(N-1)/2 edges!

def random_status():
    # 0 : Sano
    # 1 : Infetto
    # 2 : Diagnosticato 
    # 3 : Morto
    return random.choice([0]*9 + [1])

nodes = [(x,{"ass_rate": np.random.uniform(0.5,2.5),
 "dis_rate": np.random.uniform(0.4,2.0),
 "status" : random_status()
 })
 for x in range(num_nodes)] # nodi creati casualmente

G.add_nodes_from(nodes)

edges = []
for i in range(num_nodes):
    for j in range(num_nodes):
        if i != j:
            if (j,i) not in edges:
                edges.append(((i,j)))


G.add_edges_from(random.choices(edges,k=num_edges)) # sceglie edges a caso tra quelli possibili

pos = nx.kamada_kawai_layout(G)

nx.draw(G)
plt.show()
