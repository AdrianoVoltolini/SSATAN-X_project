from ContactNetwork import G
from SSA import SSA
from parametri import t, tf
import time

cnt = 0
time_start = time.time()

while t < tf:
    t += SSA(G)
    cnt += 1

time_end = time.time()

print(f"It took me {time_end-time_start} seconds and {cnt} steps to finish")