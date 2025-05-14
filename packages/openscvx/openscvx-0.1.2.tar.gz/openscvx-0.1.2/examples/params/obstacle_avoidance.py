import numpy as np
import jax.numpy as jnp

from openscvx.trajoptproblem import TrajOptProblem
from openscvx.dynamics import dynamics
from openscvx.constraints import boundary, ctcs
from openscvx.utils import qdcm, SSMP, SSM, generate_orthogonal_unit_vectors

n = 6
total_time = 4.0  # Total time for the simulation

max_state = np.array([200., 10, 20, 100, 100, 100, 1, 1, 1, 1, 10, 10, 10, 100])
min_state = np.array(
    [-200., -100, 0, -100, -100, -100, -1, -1, -1, -1, -10, -10, -10, 0]
)

initial_state = boundary(jnp.array([10.0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]))
initial_state.type[6:13] = "Free"

final_state = boundary(jnp.array([-10.0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, total_time]))
final_state.type[3:13] = "Free"
final_state.type[13] = "Minimize"

initial_control = np.array([0.0, 0, 50, 0, 0, 0])


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


def g_obs(center, A, x):
    value = 1 - (x[:3] - center).T @ A @ (x[:3] - center)
    return value


A_obs = []
radius = []
axes = []

obstacle_centers = [
    np.array([-5.1, 0.1, 2]),
    np.array([0.1, 0.1, 2]),
    np.array([5.1, 0.1, 2]),
]

np.random.seed(0)
for _ in obstacle_centers:
    ax = generate_orthogonal_unit_vectors()
    axes.append(generate_orthogonal_unit_vectors())
    rad = np.random.rand(3) + 0.1 * np.ones(3)
    radius.append(rad)
    A_obs.append(ax @ np.diag(rad**2) @ ax.T)


constraints = []
for center, A in zip(obstacle_centers, A_obs):
    constraints.append(ctcs(lambda x, u: g_obs(center, A, x)))
constraints.append(ctcs(lambda x, u: x - max_state))
constraints.append(ctcs(lambda x, u: min_state - x))


u_bar = np.repeat(np.expand_dims(initial_control, axis=0), n, axis=0)
x_bar = np.linspace(initial_state.value, final_state.value, n)

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
    u_max=np.array(
        [0, 0, 4.179446268 * 9.81, 18.665, 18.665, 0.55562]
    ),  # Upper Bound on the controls
    u_min=np.array(
        [0, 0, 0, -18.665, -18.665, -0.55562]
    ),  # Lower Bound on the controls
)

problem.params.scp.w_tr_adapt = 1.8

problem.params.dev.printing = True

problem.params.prp.dt = 0.01
problem.params.dis.custom_integrator = True
problem.params.cvx.cvxpygen = False

plotting_dict = dict(
    obstacles_centers=obstacle_centers,
    obstacles_axes=axes,
    obstacles_radii=radius,
)
