from SSATANX import SSATANX_full
import numpy as np
from ContactNetwork import graph_creator
from parametri import n_graphs, tf, num_nodes
import time
from multiprocessing import Pool

import pandas as pd
import matplotlib.pyplot as plt


graph_list = [graph_creator(str(x)) for x in range(n_graphs)]

time_start = time.perf_counter() 

def graph_elaborator(values):

    G, ass_rates, dis_rates, statuses = values


    output_diz = {}

    cnt = 0

    for k in range(1,11):
        for p in np.arange(10,110,10):

            t0 = 0


            G_new = G.copy()

            while t0 < tf:
                output = SSATANX_full(G_new, tf, t0, ass_rates, dis_rates,k, p, statuses)
                t0 += output[0]
                statuses = output[-1]

            time_current = time.perf_counter()  
            print(f"After {time_current-time_start:.0f} seconds, Copy number {cnt} of graph {G.name} is complete")
            
            cnt += 1
            time_end = time.perf_counter()
            output_diz[(k,p)] = time_end - time_start

    # print(f"It took me {time_end-time_start:.2f} seconds and {cnt} steps to finish graph {G.name}")
    return output_diz

# per fare multiprocessing:
if __name__ == '__main__':

    results = np.array(Pool().map(graph_elaborator,graph_list),dtype=tuple)

    diz_total = {key: [d[key] for d in results] for key in results[0].keys()}

    diz_mean = {key: np.array([d[key] for d in results]).mean() for key in results[0].keys()}

    print(diz_mean)

    ks = [x for x in range(1,11)]
    ps = [x for x in np.arange(10,110,10)]

    mean_dataframe = pd.DataFrame()
    for k in ks:
        for p in ps:
            mean_dataframe.loc[k,p] = diz_mean[(k,p)]
    print(mean_dataframe)


    fig, ax = plt.subplots(1,1)
    cp = ax.contourf(mean_dataframe.columns, mean_dataframe.index,mean_dataframe)
    cbar = plt.colorbar(cp)
    cbar.set_label("Time (sec)")
    ax.set_title(f"Contour Plot for P and K ({num_nodes} nodes) ")
    ax.set_xlabel("P")
    ax.set_ylabel("K")
    plt.show()




        


    
