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

print(ass_propensities)

# genera due numeri random. Ho deciso di seguire il libro di marchetti perché nel paper non si capisce una minchia
r1 = random.uniform(0,1)
r2 = random.uniform(0,1)

print(r1,r2)

a0 = 0

# while t<tF:
#     r_matrix = 