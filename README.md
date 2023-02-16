# SSATAN-X project

Python implementation of the SSATAN-X algorithm that works on Networkx graphs. This project was done for the course "Mathematical Modeling and Simulation", offered by the University of Trento. 

Requires: Python 3.7+, Networkx 3.0+, Numpy, Pandas, Matplotlib

Optional: ffmpeg if you want to save a gif, line_profiler if you want to open or create .lprof files

Main scripts:
 - parameters.py: contains all the parameters used in our project. Changing values in here will change the outputs of the other python scripts.
 - ContactNetwork.py: contains the function “graph_creator” that uses the NetworkX python module to create an initial, randomly generated graph that resembles the ones considered in the paper. This function returns a tuple containing the graph itself, two arrays containing the association and dissociation rates of the nodes, and an array containing the initial statuses of the nodes.
 - SSA.py: contains two functions, called “SSA_full” and “SSA_contact”. The first function is an implementation of the SSA algorithm that works on NetworkX graphs and it is capable of simulating both the contact and the epidemic dynamics of the system. On the other hand the second function, as the name suggests, is only capable of simulating the contact dynamics. “SSA_contact” is used in the tau-leaping algorithm in case tau is too small. Calling these functions will execute a single reaction.
 - Tau_Leaping.py: contains two functions, called “tau_leap_old” and “tau_leap_new”. The first function is a basic tau-leaping algorithm implementation that works on NetworkX graphs and is capable of simulating the contact dynamics of the system. The second function is another implementation of tau-leaping but more similar to the one used by the authors of the paper. Calling these functions will execute a single tau-leap.
 - SSATANX.py: contains a function called “SSATANX_full”, which is a full implementation of the SSATAN-X algorithm capable of working on NetworkX graphs. Calling this function will execute a single time step. 

Additional scripts:
 - grafici.py: unused script that creates plots describing a SSA-based simulation and a SSATAN-X based simulation. 
 - K_vs_P.py: used to create a contour plot (figure 2 of the report) that describes how the speed of SSATAN-X changes depending on the values of K and P.
 - KS_test.py: used to compare two empirical distribution functions (SSA vs SSATAN-X). Also to create the plots shown in figure 7 of the report.
 - plotter.py: used to create an animation shown in figure 1 of the report and during the presentation.
 - speed.py: used to measure the average speed of the SSA and the SSATAN-X algorithms, and to create the plot in figure 9 of the report.
