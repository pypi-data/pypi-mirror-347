import numpy as np
import numpy.linalg as la
import jax.numpy as jnp
import cvxpy as cp

from openscvx.trajoptproblem import TrajOptProblem
from openscvx.dynamics import dynamics
from openscvx.utils import qdcm, SSMP, SSM, rot, gen_vertices
from openscvx.constraints import boundary, ctcs, nodal

n = 33  # Number of Nodes
total_time = 30.0  # Total time for the simulation

s_inds = -1  # Time dilation index in Control

max_state = np.array(
    [200.0, 100, 50, 100, 100, 100, 1, 1, 1, 1, 10, 10, 10, 100]
)  # Upper Bound on the states
min_state = np.array(
    [-200.0, -100, 15, -100, -100, -100, -1, -1, -1, -1, -10, -10, -10, 0]
)  # Lower Bound on the states

initial_state = boundary(jnp.array([10.0, 0, 20, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]))
initial_state.type[6:13] = "Free"

final_state = boundary(jnp.array([10.0, 0, 20, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, total_time]))
final_state.type[3:13] = "Free"
final_state.type[13] = "Minimize"

initial_control = np.array([0.0, 0, 10, 0, 0, 0])
max_control = np.array(
    [0.0, 0, 4.179446268 * 9.81, 18.665, 18.665, 0.55562]
)  # Upper Bound on the controls
min_control = np.array(
    [0.0, 0, 0, -18.665, -18.665, -0.55562]
)  # Lower Bound on the controls


### View Planning Params ###
alpha_x = 6.0  # Angle for the x-axis of Sensor Cone
alpha_y = 6.0  # Angle for the y-axis of Sensor Cone
A_cone = np.diag(
    [
        1 / np.tan(np.pi / alpha_x),
        1 / np.tan(np.pi / alpha_y),
        0,
    ]
)  # Conic Matrix in Sensor Frame
c = jnp.array([0, 0, 1])  # Boresight Vector in Sensor Frame
norm_type = 2  # Norm Type
R_sb = jnp.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])

n_subs = 10
polytope_point = np.array(
    [
        [95.38, -54.62, 15.38],
        [95.38, -54.62, 24.62],
        [95.38, -45.38, 15.38],
        [95.38, -45.38, 24.62],
        [104.62, -54.62, 15.38],
        [104.62, -54.62, 24.62],
        [104.62, -45.38, 15.38],
        [104.62, -45.38, 24.62],
        [100.00, -52.85, 12.53],
        [100.00, -52.85, 27.47],
        [100.00, -47.15, 12.53],
        [100.00, -47.15, 27.47],
        [97.15, -57.47, 20.00],
        [97.15, -42.53, 20.00],
        [102.85, -57.47, 20.00],
        [102.85, -42.53, 20.00],
        [92.53, -50.00, 17.15],
        [92.53, -50.00, 22.85],
        [107.47, -50.00, 17.15],
        [107.47, -50.00, 22.85],
    ]
)
init_poses = []
for point in polytope_point:
    init_poses.append(point)

init_poses = init_poses

### Gate Parameters ###

n_gates = 10
gate_centers = [
    np.array([59.436, 0.0000, 20.0000]),
    np.array([92.964, -23.750, 25.5240]),
    np.array([92.964, -29.274, 20.0000]),
    np.array([92.964, -23.750, 20.0000]),
    np.array([130.150, -23.750, 20.0000]),
    np.array([152.400, -73.152, 20.0000]),
    np.array([92.964, -75.080, 20.0000]),
    np.array([92.964, -68.556, 20.0000]),
    np.array([59.436, -81.358, 20.0000]),
    np.array([22.250, -42.672, 20.0000]),
]

radii = np.array([2.5, 1e-4, 2.5])
A_gate = rot @ np.diag(1 / radii) @ rot.T
A_gate_cen = []
for center in gate_centers:
    center[0] = center[0] + 2.5
    center[2] = center[2] + 2.5
    A_gate_cen.append(A_gate @ center)
nodes_per_gate = 3
gate_nodes = np.arange(nodes_per_gate, n, nodes_per_gate)
vertices = []
for center in gate_centers:
    vertices.append(gen_vertices(center, radii))
### End Gate Parameters ###


def g_vp(p_s_I, x):
    p_s_s = R_sb @ qdcm(x[6:10]).T @ (p_s_I - x[0:3])
    return jnp.linalg.norm(A_cone @ p_s_s, ord=norm_type) - (c.T @ p_s_s)


constraints = []
constraints.append(ctcs(lambda x, u: x - max_state))
constraints.append(ctcs(lambda x, u: min_state - x))
for pose in init_poses:
    constraints.append(ctcs(lambda x, u, p=pose: g_vp(p, x)))
for node, cen in zip(gate_nodes, A_gate_cen):
    constraints.append(
        nodal(
            lambda x, u, A=A_gate, c=cen: cp.norm(A @ x[:3] - c, "inf") <= 1,
            nodes=[node],
            convex=True
        )
    )  # use local variables inside the lambda function


@dynamics
def dynamics(x, u):
    m = 1.0  # Mass of the drone
    g_const = -9.18
    J_b = jnp.array([1.0, 1.0, 1.0])  # Moment of Inertia of the drone

    # Unpack the state and control vectors
    v = x[3:6]
    q = x[6:10]
    w = x[10:13]

    f = u[:3]
    tau = u[3:]

    q_norm = jnp.linalg.norm(q)
    q = q / q_norm

    # Compute the time derivatives of the state variables
    r_dot = v
    v_dot = (1 / m) * qdcm(q) @ f + jnp.array([0, 0, g_const])
    q_dot = 0.5 * SSMP(w) @ q
    w_dot = jnp.diag(1 / J_b) @ (tau - SSM(w) @ jnp.diag(J_b) @ w)
    t_dot = 1
    return jnp.hstack([r_dot, v_dot, q_dot, w_dot, t_dot])


u_bar = np.repeat(np.expand_dims(initial_control, axis=0), n, axis=0)
x_bar = np.linspace(initial_state.value, final_state.value, n)

i = 0
origins = [initial_state.value[:3]]
ends = []
for center in gate_centers:
    origins.append(center)
    ends.append(center)
ends.append(final_state.value[:3])
gate_idx = 0
for _ in range(n_gates + 1):
    for k in range(n // (n_gates + 1)):
        x_bar[i, :3] = origins[gate_idx] + (k / (n // (n_gates + 1))) * (
            ends[gate_idx] - origins[gate_idx]
        )
        i += 1
    gate_idx += 1

R_sb = R_sb  # Sensor to body frame
b = R_sb @ np.array([0, 1, 0])
for k in range(n):
    kp = []
    for pose in init_poses:
        kp.append(pose)
    kp = np.mean(kp, axis=0)
    a = kp - x_bar[k, :3]
    # Determine the direction cosine matrix that aligns the z-axis of the sensor frame with the relative position vector
    q_xyz = np.cross(b, a)
    q_w = np.sqrt(la.norm(a) ** 2 + la.norm(b) ** 2) + np.dot(a, b)
    q_no_norm = np.hstack((q_w, q_xyz))
    q = q_no_norm / la.norm(q_no_norm)
    x_bar[k, 6:10] = q

problem = TrajOptProblem(
    dynamics=dynamics,
    constraints=constraints,
    idx_time=len(max_state)-1,
    N=n,
    time_init=total_time,
    x_guess=x_bar,
    u_guess=u_bar,
    initial_state=initial_state,  # Initial State
    final_state=final_state,
    x_max=max_state,
    x_min=min_state,
    u_max=max_control,  # Upper Bound on the controls
    u_min=min_control,  # Lower Bound on the controls
)

problem.params.prp.dt = 0.01

problem.params.scp.k_max = 50
problem.params.scp.w_tr = 2e0  # 2e0,  # Weight on the Trust Reigon
problem.params.scp.lam_cost = 2e-1  # 0e-1,  # Weight on the Minimal Time Objective
problem.params.scp.lam_vc = 1e1  # 1e1,  # Weight on the Virtual Control Objective (not including CTCS Augmentation)
problem.params.scp.ep_tr = 1e-5  # Trust Region Tolerance
problem.params.scp.ep_vb = 1e-4  # Virtual Control Tolerance
problem.params.scp.ep_vc = 1e-8  # Virtual Control Tolerance for CTCS
problem.params.scp.cost_drop = 10  # SCP iteration to relax minimal final time objective
problem.params.scp.cost_relax = 0.8  # Minimal Time Relaxation Factor
problem.params.scp.w_tr_adapt = 1.2  # Trust Region Adaptation Factor
problem.params.scp.w_tr_max_scaling_factor = 1e2  # Maximum Trust Region Weight

plotting_dict = dict(
    vertices=vertices,
    n_subs=n_subs,
    alpha_x=alpha_x,
    alpha_y=alpha_y,
    R_sb=R_sb,
    init_poses=init_poses,
    norm_type=norm_type,
)
