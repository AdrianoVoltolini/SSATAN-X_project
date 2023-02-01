import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from ContactNetwork import graph_creator
from SSA import SSA_full
from SSATANX import SSATANX_full
from parametri import tf, num_nodes, t0_sani, t0_infetti, t0_diagnosed, t0_morti, k,p


G, ass_rates, dis_rates, statuses = graph_creator()

G_SSA = G.copy()
statuses_SSA = statuses.copy()

t0_status = (round(num_nodes*t0_sani), round(num_nodes*t0_infetti), round(num_nodes*t0_diagnosed), round(num_nodes*t0_morti))

t0_SSA = 0
data_SSA = {}
data_SSA[0] = t0_status

while t0_SSA < tf:
    output = SSA_full(G_SSA, ass_rates, dis_rates, statuses_SSA)
    t0_SSA += output[0]
    statuses_SSA = output[-1]
    data_SSA[t0_SSA] = output[1:-1]

data_SSA = pd.DataFrame(data_SSA)


G_SSATANX = G.copy()
statuses_SSATANX = statuses.copy()

t0_SSATANX = 0
data_SSATANX = {}
data_SSATANX[0] = t0_status


while t0_SSATANX < tf:
    output = SSATANX_full(G_SSATANX, tf, t0_SSATANX, ass_rates, dis_rates,k,p, statuses_SSATANX)
    t0_SSATANX += output[0]
    statuses_SSATANX = output[-1]
    data_SSATANX[t0_SSATANX] = output[1:-1]

data_SSATANX = pd.DataFrame(data_SSATANX)

SSA_times = []
SSATANX_times = []

# uno schifo ma funziona. Trova tempi di SSA e SSATAN sufficientemente vicini, arrotondati al quarto decimale
for SSATANX_time in data_SSATANX.columns:
    for SSA_time in data_SSA.columns:
        if str(SSA_time).startswith(str(round(SSATANX_time,3))):
            if SSATANX_time not in SSATANX_times:
                SSA_times.append(SSA_time)
                SSATANX_times.append(SSATANX_time)


SSATANX_rounded = data_SSATANX.loc[:,SSATANX_times]
SSATANX_rounded.columns = [round(x,3) for x in SSATANX_rounded.columns]

SSA_rounded = data_SSA.loc[:,SSA_times]
SSA_rounded.columns = [round(x,3) for x in SSATANX_rounded.columns]

print(len(SSA_rounded.columns))

d0 = np.max(abs(SSATANX_rounded.loc[0,:] - SSA_rounded.loc[0,:]))
d1 = np.max(abs(SSATANX_rounded.loc[1,:] - SSA_rounded.loc[1,:]))
d2 = np.max(abs(SSATANX_rounded.loc[2,:] - SSA_rounded.loc[2,:]))
d3 = np.max(abs(SSATANX_rounded.loc[3,:] - SSA_rounded.loc[3,:]))

d_mean = (d0+d1+d2+d3)/4

C_05 = 1.358
condition = C_05*np.sqrt((len(SSATANX_rounded.columns)*2)/(len(SSATANX_rounded.columns**2)))
print(condition, d_mean, condition > d_mean) 
