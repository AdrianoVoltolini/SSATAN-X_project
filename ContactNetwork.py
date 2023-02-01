import networkx as nx
import random

from parametri import num_nodes, num_edges, t0_sani, t0_infetti, t0_diagnosed, t0_morti, ass_range, dis_range

#Crea graph iniziale

def graph_creator(name="0"):
    G = nx.Graph()
    G.name = name

    # 0:Sano, 1:Infetto, 2:Diagnosticato, 3:Morto
    status_list = [0]*round(num_nodes*t0_sani) + [1]*round(num_nodes*t0_infetti) + [2]*round(num_nodes*t0_diagnosed) + [3]*round(num_nodes*t0_morti)
    random.shuffle(status_list)
    diagnosed_or_dead = [x for x, y in enumerate(status_list) if y > 1] # salviamo index dei diagnosticati e morti 


    nodes = [(x,{
    "ass_rate": random.uniform(ass_range[0],ass_range[1]),
    "dis_rate": random.uniform(dis_range[0],dis_range[1]),
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

    G.add_edges_from(random.sample(edges,k=num_edges)) # sceglie edges a caso tra quelli possibili
    
    ass_rates =[nx.get_node_attributes(G,"ass_rate")[x] for x in range(num_nodes)]
    dis_rates = [nx.get_node_attributes(G,"dis_rate")[x] for x in range(num_nodes)]
    statuses = [nx.get_node_attributes(G,"status")[x] for x in range(num_nodes)]

    return (G,ass_rates,dis_rates,statuses)
