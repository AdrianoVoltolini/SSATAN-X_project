from ContactNetwork import G
from SSA import SSA
from parametri import t, tf

while t < tf:
    t += SSA(G)
    print(t)