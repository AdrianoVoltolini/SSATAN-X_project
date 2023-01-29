from matplotlib import pyplot as plt
import networkx as nx
import numpy as np

from ContactNetwork import graph_creator
from SSA import SSA_full
from SSATANX import SSATANX_full
from parametri import tf, num_nodes, t0_sani, t0_infetti, t0_diagnosed, t0_morti
import pandas as pd

fig, (ax1, ax2) = plt.subplots(2,1,constrained_layout=True)

G = graph_creator()

G_SSA = G.copy()

t0_status = (round(num_nodes*t0_sani), round(num_nodes*t0_infetti), round(num_nodes*t0_diagnosed), round(num_nodes*t0_morti))

t0_SSA = 0
data_SSA = {}
data_SSA[0] = t0_status

while t0_SSA < tf:
    output = SSA_full(G_SSA)
    t0_SSA += output[0]
    data_SSA[t0_SSA] = output[1:]

data_SSA = pd.DataFrame(data_SSA)

ax1.set_title("SSA (100 nodes)")

ax1.plot(data_SSA.iloc[0,:],c="blue")
ax1.plot(data_SSA.iloc[1,:],c="red")
ax1.plot(data_SSA.iloc[2,:],c="brown")
ax1.plot(data_SSA.iloc[3,:],c="black")

ax1.set_xlim(left=0,right=5)
ax1.set_xlabel("Time")
ax1.set_ylabel("number of nodes")

############################################################

G_SSATANX = G.copy()

t0_SSATANX = 0
data_SSATANX = {}
data_SSATANX[0] = t0_status


while t0_SSATANX < tf:
    output = SSATANX_full(G_SSATANX)
    t0_SSATANX += output[0]
    data_SSATANX[t0_SSATANX] = output[1:]

data_SSATANX = pd.DataFrame(data_SSATANX)

ax2.set_title("SSATANX (100 nodes)")

ax2.plot(data_SSATANX.iloc[0,:],c="blue")
ax2.plot(data_SSATANX.iloc[1,:],c="red")
ax2.plot(data_SSATANX.iloc[2,:],c="brown")
ax2.plot(data_SSATANX.iloc[3,:],c="black")

ax2.set_xlim(left=0,right=5)
ax2.set_xlabel("Time")
ax2.set_ylabel("number of nodes")


plt.show()

     
