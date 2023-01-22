from ContactNetwork import G
from SSA import SSA

t = 0
tf = 1

while t < tf:
    t += SSA(G)
    print(t)

