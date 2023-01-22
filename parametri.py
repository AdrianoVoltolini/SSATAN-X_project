t = 0
tf = 1

num_nodes = 10
num_edges = 20 # WARNING: non mettere più di N(N-1)/2 edges!

#percentuale della popolazione iniziale
t0_infetti = 0.2 
t0_diagnosed = 0.1
t0_morti = 0.1
t0_sani = 1 - t0_infetti - t0_diagnosed - t0_morti

#weights degli association rates
w_sano = 1
w_infetto = 1
w_diagnosed = 1/3
w_dead = 0

# range per scelta dei rates dei nodi
ass_range = (0.5,2.5) # nel paper hanno usato 0.5 e 2.5
dis_range = (0.4,2.0) # nel paper hanno usato 0.4 e 2.0

