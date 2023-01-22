import networkx as nx
import random
import numpy as np

#Crea graph iniziale
G = nx.Graph()

num_nodes = 10
num_edges = 20 # WARNING: non mettere più di N(N-1)/2 edges!

# 0:Sano, 1:Infetto, 2:Diagnosticato, 3:Morto
status_list = [0]*round(num_nodes*0.6) + [1]*round(num_nodes*0.2) + [2]*round(num_nodes*0.1) + [3]*round(num_nodes*0.1)
random.shuffle(status_list)
diagnosed_or_dead = [x for x, y in enumerate(status_list) if y > 1] # salviamo index dei diagnosticati e morti 


nodes = [(x,{
 "ass_rate": random.uniform(0.5,2.5), # nel paper hanno usato 0.5 e 2.5
 "dis_rate": random.uniform(0.4,2.0), # nel paper hanno usato 0.4 e 2.0
 "status" : status_list[x]
 })
 for x in range(num_nodes)] # nodi creati casualmente

G.add_nodes_from(nodes)

edges = []

for i in range(num_nodes): # crea lista di tutti gli edge possibili
    for j in range(num_nodes):
        if i<j:
            if i not in diagnosed_or_dead and j not in diagnosed_or_dead:
                edges.append((i,j))

G.add_edges_from(random.choices(edges,k=num_edges)) # sceglie edges a caso tra quelli possibili
