from ContactNetwork import graph_creator
from SSA import SSA_full
from SSATANX import SSATANX_full
from parametri import tf, n_graphs
import time
from multiprocessing import Pool
import numpy as np

graph_list = [graph_creator(str(x)) for x in range(n_graphs)]

#per misurare quanto tempo ci mette
time_start = time.perf_counter() 

def graph_elaborator(G):
    t0 = 0
    cnt = 0

    while t0 < tf:
        t0 += SSATANX_full(G) # ritorna delta_t
        # t0 += SSA_full(G)
        cnt += 1
        if cnt % 10 == 0: # per controllare che stia ancora lavorando
            time_current = time.perf_counter()  
            print(f"After {time_current-time_start:.0f} seconds, computation of graph {G.name} is {(1-((tf-t0)/tf))*100:.0f}% complete")
    
    time_end = time.perf_counter()

    # print(f"It took me {time_end-time_start:.2f} seconds and {cnt} steps to finish graph {G.name}")
    return (time_end - time_start,cnt)

# for G in graph_list:
#     graph_elaborator(G)

# per fare multiprocessing:
if __name__ == '__main__':
    results = np.array(Pool().map(graph_elaborator,graph_list),dtype=tuple)
    print(f"Average time: {results[:,0].mean():.2f} seconds, average number of steps: {results[:,1].mean():.2f}")
