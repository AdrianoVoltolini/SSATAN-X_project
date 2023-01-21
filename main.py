from ContactNetwork import G
from SSA import SSA

t = 0
tf = 1
cnt = 0

while t < tf:
    t += SSA(G)
    cnt +=1

print(cnt)