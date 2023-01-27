import numpy as np
import networkx as nx
from parametri import tf,w_sano, w_infetto, w_diagnosed, w_dead, gamma, w_gamma, beta, delta
from ContactNetwork import graph_creator
from Tau_Leaping import tau_leap_contact

def SSATANX_full(G,t):

    ass_rates = list(nx.get_node_attributes(G,"ass_rate").values()) # questi comandi funzionano correttamente solo se si usa python 3.7+
    dis_rates = list(nx.get_node_attributes(G,"dis_rate").values())
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
        
    Bs = min(n_edges_inf_diag,n_edges_sus)*gamma # è una stima che hanno fatto nei supplementary materials
    Bd = n_infected*delta
    Bo = (n_infected+n_diagnosed)*beta


    BTl = Bs + Bd + Bo #upper bound delle epidemic_propensities

    delta_t = np.random.exponential(1/BTl)

    if delta_t > TL:
        # print("rejecting")
        return TL
    else:
        #print("it's big brain time")
        t_leap = 0
        while t_leap < delta_t:
            t_leap += tau_leap_contact(G,delta_t,t_leap)
        
        epidemic_propensities = []
        a0 = 0

        #computa epidemic_propensities I+S e D+S
        for edge in G.edges():
            n1 = statuses[edge[0]]
            n2 = statuses[edge[1]]
            if (n1,n2) == (0,1) or (n1,n2) == (1,0): #caso S+I o I+S
                a0 += gamma
                epidemic_propensities.append((edge,gamma,"spread"))
            elif (n1,n2) == (0,2) or (n1,n2) == (2,0): #caso S+D o D+S
                a0 += gamma*w_gamma
                epidemic_propensities.append((edge,gamma*w_gamma,"spread"))
            
        #computa epidemic_propensities I -> D, I -> M, D -> M
        for i in range(len(statuses)):
            if statuses[i] == 1:
                a0 += delta
                epidemic_propensities.append((i,delta,"diagnosis"))

                a0 += beta
                epidemic_propensities.append((i,beta,"death"))
            elif statuses[1] == 2:
                a0 += beta
                epidemic_propensities.append((i,beta,"death"))
        
        u = np.random.uniform()

        if a0 > BTl*u:
            # print("accepting")
            R_index = 0

            epidemic_propensities = np.array(epidemic_propensities,dtype=tuple)

            zeta = epidemic_propensities[:,1].cumsum()

            # Trova la prossima reazione
            for i in zeta:
                if i  >= BTl*u:
                    break
                R_index += 1

            if epidemic_propensities[R_index][2] == "spread":
                n1 = epidemic_propensities[R_index][0][0]
                n2 = epidemic_propensities[R_index][0][1]
                n1_status = statuses[n1]
                n2_status = statuses[n2]
                
                if n1_status == 0:
                    n1_status = 1
                    n1_attributes = {"ass_rate": ass_rates[n1],"dis_rate": dis_rates[n1],"status": n1_status}
                    nx.set_node_attributes(G,{n1:n1_attributes})
                else:
                    n2_status = 1
                    n2_attributes = {"ass_rate": ass_rates[n2],"dis_rate": dis_rates[n2],"status": n2_status}
                    nx.set_node_attributes(G,{n2:n2_attributes})

            elif epidemic_propensities[R_index][2] == "diagnosis":
                n1 = epidemic_propensities[R_index][0]
                n1_status = 2
                n1_attributes = {"ass_rate": ass_rates[n1],"dis_rate": dis_rates[n1],"status": n1_status}
                nx.set_node_attributes(G,{n1:n1_attributes})
                
                n1_edges = list(G.edges(n1))
                G.remove_edges_from(n1_edges)
            
            else: #death
                n1 = epidemic_propensities[R_index][0]
                n1_status = 3
                n1_attributes = {"ass_rate": ass_rates[n1],"dis_rate": dis_rates[n1],"status": n1_status}
                nx.set_node_attributes(G,{n1:n1_attributes})
                
                n1_edges = list(G.edges(n1))
                G.remove_edges_from(n1_edges)
        else:
            # print("thinning")  
            return delta_t     
    return delta_t


G = graph_creator()
SSATANX_full(G,0)