## R simulations

We cannot find the original source code used by Marcella to produce the plots
in Figure 3 and 4 of the paper. Figure 3 compared the "ABM" simulations
(written in R) with the mean-field approximation. For the latter, I do have
Python code that can be used to recreate the mean-field dynamic. For the
former, we do have the code of the simulator with the segregated model. This
code launches a single simulation for a given set of parameter; it does not
systematically vary the parameters, and we cannot find the original source code
used to do that (if one was ever created). So we will need to replicate this. 

Marcella's code uses three R scripts, one to set up the main parameters of the
model (`launch_simulation.R`), one to set up the network
(`hoaxspread_create_net.R`), and one for the simulation itself
(`hoaxspread_process.R`). At the end of the simulation, plots are created and
the data are save in `.Rdata` files. 

This setup allows to run one simulation, but since I will need to
systematically vary the parameters, I will replace the main launch script with
a Python code that generates a parameter grid, and use rpy2 to set up an
environment in which then I can source the two scripts for creating the network
and running the simulation. The files are going to be untouched; only this
driver for the parameter sweep will need to be written, along with code to load
the saved data and produce the plots.

## To-do

- [X] Install R and rpy2 in misinfo_spread environment;
- [ ] Create Python script that replaces `launch_simulation.R` and sets all the
  parameters in the global environment;
- [ ] Source `hoaxspread_create_net.R` and `hoaxspread_process.R`, making sure
  to set the working directory to the experiment folder;
- [ ] Check the name of the created files. If the name include the parameter
  values, then they can all be created in the same directory. If not, different
  directories will need to be created;
- [ ] Write function to load all the final densities from the various runs and
  plot the heatmaps
- [ ] Find suitable value of the number of simulation steps
- [ ] Launch simulation.
