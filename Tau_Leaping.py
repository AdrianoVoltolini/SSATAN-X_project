import numpy as np
import networkx as nx
from parametri import tf, num_nodes, w_sano, w_infetto, w_diagnosed, w_dead, gamma, w_gamma, beta, delta, epsilon
from SSA import SSA_full

from ContactNetwork import graph_creator


def tau_leap(G,t):

    ass_rates = list(nx.get_node_attributes(G,"ass_rate").values()) # questi comandi funzionano correttamente solo se si usa python 3.7+
    dis_rates = list(nx.get_node_attributes(G,"dis_rate").values())
    statuses = list(nx.get_node_attributes(G,"status").values())

    r0_ass = 0
    r0_dis = 0

    ass_propensities = []
    dis_propensities = []

    # per modificare i rate in base allo status del nodo
    contact_diz = {0: w_sano, 1: w_infetto, 2:w_diagnosed, 3:w_dead}
    
    #computa le propensities che creano nuovi edges
    for i in range(len(ass_rates)):
        for j in range(i+1,len(ass_rates)):
            if (i,j) not in G.edges(): # WARNING: gli edges di G NON sono in ordine!
                ass_propensity = (ass_rates[i]*contact_diz[statuses[i]])*(ass_rates[j]*contact_diz[statuses[j]])
                r0_ass += ass_propensity
                ass_propensities.append(((i,j),ass_propensity,"new_contact"))
        
    #computa le propensities che rompono edges
    for i in range(len(dis_rates)):
        for j in range(i+1,len(dis_rates)):
            if (i,j) in G.edges(): # WARNING: gli edges di G NON sono in ordine!
                dis_propensity = dis_rates[i]*dis_rates[j] # le propensities sono (lambda_j * lambda_k)
                r0_dis += dis_propensity
                dis_propensities.append(((i,j),dis_propensity,"break_contact"))

    r0_tot = r0_ass + r0_dis

    living_nodes = num_nodes - statuses.count(3) # conta i nodi ancora vivi nel graph

    E_max = (living_nodes*(living_nodes-1))/2
    E = len(G.edges)
    E_prime = E_max - E #forse non serve

    mu = r0_ass - r0_dis
    mu_prime = r0_dis - r0_ass #forse non serve

    sigma2 = r0_ass + r0_dis

    tau_a = max(epsilon*E,1)/abs(mu)
    tau_b = (max(epsilon*E,1)**2)/sigma2
    tau_c = max(epsilon*E_prime,1)/abs(mu_prime) #forse non serve
    tau_d = (max(epsilon*E_prime,1)**2)/sigma2 #forse non serve

    tau_temp = min(tau_a,tau_b,tau_c,tau_d)

    tau = min(tau_temp, tf-t)

    if tau < 10/r0_tot:
        t_SSA = 0
        print("it's SSA time!")
        # for i in range(100):
        #     t_SSA += SSA_full(G)
        # return t_SSA
    else:
        ass_reactions = np.random.poisson(r0_ass*tau)
        dis_reactions = np.random.poisson(r0_dis*tau)
        print("it's tau-leaping time!",ass_reactions, dis_reactions)

        # da implementare: scegli le reazioni ed aggiorna il graph
        # se nuovo graph non rispetta le condizioni:
        # -> rejecta il nuovo graph e diminuisci tau 
        # ritorna graph e tau

        
    


            







G = graph_creator()
tau_leap(G,0)