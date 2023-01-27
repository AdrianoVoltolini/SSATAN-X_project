import numpy as np
import networkx as nx
from parametri import tf,w_sano, w_infetto, w_diagnosed, w_dead, gamma, w_gamma, beta, delta
from ContactNetwork import graph_creator

def SSATANX_full(G,t):

    statuses = list(nx.get_node_attributes(G,"status").values())

    TL = tf-t

    #roba sotto serve per calcolare upper bound
    n_edges_sus = 0
    n_edges_inf_diag = 0
    n_infected = 0
    n_diagnosed = 0

    for i in range(len(statuses)):

        if statuses[i] == 0:
            n_edges_sus += len(G.edges(i))
        elif statuses[i] == 1:
            n_edges_inf_diag += len(G.edges(i))
            n_infected += 1
        elif statuses[i] == 2:
            n_edges_inf_diag += len(G.edges(i))
            n_diagnosed += 1
        
    Bs = min(n_edges_inf_diag,n_edges_sus)*gamma # è una stima che hanno fatto nei supplementary
    Bd = n_infected*delta
    Bo = (n_infected+n_diagnosed)*beta

    BTl = Bs + Bd + Bo #upper bound

    print(Bs,Bd,Bo)





G = graph_creator()
SSATANX_full(G,0)


