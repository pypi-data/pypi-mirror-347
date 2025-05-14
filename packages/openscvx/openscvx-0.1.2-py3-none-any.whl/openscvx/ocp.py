import os
import numpy.linalg as la
from numpy import block
import numpy as np
import cvxpy as cp
from cvxpygen import cpg
from openscvx.config import Config
from cvxpygen import cpg


def OptimalControlProblem(params: Config):
    ########################
    # VARIABLES & PARAMETERS
    ########################

    # Parameters
    w_tr = cp.Parameter(nonneg = True, name='w_tr')
    lam_cost = cp.Parameter(nonneg=True, name='lam_cost')

    # State
    x = cp.Variable((params.scp.n, params.sim.n_states), name='x') # Current State
    dx = cp.Variable((params.scp.n, params.sim.n_states), name='dx') # State Error
    x_bar = cp.Parameter((params.scp.n, params.sim.n_states), name='x_bar') # Previous SCP State

    # Affine Scaling for State
    S_x = params.sim.S_x
    inv_S_x = params.sim.inv_S_x
    c_x = params.sim.c_x

    # Control
    u = cp.Variable((params.scp.n, params.sim.n_controls), name='u') # Current Control
    du = cp.Variable((params.scp.n, params.sim.n_controls), name='du') # Control Error
    u_bar = cp.Parameter((params.scp.n, params.sim.n_controls), name='u_bar') # Previous SCP Control

    # Affine Scaling for Control
    S_u = params.sim.S_u
    inv_S_u = params.sim.inv_S_u
    c_u = params.sim.c_u

    # Discretized Augmented Dynamics Constraints
    A_d = cp.Parameter((params.scp.n - 1, (params.sim.n_states)*(params.sim.n_states)), name='A_d')
    B_d = cp.Parameter((params.scp.n - 1, params.sim.n_states*params.sim.n_controls), name='B_d')
    C_d = cp.Parameter((params.scp.n - 1, params.sim.n_states*params.sim.n_controls), name='C_d')
    z_d = cp.Parameter((params.scp.n - 1, params.sim.n_states), name='z_d')
    nu  = cp.Variable((params.scp.n - 1, params.sim.n_states), name='nu') # Virtual Control

    # Linearized Nonconvex Nodal Constraints
    if params.sim.constraints_nodal:
        g = []
        grad_g_x = []
        grad_g_u = []
        nu_vb = []
        for idx_ncvx, constraint in enumerate(params.sim.constraints_nodal):
            if not constraint.convex:
                g.append(cp.Parameter(params.scp.n, name = 'g_' + str(idx_ncvx)))
                grad_g_x.append(cp.Parameter((params.scp.n, params.sim.n_states), name='grad_g_x_' + str(idx_ncvx)))
                grad_g_u.append(cp.Parameter((params.scp.n, params.sim.n_controls), name='grad_g_u_' + str(idx_ncvx)))
                nu_vb.append(cp.Variable(params.scp.n, name='nu_vb_' + str(idx_ncvx))) # Virtual Control for VB

    # Applying the affine scaling to state and control
    x_nonscaled = []
    u_nonscaled = []
    for k in range(params.scp.n):
        x_nonscaled.append(S_x @ x[k] + c_x)
        u_nonscaled.append(S_u @ u[k] + c_u)

    constr = []
    cost = lam_cost * 0

    #############
    # CONSTRAINTS
    #############
    idx_ncvx = 0
    if params.sim.constraints_nodal:
        for constraint in params.sim.constraints_nodal:
            if constraint.nodes is None:
                nodes = range(params.scp.n)
            else:
                nodes = constraint.nodes

            if constraint.convex:
                constr += [constraint(x_nonscaled[node], u_nonscaled[node]) for node in nodes]

            elif not constraint.convex:
                constr += [((g[idx_ncvx][node] + grad_g_x[idx_ncvx][node] @ dx[node] + grad_g_u[idx_ncvx][node] @ du[node])) == nu_vb[idx_ncvx][node] for node in nodes]
                idx_ncvx += 1

    for i in range(params.sim.idx_x_true.start, params.sim.idx_x_true.stop):
        if params.sim.initial_state.type[i] == 'Fix':
            constr += [x_nonscaled[0][i] == params.sim.initial_state.value[i]]  # Initial Boundary Conditions
        if params.sim.final_state.type[i] == 'Fix':
            constr += [x_nonscaled[-1][i] == params.sim.final_state.value[i]]   # Final Boundary Conditions
        if params.sim.initial_state.type[i] == 'Minimize':
            cost += lam_cost * x_nonscaled[0][i]
        if params.sim.final_state.type[i] == 'Minimize':
            cost += lam_cost * x_nonscaled[-1][i]
        if params.sim.initial_state.type[i] == 'Maximize':
            cost += lam_cost * x_nonscaled[0][i]
        if params.sim.final_state.type[i] == 'Maximize':
            cost += lam_cost * x_nonscaled[-1][i]

    if params.scp.uniform_time_grid:
        constr += [x_nonscaled[i][params.sim.idx_t] - x_nonscaled[i-1][params.sim.idx_t] == x_nonscaled[i-1][params.sim.idx_t] - x_nonscaled[i-2][params.sim.idx_t] for i in range(2, params.scp.n)] # Uniform Time Step

    constr += [0 == la.inv(S_x) @ (x_nonscaled[i] - x_bar[i] - dx[i]) for i in range(params.scp.n)] # State Error
    constr += [0 == la.inv(S_u) @ (u_nonscaled[i] - u_bar[i] - du[i]) for i in range(params.scp.n)] # Control Error

    constr += [x_nonscaled[i] == \
                      cp.reshape(A_d[i-1], (params.sim.n_states, params.sim.n_states)) @ x_nonscaled[i-1] \
                    + cp.reshape(B_d[i-1], (params.sim.n_states, params.sim.n_controls)) @ u_nonscaled[i-1] \
                    + cp.reshape(C_d[i-1], (params.sim.n_states, params.sim.n_controls)) @ u_nonscaled[i] \
                    + z_d[i-1] \
                    + nu[i-1] for i in range(1, params.scp.n)] # Dynamics Constraint
    
    constr += [u_nonscaled[i] <= params.sim.max_control for i in range(params.scp.n)]
    constr += [u_nonscaled[i] >= params.sim.min_control for i in range(params.scp.n)] # Control Constraints

    constr += [x_nonscaled[i][params.sim.idx_x_true] <= params.sim.max_state[params.sim.idx_x_true] for i in range(params.scp.n)]
    constr += [x_nonscaled[i][params.sim.idx_x_true] >= params.sim.min_state[params.sim.idx_x_true] for i in range(params.scp.n)] # State Constraints (Also implemented in CTCS but included for numerical stability)

    ########
    # COSTS
    ########
    
    inv = block([[inv_S_x, np.zeros((S_x.shape[0], S_u.shape[1]))], [np.zeros((S_u.shape[0], S_x.shape[1])), inv_S_u]])
    cost += sum(w_tr * cp.sum_squares(inv @ cp.hstack((dx[i], du[i]))) for i in range(params.scp.n))  # Trust Region Cost
    cost += sum(params.scp.lam_vc * cp.sum(cp.abs(nu[i-1])) for i in range(1, params.scp.n)) # Virtual Control Slack
    
    idx_ncvx = 0
    if params.sim.constraints_nodal:
        for constraint in params.sim.constraints_nodal:
            if not constraint.convex:
                cost += params.scp.lam_vb * cp.sum(cp.pos(nu_vb[idx_ncvx]))
                idx_ncvx += 1

    for idx, nodes in zip(np.arange(params.sim.idx_y.start, params.sim.idx_y.stop), params.sim.ctcs_node_intervals):  
        if nodes[0] == 0:
            start_idx = 1
        else:
            start_idx = nodes[0]
        constr += [cp.abs(x_nonscaled[i][idx] - x_nonscaled[i-1][idx]) <= params.sim.max_state[idx] for i in range(start_idx, nodes[1])]
        constr += [x_nonscaled[0][idx] == 0]

    
    #########
    # PROBLEM
    #########
    prob = cp.Problem(cp.Minimize(cost), constr)
    if params.cvx.cvxpygen:
        # Check to see if solver directory exists
        if not os.path.exists('solver'):
            cpg.generate_code(prob, solver = params.cvx.solver, code_dir='solver', wrapper = True)
        else:
            # Prompt the use to indicate if they wish to overwrite the solver directory or use the existing compiled solver
            overwrite = input("Solver directory already exists. Overwrite? (y/n): ")
            if overwrite.lower() == 'y':
                cpg.generate_code(prob, solver = params.cvx.solver, code_dir='solver', wrapper = True)
            else:
                pass
    return prob