import numpy as np
import networkx as nx
from parametri import tf, num_nodes, gamma, w_gamma, beta, delta, p, k
from ContactNetwork import graph_creator
from Tau_Leaping import tau_leap_old, tau_leap_new

# @profile #mi serve per misurare lentezza del codice
def SSATANX_full(G,t_final, t_current, ass_rates, dis_rates, p_input, k_input, statuses):

    TL = t_final - t_current

    a0 = 0

    epidemic_propensities = []

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

            #epidemic propensities 
            a0 += (delta + beta)
            epidemic_propensities.extend([(i,delta,"diagnosis"),(i,beta,"death")])

        elif statuses[i] == 2:
            n_edges_inf_diag += len(G.edges(i))
            n_diagnosed += 1

            # epidemic propensities
            a0 += beta
            epidemic_propensities.append((i,beta,"death"))
        
    Bs = min(n_edges_inf_diag,n_edges_sus)*gamma # è una stima che hanno fatto nei supplementary materials
    Bd = n_infected*delta
    Bo = (n_infected+n_diagnosed)*beta

    BTl = Bs + Bd + Bo #upper bound delle epidemic_propensities

    if BTl <= 0: # sono morti tutti, non ci sono più reazioni da fare

        n_sus = 0
        n_inf = 0
        n_dia = 0
        n_mor = 0

        for s in statuses:
            if s == 0:
                n_sus += 1
            elif s == 1:
                n_inf += 1
            elif s == 2:
                n_dia += 1
            else:
                n_mor += 1
        
        return (TL, n_sus, n_inf, n_dia, n_mor, statuses)


    #r2 = np.random.uniform(0,1)
    # time_step = np.log(1/r2)/BTl
    time_step = np.random.exponential(1/BTl)

    if time_step > TL:
        #reject

        n_sus = 0
        n_inf = 0
        n_dia = 0
        n_mor = 0

        for s in statuses:
            if s == 0:
                n_sus += 1
            elif s == 1:
                n_inf += 1
            elif s == 2:
                n_dia += 1
            else:
                n_mor += 1
        
        return (TL, n_sus, n_inf, n_dia, n_mor, statuses)

    else:
        t_leap = 0
        while t_leap < time_step: # tau leaping per contact dynamics
            t_leap += tau_leap_new(G, time_step, t_leap, ass_rates, dis_rates, p_input, k_input, statuses)

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

        u = np.random.uniform()

        if a0 > BTl*u:
            # print("accepting")
            R_index = 0

            # cumulative sum delle propensities
            zeta = np.array(epidemic_propensities,dtype=tuple)[:,1].cumsum()

            # Trova la prossima reazione utilizzando binary sort
            R_index = np.searchsorted(zeta,BTl*u)

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
            pass
        
        new_statuses = [nx.get_node_attributes(G,"status")[x] for x in range(num_nodes)]

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
        
        return (time_step, n_sus, n_inf, n_dia, n_mor, new_statuses)

if __name__ == '__main__':
    G, ass_rates, dis_rates, statuses = graph_creator()
    t0 = 0
    while t0 < tf:    
        output = SSATANX_full(G,tf, t0, ass_rates, dis_rates,p,k, statuses)
        t0 += output[0]
        statuses = output[-1]
        print(output)