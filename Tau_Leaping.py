import numpy as np
import networkx as nx
from parametri import num_nodes, w_sano, w_infetto, w_diagnosed, w_dead, p, k, alpha, epsilon
from SSA import SSA_contact
from ContactNetwork import graph_creator

#@profile #mi serve per misurare lentezza del codice
def tau_leap_contact(G,delta_t,leap_t):

    ass_rates = list(nx.get_node_attributes(G,"ass_rate").values()) # questi comandi funzionano correttamente solo se si usa python 3.7+
    dis_rates = list(nx.get_node_attributes(G,"dis_rate").values())
    statuses = list(nx.get_node_attributes(G,"status").values())

    G_edges = set(G.edges())

    # per modificare i rate in base allo status del nodo
    contact_diz = {0: w_sano, 1: w_infetto, 2:w_diagnosed, 3:w_dead}

    living_nodes = num_nodes - statuses.count(3) # conta i nodi ancora vivi nel graph
    E_max = (living_nodes*(living_nodes-1))/2

    r0_ass = 0
    r0_dis = 0

    ass_propensities = []
    dis_propensities = []
    
    #computa le propensities che creano nuovi edges
    for i in range(len(ass_rates)):
        for j in range(i+1,len(ass_rates)):
            if (i,j) in G_edges: # WARNING: gli edges di G NON sono in ordine!
                dis_propensity = dis_rates[i]*dis_rates[j] # le propensities sono (lambda_j * lambda_k)
                r0_dis += dis_propensity
                dis_propensities.append(((i,j),dis_propensity,"break_contact"))
            else:
                if statuses[i] != 3 and statuses[j] !=3: #evita di calcolare propensities dei morti
                    ass_propensity = (ass_rates[i]*contact_diz[statuses[i]])*(ass_rates[j]*contact_diz[statuses[j]])
                    r0_ass += ass_propensity
                    ass_propensities.append(((i,j),ass_propensity,"new_contact"))
                pass

    r0_tot = r0_ass + r0_dis
    E = len(G.edges)
    E_prime = E_max - E

    mu = r0_ass - r0_dis
    mu_prime = r0_dis - r0_ass
    sigma2 = r0_ass + r0_dis

    tau_a = max(epsilon*E,1)/(abs(mu)*2) # nel paper il *2 non c'è, mentre nel libro sì
    tau_b = (max(epsilon*E,1)**2)/(sigma2*4) # nel paper il *4 non c'è, mentre nel libro sì
    tau_c = max(epsilon*E_prime,1)/(abs(mu_prime)*2)
    tau_d = (max(epsilon*E_prime,1)**2)/(sigma2*4)
    # print(tau_a,tau_b,tau_c,tau_d)
    tau_temp = min(tau_a,tau_b,tau_c,tau_d)
    tau = min(tau_temp, delta_t-leap_t)

    #print(tau, k/r0_tot)

    setAcceptedLeap = False
    while setAcceptedLeap == False: # ho deciso di seguire il libro invece che il paper per tau-leaping
        setAcceptedLeap = True
        
        if tau < k/r0_tot:
            t_SSA = 0
            # print("it's SSA time!")
            for i in range(p):
                t_SSA += SSA_contact(G)
            return t_SSA
        else:
            n_ass_reactions = np.random.poisson(r0_ass*tau)
            n_dis_reactions = np.random.poisson(r0_dis*tau)

            E_next = E + n_ass_reactions - n_dis_reactions

            if E_next < 0 or E_next > E_max:
                tau = tau*alpha
                setAcceptedLeap = False
                # print("Trying with a smaller tau")
            else:
                # print("it's tau-leaping time!",n_ass_reactions, n_dis_reactions)

                O = [0]*n_ass_reactions + [1]*n_dis_reactions
                np.random.shuffle(O)

                u = np.random.uniform(size=len(O))
                ass_propensities = np.array(ass_propensities,dtype=tuple) #trasformo perché è più comodo
                dis_propensities = np.array(dis_propensities,dtype=tuple) #lavorare con np.array

                zeta_ass = ass_propensities[:,1].cumsum()
                zeta_dis = dis_propensities[:,1].cumsum()

                for r in range(len(O)):
                    if O[r] == 1: # rimuovi un edge
                        r0_dis = zeta_dis[-1]
                        u_r0_dis = u[r]*r0_dis

                        R_index_dis = 0

                        #find first y such as:
                        for i in zeta_dis:
                            if i >= u_r0_dis:
                                break
                            R_index_dis += 1
                        
                        #print("chosen breaking reaction:",temp_dis_propensities[R_index_dis])

                        #rimuovi dal graph
                        n1 = dis_propensities[R_index_dis][0][0]
                        n2 = dis_propensities[R_index_dis][0][1]
                        G.remove_edge(n1,n2)

                        #aggiorna i vari array
                        ass_propensity = ((ass_rates[n1]*contact_diz[statuses[n1]])*(ass_rates[n2]*contact_diz[statuses[n2]]))+zeta_ass[-1]
                        zeta_ass = np.append(zeta_ass, ass_propensity)
                        new_row = np.array(((n1,n2),ass_propensity,"new_contact"),ndmin=2,dtype=tuple)
                        ass_propensities = np.append(ass_propensities,new_row,axis=0)
                        zeta_dis = np.delete(zeta_dis,R_index_dis)
                        dis_propensities = np.delete(dis_propensities,R_index_dis,0)


                    else: #aggiungi un edge
                        r0_ass = zeta_ass[-1]
                        u_r0_ass = u[r]*r0_ass

                        R_index_ass = 0

                        #find first y such as:
                        for i in zeta_ass:
                            if i >= u_r0_ass:
                                break
                            R_index_ass += 1
                        
                        #print("chosen creating reaction:",temp_ass_propensities[R_index_ass])

                        #aggiungi al graph
                        n1 = ass_propensities[R_index_ass][0][0]
                        n2 = ass_propensities[R_index_ass][0][1]
                        G.add_edge(n1,n2)

                        #aggiorna i vari array
                        dis_propensity = (dis_rates[n1]*dis_rates[n2])+zeta_dis[-1]
                        zeta_dis = np.append(zeta_dis,dis_propensity)
                        new_row = np.array(((n1,n2),dis_propensity,"break_contact"),ndmin=2,dtype=tuple)
                        dis_propensities = np.append(dis_propensities,new_row,axis=0)
                        zeta_ass = np.delete(zeta_ass,R_index_ass)
                        ass_propensities =np.delete(ass_propensities,R_index_ass,0)

    return tau

# if __name__ == '__main__':
#     G = graph_creator()
#     tau_leap_contact(G,5,0)