import numpy as np
#import matplotlib.pyplot as plt
import networkx as nx
import random

from ContactNetwork import G

# inizializzazione
t=0
tf = 10
ass_rates = np.array(list(nx.get_node_attributes(G,"ass_rate").values()))
ass_propensities = []

#while t < tf:
a0 = 0

#computa le propensities e a0
for i in range(len(ass_rates)):
    for j in range(len(ass_rates)):
        if i<j:
            propensity = ass_rates[i]*ass_rates[j] # le propensities sono (lambda_j * lambda_k)
            a0 += propensity
            ass_propensities.append(((i,j),propensity))

# genera due numeri random
r1 = random.uniform()
r2 = random.uniform()




print(ass_propensities)
a0 = 0

# while t<tF:
#     r_matrix = 