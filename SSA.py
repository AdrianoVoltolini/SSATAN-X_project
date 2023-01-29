import numpy as np
import networkx as nx
from parametri import w_sano, w_infetto, w_diagnosed, w_dead, gamma, w_gamma, beta, delta
from ContactNetwork import graph_creator

def SSA_full(G):

    ass_rates = list(nx.get_node_attributes(G,"ass_rate").values()) # questi comandi funzionano correttamente solo se si usa python 3.7+
    dis_rates = list(nx.get_node_attributes(G,"dis_rate").values())
    statuses = list(nx.get_node_attributes(G,"status").values())

    G_edges = set(G.edges())
    
    r0 = 0 # contact dynamics
    a0 = 0 # epidemic dynamics

    propensities = []

    # per modificare i rate in base allo status del nodo
    contact_diz = {0: w_sano, 1: w_infetto, 2:w_diagnosed, 3:w_dead}
    
    #computa le propensities
    for i in range(len(ass_rates)):

        #computa propensities I -> D, I -> M, D -> M
        if statuses[i] == 1:
            a0 += (delta + beta)
            propensities.extend([(i,delta,"diagnosis"),(i,beta,"death")])

        elif statuses[i] == 2:
            a0 += beta
            propensities.append((i,beta,"death"))

        #computa le propensities che riguardano gli edges
        for j in range(i+1,len(ass_rates)):

            if (i,j) in G_edges: # WARNING: gli edges di G NON sono in ordine!
                G_edges.remove((i,j))
                dis_propensity = dis_rates[i]*dis_rates[j] # le propensities sono (lambda_j * lambda_k)
                r0 += dis_propensity
                propensities.append(((i,j),dis_propensity,"break_contact"))

                #computa propensities S+I e S+D
                n1 = statuses[i]
                n2 = statuses[j]
                if (n1,n2) == (0,1) or (n1,n2) == (1,0): #caso S+I o I+S
                    a0 += gamma
                    propensities.append(((i,j),gamma,"spread"))
                elif (n1,n2) == (0,2) or (n1,n2) == (2,0): #caso S+D o D+S
                    a0 += gamma*w_gamma
                    propensities.append(((i,j),gamma*w_gamma,"spread"))
            else:
                if statuses[i] != 3 and statuses[j] !=3: #evita di calcolare propensities dei morti
                    ass_propensity = (ass_rates[i]*contact_diz[statuses[i]])*(ass_rates[j]*contact_diz[statuses[j]])
                    r0 += ass_propensity
                    propensities.append(((i,j),ass_propensity,"new_contact"))
                pass
        
    # genera numeri random. Seguo il libro di marchetti perché nel paper non si capisce una minchia
    r1 = np.random.uniform(0,1)
    r2 = np.random.uniform(0,1)

    r0a0_r1 = (r0+a0)*r1
    R_index = 0
    # Trova la prossima reazione
    propensities = np.array(propensities,dtype=tuple)

    zeta = propensities[:,1].cumsum()

    # Trova la prossima reazione
    for i in zeta:
        if i  >= r0a0_r1:
            break
        R_index += 1

    # computa tau
    tau = np.log(1/r2)/(r0+a0)
    #print(tau)

    # aggiorniamo il graph
    if propensities[R_index][2] == "new_contact":
        n1 = propensities[R_index][0][0]
        n2 = propensities[R_index][0][1]
        G.add_edge(n1,n2)

    elif propensities[R_index][2] == "break_contact":
        n1 = propensities[R_index][0][0]
        n2 = propensities[R_index][0][1]
        G.remove_edge(n1,n2)

    elif propensities[R_index][2] == "spread":
        n1 = propensities[R_index][0][0]
        n2 = propensities[R_index][0][1]
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

    elif propensities[R_index][2] == "diagnosis":
        n1 = propensities[R_index][0]
        n1_status = 2
        n1_attributes = {"ass_rate": ass_rates[n1],"dis_rate": dis_rates[n1],"status": n1_status}
        nx.set_node_attributes(G,{n1:n1_attributes})
        
        n1_edges = list(G.edges(n1))
        G.remove_edges_from(n1_edges)
    
    else: #death
        n1 = propensities[R_index][0]
        n1_status = 3
        n1_attributes = {"ass_rate": ass_rates[n1],"dis_rate": dis_rates[n1],"status": n1_status}
        nx.set_node_attributes(G,{n1:n1_attributes})
        
        n1_edges = list(G.edges(n1))
        G.remove_edges_from(n1_edges)

    new_statuses = list(nx.get_node_attributes(G,"status").values())

    n_sus = 0
    n_inf = 0
    n_dia = 0
    n_mor = 0

    for s in new_statuses:
        if s == 0:
            n_sus += 1
        elif s == 1:
            n_inf += 1
        elif s == 2:
            n_dia += 1
        else:
            n_mor += 1
    
    return (tau,n_sus,n_inf,n_dia,n_mor)

def SSA_contact(G):

    ass_rates = list(nx.get_node_attributes(G,"ass_rate").values()) # questi comandi funzionano correttamente solo se si usa python 3.7+
    dis_rates = list(nx.get_node_attributes(G,"dis_rate").values())
    statuses = list(nx.get_node_attributes(G,"status").values())

    G_edges = set(G.edges())

    r0 = 0 # contact dynamics

    propensities = []

    # per modificare i rate in base allo status del nodo
    contact_diz = {0: w_sano, 1: w_infetto, 2:w_diagnosed, 3:w_dead}
    
    #computa le propensities che creano nuovi edges
    for i in range(len(ass_rates)):
        for j in range(i+1,len(ass_rates)):
            if (i,j) in G_edges: # WARNING: gli edges di G NON sono in ordine!
                G_edges.remove((i,j))
                dis_propensity = dis_rates[i]*dis_rates[j] # le propensities sono (lambda_j * lambda_k)
                r0 += dis_propensity
                propensities.append(((i,j),dis_propensity,"break_contact"))
            else:
                if statuses[i] != 3 and statuses[j] !=3: #evita di calcolare propensities dei morti
                    ass_propensity = (ass_rates[i]*contact_diz[statuses[i]])*(ass_rates[j]*contact_diz[statuses[j]])
                    r0 += ass_propensity
                    propensities.append(((i,j),ass_propensity,"new_contact"))
                pass

    # genera numeri random. Seguo il libro di marchetti perché nel paper non si capisce una minchia
    r1 = np.random.uniform(0,1)
    r2 = np.random.uniform(0,1)

    r0_r1 = r0*r1
    R_index = 0

    # Trova la prossima reazione
    propensities = np.array(propensities,dtype=tuple)

    zeta = propensities[:,1].cumsum()

    # Trova la prossima reazione
    for i in zeta:
        if i  >= r0_r1:
            break
        R_index += 1
    # print(propensities[R_index])

    # computa tau
    tau = np.log(1/r2)/r0
    #print(tau)

    # aggiorniamo il graph
    if propensities[R_index][2] == "new_contact":
        n1 = propensities[R_index][0][0]
        n2 = propensities[R_index][0][1]
        G.add_edge(n1,n2)

    elif propensities[R_index][2] == "break_contact":
        n1 = propensities[R_index][0][0]
        n2 = propensities[R_index][0][1]
        G.remove_edge(n1,n2)

    return tau

if __name__ == '__main__':
    G = graph_creator()
    print(SSA_full(G))
    # SSA_contact(G)
