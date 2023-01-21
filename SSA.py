import numpy as np
import networkx as nx
import random

def SSA(G):

    ass_rates = list(nx.get_node_attributes(G,"ass_rate").values()) # questi comandi funzionano correttamente solo se si usa python 3.7+
    dis_rates = list(nx.get_node_attributes(G,"dis_rate").values())

    r0 = 0 # contact dynamics
    a0 = 0 # epidemic dynamics

    contact_propensities = []

    #computa le propensities che creano nuovi edges
    for i in range(len(ass_rates)):
        for j in range(i+1,len(ass_rates)):
            if (i,j) not in G.edges(): # WARNING: gli edges di G NON sono in ordine!
                ass_propensity = ass_rates[i]*ass_rates[j] # le propensities sono (lambda_j * lambda_k)
                r0 += ass_propensity
                contact_propensities.append(((i,j),ass_propensity,True)) # True per indicare che reazione crea un edge

    #computa le propensities che rompono edges
    for i in range(len(dis_rates)):
        for j in range(i+1,len(dis_rates)):
            if (i,j) in G.edges(): # WARNING: gli edges di G NON sono in ordine!
                dis_propensity = dis_rates[i]*dis_rates[j] # le propensities sono (lambda_j * lambda_k)
                r0 += dis_propensity
                contact_propensities.append(((i,j),dis_propensity,False)) # False per indicare che reazione rompe un edge

    #print(contact_propensities)
    # print(a0)

    # genera numeri random. Seguo il libro di marchetti perché nel paper non si capisce una minchia
    r1 = random.uniform(0,1)
    r2 = random.uniform(0,1)

    r0r1 = r0*r1
    R_index = 0
    # Trova la prossima reazione
    for i in range(len(contact_propensities)):
        #print(f"calculating {r0r1}-{contact_propensities[i][1]}")
        r0r1 -= contact_propensities[i][1]
        R_index = i
        if r0r1 <= 0:
            break
    #print(contact_propensities[R_index])

    # computa tau
    tau = np.log(1/r2)/r0
    #print(tau)

    # aggiorniamo il graph
    if contact_propensities[R_index][2] == True:
        G.add_edge(contact_propensities[R_index][0][0],contact_propensities[R_index][0][1])
    else:
        G.remove_edge(contact_propensities[R_index][0][0],contact_propensities[R_index][0][1])

    #print(G.edges())
    return tau



