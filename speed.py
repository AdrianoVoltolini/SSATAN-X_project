import numpy as np
import time
from multiprocessing import Pool
import matplotlib.pyplot as plt
import pandas as pd

from ContactNetwork import graph_creator
from SSA import SSA_full
from SSATANX import SSATANX_full
from parametri import tf, n_graphs, k, p
from Tau_Leaping import tau_leap_new, tau_leap_old


# questo script serve per misurare velocità media di SSA e SSATANX

graph_list = [graph_creator(str(x)) for x in range(n_graphs)]

def graph_elaborator(values):

    output_diz ={}
    for i in ["SSATANX_new","SSATANX_old","SSA"]:
        t0 = 0
        cnt = 0

        G, ass_rates, dis_rates, statuses = values

        G_copy = G.copy()

        time_start = time.perf_counter() 

        while t0 < tf:

            if i == "SSATANX_new":
                output = SSATANX_full(G_copy, tf, t0, ass_rates, dis_rates, k, p, tau_leap_new, statuses)
            elif i == "SSATANX_old":
                output = SSATANX_full(G_copy, tf, t0, ass_rates, dis_rates, k, p, tau_leap_old, statuses)
            elif i == "SSA":
                output = SSA_full(G_copy, tf, t0, ass_rates, dis_rates, statuses)
            
            cnt += 1
            t0 += output[0]
            statuses = output[-1]
        
        time_end = time.perf_counter()

        output_diz[i] = (time_end - time_start, cnt)
    
    return output_diz

# for G in graph_list:
#     graph_elaborator(G)

# per fare multiprocessing:
if __name__ == '__main__':
    results = np.array(Pool().map(graph_elaborator,graph_list),dtype=tuple)

    time_mean = pd.Series({key: np.array([d[key][0] for d in results]).mean() for key in results[0].keys()})
    time_sd = pd.Series({key: np.array([d[key][0] for d in results]).std() for key in results[0].keys()})

    step_mean = pd.Series({key: np.array([d[key][1] for d in results]).mean() for key in results[0].keys()})
    step_sd = pd.Series({key: np.array([d[key][1] for d in results]).std() for key in results[0].keys()})

    fig, (ax1,ax2) = plt.subplots(2,1, constrained_layout=True)

    ax1.bar(time_mean.index, time_mean, yerr=time_sd)
    ax2.bar(step_mean.index, step_mean, yerr=step_sd)

    ax1.set_ylabel("Time (seconds)")
    ax2.set_ylabel("Number of Steps")

    ax1.set_title("Speed Comparison")
    ax2.set_title("Steps Comparison")
    plt.show()
