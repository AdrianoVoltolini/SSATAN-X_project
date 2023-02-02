tf = 5
n_graphs = 4

num_nodes = 100 
num_edges = int(0.15*num_nodes*(num_nodes-1)/2) # WARNING: non mettere più di N(N-1)/2 edges!

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
gamma = 0.04 #infezione
w_gamma = 0.5 #penalità per essere diagnosticato
delta = 0.5 #diagnosi
beta = 0.08 # morte

# range per scelta dei rates dei nodi
ass_range = (0.5,2.5)
dis_range = (0.4,2.0)

# parametri tau-leaping
k = 10 # fai cross validation
epsilon = 0.03 
alpha = 0.75
alpha_star = 0.9
omega = 0.98
omega_star = 1.02
p = 10 # fai cross validation

# parametri KS test
a = 0.05
t_decimals = 6

