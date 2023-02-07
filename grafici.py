import matplotlib.pyplot as plt
import pandas as pd

from ContactNetwork import graph_creator
from SSA import SSA_full
from SSATANX import SSATANX_full
from parametri import tf, num_nodes, t0_sani, t0_infetti, t0_diagnosed, t0_morti, k,p
from Tau_Leaping import tau_leap_new, tau_leap_old


fig, (ax1, ax2) = plt.subplots(2,1,constrained_layout=True)

G, ass_rates, dis_rates, statuses = graph_creator()

G_SSA = G.copy()
statuses_SSA = statuses.copy()

t0_status = (round(num_nodes*t0_sani), round(num_nodes*t0_infetti), round(num_nodes*t0_diagnosed), round(num_nodes*t0_morti))

t0_SSA = 0
data_SSA = {}
data_SSA[0] = t0_status

while t0_SSA < tf:
    output = SSA_full(G_SSA, tf, t0_SSA, ass_rates, dis_rates, statuses_SSA)
    t0_SSA += output[0]
    statuses_SSA = output[-1]
    data_SSA[t0_SSA] = output[1:-1]

data_SSA = pd.DataFrame(data_SSA)

ax1.set_title(f"SSA ({num_nodes} nodes)")

ax1.plot(data_SSA.iloc[0,:],c="blue")
ax1.plot(data_SSA.iloc[1,:],c="red")
ax1.plot(data_SSA.iloc[2,:],c="brown")
ax1.plot(data_SSA.iloc[3,:],c="black")

ax1.set_xlim(left=0,right=5)
ax1.set_xlabel("Time")
ax1.set_ylabel("number of nodes")

############################################################

G_SSATANX = G.copy()
statuses_SSATANX = statuses.copy()

t0_SSATANX = 0
data_SSATANX = {}
data_SSATANX[0] = t0_status


while t0_SSATANX < tf:
    output = SSATANX_full(G_SSATANX, tf, t0_SSATANX, ass_rates, dis_rates, k, p, tau_leap_new, statuses_SSATANX)
    t0_SSATANX += output[0]
    statuses_SSATANX = output[-1]
    data_SSATANX[t0_SSATANX] = output[1:-1]

data_SSATANX = pd.DataFrame(data_SSATANX)

ax2.set_title(f"SSATANX ({num_nodes} nodes)")

ax2.plot(data_SSATANX.iloc[0,:],c="blue")
ax2.plot(data_SSATANX.iloc[1,:],c="red")
ax2.plot(data_SSATANX.iloc[2,:],c="brown")
ax2.plot(data_SSATANX.iloc[3,:],c="black")

ax2.set_xlim(left=0,right=5)
ax2.set_xlabel("Time")
ax2.set_ylabel("number of nodes")

plt.show()

#controlla che i morti non diventino zombie
print(data_SSATANX.iloc[3,:].is_monotonic_increasing)
print(data_SSA.iloc[3,:].is_monotonic_increasing)