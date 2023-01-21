import networkx as nx
import random

#Crea graph iniziale
G = nx.Graph()

num_nodes = 10
num_edges = 20 # WARNING: non mettere più di N(N-1)/2 edges!

status_list = [0]*round(num_nodes*0.9) + [1]*round(num_nodes*0.1) # 0:Sano, 1:Infetto, 2:Diagnosticato, 3:Morto
random.shuffle(status_list)

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
            edges.append((i,j))

G.add_edges_from(random.choices(edges,k=num_edges)) # sceglie edges a caso tra quelli possibili
