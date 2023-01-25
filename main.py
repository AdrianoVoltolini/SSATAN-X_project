from ContactNetwork import graph_creator
from SSA import SSA_full
from parametri import tf, n_graphs
import time
from multiprocessing import Pool

graph_list = [graph_creator() for x in range(n_graphs)]

#per misurare quanto tempo ci mette
time_start = time.perf_counter() 

def graph_elaborator(G):
    t0 = 0
    cnt = 0

    while t0 < tf:
        t0 += SSA_full(G) # SSA_full ritorna tau
        cnt += 1

    time_end = time.perf_counter()

    print(f"It took me {time_end-time_start} seconds and {cnt} steps")
    return None

# for G in graph_list:
#     graph_elaborator(G)

# per fare multiprocessing:
if __name__ == '__main__':
    Pool().map(graph_elaborator,graph_list)
