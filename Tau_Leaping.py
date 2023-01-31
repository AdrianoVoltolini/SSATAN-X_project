import numpy as np
from collections import deque
import networkx as nx
from parametri import num_nodes, w_sano, w_infetto, w_diagnosed, w_dead, p, k, alpha, alpha_star, epsilon, omega, omega_star
from SSA import SSA_contact
from ContactNetwork import graph_creator

# @profile #mi serve per misurare lentezza del codice
def tau_leap_old(G, delta_t, ass_rates, dis_rates, statuses):

    G_edges = set(G.edges())

    living_nodes = num_nodes - statuses.count(3) # conta i nodi ancora vivi nel graph
    E_max = (living_nodes*(living_nodes-1))/2
    E = len(G_edges)
    E_prime = E_max - E

    # per modificare i rate in base allo status del nodo
    contact_diz = {0: w_sano, 1: w_infetto, 2:w_diagnosed, 3:w_dead}

    r0_ass = 0
    r0_dis = 0

    ass_propensities = []
    dis_propensities = []
    
    #computa le propensities che creano nuovi edges
    for i in range(len(ass_rates)):
        if statuses[i] != 3: # evita di calcolare propensities dei morti
            for j in range(i+1,len(ass_rates)):
                if statuses[j] != 3: # evita di calcolare propensities dei morti
                    if (i,j) in G_edges: # WARNING: gli edges di G NON sono in ordine!
                        G_edges.remove((i,j))
                        dis_propensity = dis_rates[i]*dis_rates[j] # le propensities sono (lambda_j * lambda_k)
                        r0_dis += dis_propensity
                        dis_propensities.append(((i,j),dis_propensity,"break_contact"))
                    else:
                        ass_propensity = (ass_rates[i]*contact_diz[statuses[i]])*(ass_rates[j]*contact_diz[statuses[j]])
                        r0_ass += ass_propensity
                        ass_propensities.append(((i,j),ass_propensity,"new_contact"))

    r0_tot = r0_ass + r0_dis

    mu = r0_ass - r0_dis
    mu_prime = r0_dis - r0_ass
    sigma2 = r0_ass + r0_dis

    tau_a = max(epsilon*E,1)/(abs(mu)*2) # nel paper il *2 non c'è, mentre nel libro sì
    tau_b = (max(epsilon*E,1)**2)/(sigma2*4) # nel paper il *4 non c'è, mentre nel libro sì
    tau_c = max(epsilon*E_prime,1)/(abs(mu_prime)*2)
    tau_d = (max(epsilon*E_prime,1)**2)/(sigma2*4)
    # print(tau_a,tau_b,tau_c,tau_d)
    tau_temp = min(tau_a,tau_b,tau_c,tau_d)

    # print(tau_temp,delta_t)
    tau = min(tau_temp, delta_t)

    #print(tau, k/r0_tot)

    setAcceptedLeap = False
    while setAcceptedLeap == False: # ho deciso di seguire il libro invece che il paper per tau-leaping
        setAcceptedLeap = True
        
        if tau < k/r0_tot:
            t_SSA = 0
            # print("it's SSA time!")
            for i in range(p):
                t_SSA += SSA_contact(G, ass_rates, dis_rates, statuses)
            return t_SSA
        else:
            n_ass_reactions = np.random.poisson(r0_ass*tau)
            n_dis_reactions = np.random.poisson(r0_dis*tau)

            E_next = E + n_ass_reactions - n_dis_reactions

            # print(E_next, E_max)

            if E_next < 0 or E_next > E_max:
                tau = tau*alpha
                setAcceptedLeap = False
                # print("Trying with a smaller tau")
            else:
                # da qui in poi è Algoritmo 4

                O = [0]*n_ass_reactions + [1]*n_dis_reactions
                np.random.shuffle(O)

                u = np.random.uniform(size=len(O))

                #cumulative sums delle propensities
                zeta_ass = list(np.array(ass_propensities,dtype=tuple)[:,1].cumsum())
                zeta_dis = list(np.array(dis_propensities,dtype=tuple)[:,1].cumsum())

                for r in range(len(O)):
                    if O[r] == 1: # rimuovi un edge

                        r0_dis = zeta_dis[-1]

                        #per trovare prossima reazione
                        R_index_dis = np.searchsorted(zeta_dis,u[r]*r0_dis)
                        
                        #print("chosen breaking reaction:",temp_dis_propensities[R_index_dis])

                        #rimuovi dal graph
                        n1 = dis_propensities[R_index_dis][0][0]
                        n2 = dis_propensities[R_index_dis][0][1]
                        G.remove_edge(n1,n2)

                        #aggiorna i vari array
                        ass_propensity = ((ass_rates[n1]*contact_diz[statuses[n1]])*(ass_rates[n2]*contact_diz[statuses[n2]]))+zeta_ass[-1]
                        zeta_ass.append(ass_propensity)
                        new_row = ((n1,n2),ass_propensity,"new_contact")
                        ass_propensities.append(new_row)
                        zeta_dis.remove(zeta_dis[R_index_dis])
                        dis_propensities.remove(dis_propensities[R_index_dis])


                    else: #aggiungi un edge
                        r0_ass = zeta_ass[-1]
                        u_r0_ass = u[r]*r0_ass

                        #per trovare prossima reazione
                        R_index_ass = np.searchsorted(zeta_ass,u_r0_ass)
                        
                        #print("chosen creating reaction:",temp_ass_propensities[R_index_ass])

                        #aggiungi al graph
                        n1 = ass_propensities[R_index_ass][0][0]
                        n2 = ass_propensities[R_index_ass][0][1]
                        G.add_edge(n1,n2)

                        #aggiorna i vari array
                        dis_propensity = (dis_rates[n1]*dis_rates[n2])+zeta_dis[-1]
                        zeta_dis.append(dis_propensity)
                        new_row = ((n1,n2),dis_propensity,"break_contact")
                        dis_propensities.append(new_row)
                        zeta_ass.remove(zeta_ass[R_index_ass])
                        ass_propensities.remove(ass_propensities[R_index_ass])

    return tau

# @profile #mi serve per misurare lentezza del codice
def tau_leap_new(G,delta_t,ass_rates, dis_rates, statuses):

    G_edges = set(G.edges())

    living_nodes = num_nodes - statuses.count(3) # conta i nodi ancora vivi nel graph

    E_max = (living_nodes*(living_nodes-1))/2
    E = len(G_edges)
    E_prime = E_max - E

    M = [0,0]
    Q = [0,0]
    C = [0,0]
    S = [deque([[0,0]]), deque([[0,0]])]
    r0 = [0,0]
    row = [0,0]

    ass_propensities = []
    dis_propensities = []

    # per modificare i rate in base allo status del nodo
    contact_diz = {0: w_sano, 1: w_infetto, 2:w_diagnosed, 3:w_dead}
    
    #computa le propensities che creano nuovi edges
    for i in range(len(ass_rates)):
        if statuses[i] != 3: # evita di calcolare propensities dei morti
            for j in range(i+1,len(ass_rates)):
                if statuses[j] != 3: # evita di calcolare propensities dei morti
                    if (i,j) in G_edges: # WARNING: gli edges di G NON sono in ordine!
                        G_edges.remove((i,j))
                        dis_propensity = dis_rates[i]*dis_rates[j] # le propensities sono (lambda_j * lambda_k)
                        r0[1] += dis_propensity
                        dis_propensities.append(((i,j),dis_propensity,"break_contact"))
                    else:
                        ass_propensity = (ass_rates[i]*contact_diz[statuses[i]])*(ass_rates[j]*contact_diz[statuses[j]])
                        r0[0] += ass_propensity
                        ass_propensities.append(((i,j),ass_propensity,"new_contact"))

    mu = r0[0] - r0[1]
    mu_prime = r0[1] - r0[0]
    sigma2 = r0[0] + r0[1]

    r0_tot = r0[0] + r0[1]

    tau_a = max(epsilon*E,1)/(abs(mu)*2) # nel paper il *2 non c'è, mentre nel libro sì
    tau_b = (max(epsilon*E,1)**2)/(sigma2*4) # nel paper il *4 non c'è, mentre nel libro sì
    tau_c = max(epsilon*E_prime,1)/(abs(mu_prime)*2)
    tau_d = (max(epsilon*E_prime,1)**2)/(sigma2*4)
    # print(tau_a,tau_b,tau_c,tau_d)
    tau_temp = min(tau_a,tau_b,tau_c,tau_d)

    # print(tau_temp,delta_t)
    tau = min(tau_temp, delta_t)

    setAcceptedLeap = False
    while setAcceptedLeap == False:
        setAcceptedLeap = True
        
        if tau < k/r0_tot:
            # print("it's SSA time!")
            t_SSA = 0
            for i in range(p):
                t_SSA += SSA_contact(G, ass_rates,dis_rates, statuses)
            return t_SSA
        else:
            for i in [0,1]: # 0 crea edges, 1 li rompe
                B = len(S[i])-1
                if r0[i]*tau + Q[i] >= S[i][B][0]: #utilizza poisson per decidere quante reazioni fare
                    M[i] = np.random.poisson(r0[i]*tau + Q[i] - S[i][B][0]) + S[i][B][1] - C[i]
                    row[i] = B

                else: # utilizza binomiale invece
                    K = 0
                    condition1 = S[i][K-1][0] <= r0[i]*tau
                    condition2 = S[i][K][0] > r0[i]*tau
                    while (condition1 and condition2) == False:
                        K += 1
                    u = (r0[i]*tau + Q[i] - S[i][K-1][0])/S[i][K][0] - S[i][K-1][0]
                    M[i] = np.random.binomial(S[i][K][1] - S[i][K-1][1],u) + S[i][K-1][1] - C[i]
                    row[i] = K - 1

            condition1_leap = M[0] - M[1] <= max(epsilon*E,1)
            condition2_leap = -M[0] + M[1] <= max(epsilon*E_prime,1)
            # print(M[0] - M[1], epsilon*E)
            # print(-M[0] +M[1], epsilon*E_prime)
            if (condition1_leap and condition2_leap) == True: # leap accepted
                for i in [0,1]:
                    # S[i][:] = S[i][row+1:]
                    cnt = 0
                    while cnt <= row[i]:
                        S[i].popleft()
                        cnt += 1
                    S[i].appendleft([r0[i]*tau + Q[i],C[i]+M[i]])
                    Q[i] = Q[i] + r0[i]*tau
                    C[i] = C[i] + M[i]
                    # print(Q[i],C[i])

                condition1_prime = M[0] - M[1] <= max(epsilon*E*0.75,1)
                condition2_prime = -M[0] + M[1] <= max(epsilon*E_prime*0.75,1)

                if (condition1_prime and condition2_prime) == False:
                    return tau*alpha_star
                else:
                    if delta_t + tau < 1:
                        tau = tau**omega
                    else:
                        tau = tau**omega_star

                #da qui in poi è Algoritmo 4

                O = [0]*M[0] + [1]*M[1]
                np.random.shuffle(O)

                u = np.random.uniform(size=len(O))

                #cumulative sums delle propensities
                zeta_ass = list(np.array(ass_propensities,dtype=tuple)[:,1].cumsum())
                zeta_dis = list(np.array(dis_propensities,dtype=tuple)[:,1].cumsum())

                for r in range(len(O)):
                    if O[r] == 1: # rimuovi un edge

                        r0_dis = zeta_dis[-1]

                        #per trovare prossima reazione utilizzando binary search
                        R_index_dis = np.searchsorted(zeta_dis,u[r]*r0_dis)
                        
                        #print("chosen breaking reaction:",temp_dis_propensities[R_index_dis])

                        #rimuovi dal graph
                        n1 = dis_propensities[R_index_dis][0][0]
                        n2 = dis_propensities[R_index_dis][0][1]
                        G.remove_edge(n1,n2)

                        #aggiorna i vari array
                        ass_propensity = ((ass_rates[n1]*contact_diz[statuses[n1]])*(ass_rates[n2]*contact_diz[statuses[n2]]))+zeta_ass[-1]
                        zeta_ass.append(ass_propensity)
                        new_row = ((n1,n2),ass_propensity,"new_contact")
                        ass_propensities.append(new_row)
                        zeta_dis.remove(zeta_dis[R_index_dis])
                        dis_propensities.remove(dis_propensities[R_index_dis])


                    else: #aggiungi un edge
                        r0_ass = zeta_ass[-1]
                        u_r0_ass = u[r]*r0_ass

                        #per trovare prossima reazione
                        R_index_ass = np.searchsorted(zeta_ass,u_r0_ass)
                        
                        #print("chosen creating reaction:",temp_ass_propensities[R_index_ass])

                        #aggiungi al graph
                        n1 = ass_propensities[R_index_ass][0][0]
                        n2 = ass_propensities[R_index_ass][0][1]
                        G.add_edge(n1,n2)

                        #aggiorna i vari array
                        dis_propensity = (dis_rates[n1]*dis_rates[n2])+zeta_dis[-1]
                        zeta_dis.append(dis_propensity)
                        new_row = ((n1,n2),dis_propensity,"break_contact")
                        dis_propensities.append(new_row)
                        zeta_ass.remove(zeta_ass[R_index_ass])
                        ass_propensities.remove(ass_propensities[R_index_ass])
            else: #leap rejected
                setAcceptedLeap = False
                for i in [0,1]:
                    S[i].insert(row[i],[r0[0]*tau+Q[i],C[i]+M[i]])
                    tau = tau*alpha
    return tau

if __name__ == '__main__':
    G, ass_rates, dis_rates = graph_creator()
    dt = 0
    statuses = [nx.get_node_attributes(G,"status")[x] for x in range(num_nodes)] 
    while dt < 5:
        dt += tau_leap_new(G,dt,ass_rates,dis_rates, statuses)


