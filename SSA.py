#import numpy as np
#import matplotlib.pyplot as plt
import networkx as nx
import random

from ContactNetwork import G

# inizializzazione
t=0
tf = 10
ass_rates = list(nx.get_node_attributes(G,"ass_rate").values()) # questo comando funziona correttamente solo se si usa python 3.7+


#while t < tf:
a0 = 0
ass_propensities = []

#computa le propensities e a0
for i in range(len(ass_rates)):
    for j in range(i+1,len(ass_rates)):
        if (i,j) not in G.edges(): # WARNING: gli edges di G NON sono in ordine!
            propensity = ass_rates[i]*ass_rates[j] # le propensities sono (lambda_j * lambda_k)
            a0 += propensity
            ass_propensities.append(((i,j),propensity))

print(G.edges())
print(ass_propensities)
print(a0)

# genera due numeri random. Seguo il libro di marchetti perché nel paper non si capisce una minchia
r1 = random.uniform(0,1)
r2 = random.uniform(0,1)


