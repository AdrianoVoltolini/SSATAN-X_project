tf = 5
n_graphs = 4

num_nodes = 10 
num_edges = 20 # WARNING: non mettere più di N(N-1)/2 edges!

#frazioni della popolazione iniziale
t0_infetti = 0.1 
t0_diagnosed = 0
t0_morti = 0
t0_sani = 1 - t0_infetti - t0_diagnosed - t0_morti

#weights degli association rates
w_sano = 1
w_infetto = 1
w_diagnosed = 1/3
w_dead = 0

#parametri dell'epidemic dynamics
gamma = 0.16 #infezione
w_gamma = 0.5 #penalità per essere diagnosticato
delta = 0.5 #diagnosi
beta = 0.08 # morte

# range per scelta dei rates dei nodi
ass_range = (0.5,2.5)
dis_range = (0.4,2.0)

# parametri tau-leaping
k = 10
epsilon = 0.03 #bisognerebbe fare cross validation per sceglierlo. Determina margine d'errore
alpha = 0.75
p = 100


