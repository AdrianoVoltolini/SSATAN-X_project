from matplotlib import pyplot as plt, animation
import networkx as nx
import numpy as np
#import ffmpeg

from ContactNetwork import graph_creator
from SSA import SSA_full
from SSATANX import SSATANX_full
from parametri import tf, num_nodes

G, ass_rate, dis_rate, old_statuses = graph_creator()

fig = plt.figure()

pos = nx.circular_layout(G) # determina come vengono disposti i nodi

G.name = str(0)

def animate(frame):
    fig.clear()
    statuses = [nx.get_node_attributes(G,"status")[x] for x in range(num_nodes)]
    t = np.float64(G.name)
    #output = SSATANX_full(G, tf, t, ass_rate, dis_rate, statuses)
    output = SSA_full(G, ass_rate, dis_rate, statuses)
    
    new_statuses = output[-1]

    G.name = str(t + output[0])

    sane_nodes = []
    infected_nodes = []
    diagnosed_nodes = []
    morti_nodes = []

    for i in range(num_nodes): # smista i nodi in base allo status per colorarli dopo 
        if new_statuses[i] == 0:
            sane_nodes.append(i)
        elif new_statuses[i] == 1:
            infected_nodes.append(i)
        elif new_statuses[i] == 2:
            diagnosed_nodes.append(i)
        else:
            morti_nodes.append(i)

    plt.title(f"SSA Contact and Epidemic Dynamics. t = {t:.2f}")

    # nx.draw_networkx_edges(G,pos) # disegna gli edge

    nx.draw_networkx_nodes(G, pos, nodelist=sane_nodes, node_color="blue") # disegna e colora i nodi
    nx.draw_networkx_nodes(G, pos, nodelist=infected_nodes, node_color="red")
    nx.draw_networkx_nodes(G, pos, nodelist=diagnosed_nodes, node_color="brown")
    nx.draw_networkx_nodes(G, pos, nodelist=morti_nodes, node_color="black")

    plt.axis([-1.2,1.2,-1.2,1.2]) #margini di matplotlib
    plt.tight_layout()

ani = animation.FuncAnimation(fig, animate, interval=100, frames=360)
plt.show()

# per salvare il video
# writervideo = animation.FFMpegWriter(fps=6)
# ani.save('SSA_dynamics.mp4', writer=writervideo)
# plt.close()