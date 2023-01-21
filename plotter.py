from matplotlib import pyplot as plt, animation
import networkx as nx
#import ffmpeg

from ContactNetwork import G
from SSA import SSA

fig = plt.figure()

pos = nx.circular_layout(G) # determina come vengono disposti i nodi

def animate(frame):
    fig.clear()
    SSA(G)

    sane_nodes = []
    infected_nodes = []
    diagnosed_nodes = []
    morti_nodes = []

    for i in G.nodes(): # smista i nodi in base allo status per colorarli dopo 
        if nx.get_node_attributes(G,"status")[i] == 0:
            sane_nodes.append(i)
        elif nx.get_node_attributes(G,"status")[i] == 1:
            infected_nodes.append(i)
        elif nx.get_node_attributes(G,"status")[i] == 2:
            diagnosed_nodes.append(i)
        else:
            morti_nodes.append(i)

    nx.draw_networkx_nodes(G, pos, nodelist=sane_nodes, node_color="blue") # disegna e colora i nodi
    nx.draw_networkx_nodes(G, pos, nodelist=infected_nodes, node_color="red")
    nx.draw_networkx_nodes(G, pos, nodelist=diagnosed_nodes, node_color="brown")
    nx.draw_networkx_nodes(G, pos, nodelist=morti_nodes, node_color="black")

    nx.draw_networkx_edges(G,pos) # disegna gli edge
    plt.title(f"SSA Contact Dynamics. Num of Edges: {len(G.edges)}")

ani = animation.FuncAnimation(fig, animate, interval=500, frames=120)
plt.show()

# per salvare il video
# writervideo = animation.FFMpegWriter(fps=2)
# ani.save('SSA_Contact_dynamics.mp4', writer=writervideo)
# plt.close()