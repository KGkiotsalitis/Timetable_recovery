import numpy as np

S = 4 #number of stops
n = 3 #number of trips following the disrupted train that can modify their dispatching times
set_S = range(1, S+1)#set of stops
set_N = range(1, n+1)#set of trips
set_N_1 = range(2, n+1)#set of trips except the 1st one
set_S_r = range(2,S)#set of stops where we measure the service regularity
set_S_1 = range(2,S+1)#set of stops ignoring stop 1
h_min=300 #minimum allowed dispatching headway between two successive trips in seconds
h_max=900 #maximum allowed dispatching headway between two successive trips in seconds
h_js = {(j,s): 600 for j in set_N for s in set_S_r} #target headways in seconds
d = {1:600, 2:1200, 3:1800} #originally planned dispatching times of trains in set_N
a_0 = {2:900, 3:1600} #arrival times of the already dispatched train 0 at the stops where we measure regularity
b = {1: 660,2: 1260,3: 1860} #latest possible dispathcing times to avoid schedule sliding (in seconds)
k_js = {(j,s): 30 for j in set_N for s in set_S_r} #pre-determined dwell times at each stop, in seconds
pi = {1:660, 2:1220, 3:1820} #earliest possible dispatching time of each trip due to circulation limitations
t = {(1,1): 900, (1,2):720, (1,3):800, (2,1):920, (2,2):700, (2,3):800, (3,1):880, (3,2):640, (3,3):800}
M=100000 #a very large number
tilde_d_0=0 # dispatching time of trip 0

c_js_matrix=np.zeros((n+2,S+1))
for j in set_N:
    for s in range(2,S+1):
        t_sum=0;k_sum=0
        if s==2:
            t_sum=t[j,1]
        else:
            for phi in range(1,s):
                t_sum=t_sum+t[j,phi]
            for phi in range(2,s):
                k_sum=k_sum+k_js[j,phi]
        c_js_matrix[j][s]=d[j]+t_sum+k_sum

c_js = {(j,s): c_js_matrix[j][s] for j in set_N for s in set_S_r}



print(h_js[1,2]) #call dictionary element
print(b[2])
print(c_js[2,3])



from gurobipy import *
m = Model("metro_dispatching_model_Gurobi_solver")

#Create variables
x = {(j) : m.addVar(vtype=GRB.CONTINUOUS,
                        name="x".format(j)) for j in set_N}

v = {(j) : m.addVar(vtype=GRB.CONTINUOUS,
                        name="v".format(j)) for j in set_N}

'''
a = {(j,s) : m.addVar(vtype=GRB.CONTINUOUS,
                        name="a_j_s".format(j,s)) for j in set_N for s in set_S_1}

h = {(j,s) : m.addVar(vtype=GRB.CONTINUOUS,
                        name="h_j_s".format(j,s)) for j in set_N for s in set_S_1}
'''

m.update()

#Create Objective function
objective = (sum( (x[1] + c_js[1,s] - a_0[s] - h_js[1,s])*(x[1] + c_js[1,s] - a_0[s] - h_js[1,s]) for s in set_S_r)+
             sum( (x[j] + c_js[j,s] - (x[j-1]+c_js[j-1,s]) - h_js[j,s])*(x[j] + c_js[j,s] - (x[j-1]+c_js[j-1,s]) - h_js[j,s]) for j in set_N_1 for s in set_S_r)+
             sum(M*v[j] for j in set_N))

m.ModelSense = GRB.MINIMIZE
m.setObjective(objective)

# Add Constraints
constraints = {(j):m.addConstr(
        lhs= d[j]+x[j]-d[j-1]-x[j-1],
        sense=GRB.LESS_EQUAL,
        rhs=h_max,
        name="c7a".format(j))
    for j in set_N_1}
constraints2 = {(j):m.addConstr(
        lhs= d[j]+x[j]-d[j-1]-x[j-1],
        sense=GRB.GREATER_EQUAL,
        rhs=h_min,
        name="c7b".format(j))
    for j in set_N_1}

m.addConstr(d[1]+x[1]-tilde_d_0 <= h_max, "c8a")
m.addConstr(d[1]+x[1]-tilde_d_0 >= h_min, "c8b")

constraints3 = {(j):m.addConstr(
        lhs= d[j]+x[j],
        sense=GRB.GREATER_EQUAL,
        rhs=pi[j],
        name="c9".format(j))
    for j in set_N}

constraints4 = {(j):m.addConstr(
        lhs= v[j],
        sense=GRB.GREATER_EQUAL,
        rhs=0,
        name="cadd1".format(j))
    for j in set_N}

constraints5 = {(j):m.addConstr(
        lhs= v[j],
        sense=GRB.GREATER_EQUAL,
        rhs=d[j]+x[j]-b[j],
        name="cadd2".format(j))
    for j in set_N}

#Solve and print solution
m.optimize() #Solve program with Gurobi
print([(v.varName, v.X) for v in m.getVars() if abs(v.obj) > 1e-6]) #print optimal solution

