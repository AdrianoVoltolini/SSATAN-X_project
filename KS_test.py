import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from ContactNetwork import graph_creator
from SSA import SSA_full
from SSATANX import SSATANX_full
from parametri import tf, num_nodes, t0_sani, t0_infetti, t0_diagnosed, t0_morti, k, p, a, time_step

# questo script determina se due distribuzioni possono essere considerate uguali
# andando a vedere la loro distanza massima a certi valori di t
# e confrontandola con un threshold

G, ass_rates, dis_rates, statuses = graph_creator()
t0_status = (round(num_nodes*t0_sani), round(num_nodes*t0_infetti), round(num_nodes*t0_diagnosed), round(num_nodes*t0_morti))

G_SSA = G.copy()
statuses_SSA = statuses.copy()
t0_SSA = 0
data_SSA = {}
data_SSA[0] = t0_status
output_SSA = []

G_SSATANX = G.copy()
statuses_SSATANX = statuses.copy()
t0_SSATANX = 0
data_SSATANX = {}
data_SSATANX[0] = t0_status
output_SSATANX = []

for t in np.arange(time_step,tf + time_step, time_step):

    while t0_SSA < t:
        output_SSA = SSA_full(G_SSA, t, t0_SSA, ass_rates, dis_rates, statuses_SSA)
        t0_SSA += output_SSA[0]
        statuses_SSA = output_SSA[-1]

    while t0_SSATANX < t:
        output_SSATANX = SSATANX_full(G_SSATANX, t, t0_SSATANX, ass_rates, dis_rates,k,p, statuses_SSATANX)
        t0_SSATANX += output_SSATANX[0]
        statuses_SSATANX = output_SSATANX[-1]

    data_SSA[t] = output_SSA[1:-1]
    data_SSATANX[t] = output_SSATANX[1:-1]

data_SSA = pd.DataFrame(data_SSA)
data_SSATANX = pd.DataFrame(data_SSATANX)

data_diff = abs(data_SSA - data_SSATANX)

print(data_diff)

condition = np.sqrt(-np.log(a/2)*(1 + (len(data_SSA.columns)/len(data_SSATANX.columns)))/(2*len(data_SSATANX.columns)))*num_nodes

print(f"Threshold for the distance: {condition}")

fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2,constrained_layout=True)
axes = [ax1,ax2,ax3,ax4]

status_diz = {0: "Susceptibles", 1: "Infected", 2: "Diagnosed", 3: "Dead"}

cnt = 0
for riga in data_diff.iterrows():
    riga_max = max(riga[1])
    print(f"Status: {status_diz[riga[0]]}. Observed maximum distance: {riga_max}. Is distance below the threshold? {riga_max < condition}")
    axes[cnt].plot(data_SSA.columns, data_SSA.iloc[cnt,:])
    axes[cnt].plot(data_SSATANX.columns, data_SSATANX.iloc[cnt,:])
    axes[cnt].set_title(f"{status_diz[cnt]}")
    axes[cnt].set_ylim(0,num_nodes)
    axes[cnt].set_xlabel("Time")
    axes[cnt].set_ylabel("number of nodes")
    axes[cnt].legend(["SSA","SSATANX"])
    cnt += 1

fig.suptitle(f"SSA vs SSATANX comparison ({num_nodes} nodes)")

plt.show()
