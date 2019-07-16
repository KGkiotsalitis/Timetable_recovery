# Timetable_recovery

This repository is meant for publishing some of the code related to the **timetable recovery problem** applied in public transit (in particular, **high-frequency metro lines** with stable dwell times).

Currently, this repository contains the main model and its implementation in the toy network:

`timetable_model_toy_network_demonstration.py` 

This script contains all necessary functions to calculate the optimal dispatching times of all upstream trips of a disrupted train. 

# Referencing

In case you use this code for scientific purposes, it is appreciated if you provide a citation to the paper **Timetable recovery after disruptions in metro lines: infeasibility, nonlinearities and convex reformulation** once it is publicly available.

# License

MIT License

# Dependencies

Note that the script is programmed in Python and for the optimization we use Gurobi. Running or modifying the script requires an installed version of **Python 3.7** and **gurobipy**. In addition, the following libraries should also be installed:
* numpy 
* math
