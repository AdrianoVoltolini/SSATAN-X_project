import numpy as np
import time
from multiprocessing import Pool

from ContactNetwork import graph_creator
from SSA import SSA_full
from SSATANX import SSATANX_full
from parametri import tf, n_graphs, k, p

# questo script serve per misurare velocità media di SSA e SSATANX

graph_list = [graph_creator(str(x)) for x in range(n_graphs)]

#per misurare quanto tempo ci mette
time_start = time.perf_counter() 

def graph_elaborator(values):
    t0 = 0
    cnt = 0

    G, ass_rates, dis_rates, statuses = values

    while t0 < tf:
        # output = SSA_full(G, tf, t0, ass_rates, dis_rates, statuses)
        output = SSATANX_full(G, tf, t0, ass_rates, dis_rates, k, p, statuses)
        t0 += output[0]
        statuses = output[-1]

        cnt += 1
        if cnt % 10 == 0: # per controllare che stia ancora lavorando
            time_current = time.perf_counter()  
            print(f"After {time_current-time_start:.0f} seconds, graph {G.name} is {(1-((tf-t0)/tf))*100:.0f}% complete")
    
    time_end = time.perf_counter()

    # print(f"It took me {time_end-time_start:.2f} seconds and {cnt} steps to finish graph {G.name}")
    return (time_end - time_start,cnt)

# for G in graph_list:
#     graph_elaborator(G)

# per fare multiprocessing:
if __name__ == '__main__':
    results = np.array(Pool().map(graph_elaborator,graph_list),dtype=tuple)
    print(f"Time: {results[:,0].mean():.2f} +- {results[:,0].std():.2f} seconds.")
    print(f"Number of steps: {results[:,1].mean():.0f} +- {results[:,1].std():.0f}")
