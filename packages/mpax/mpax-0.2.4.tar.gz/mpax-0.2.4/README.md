<p align="center">
  <img src="https://github.com/MIT-Lu-Lab/mpax/blob/main/docs/mpax.png" alt="MPAX" width="360">
</p>

# MPAX: Mathematical Programming in JAX

[![pypi](https://img.shields.io/pypi/v/mpax.svg?color=brightgreen)](https://pypi.org/pypi/mpax/)
![CI status](https://github.com/MIT-Lu-Lab/MPAX/actions/workflows/test.yml/badge.svg?branch=main)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/MIT-Lu-Lab/MPAX/blob/main/LICENSE)
[![arXiv](https://img.shields.io/badge/arXiv-2412.09734-B31B1B.svg)](https://arxiv.org/abs/2412.09734)

MPAX is a hardware-accelerated, differentiable, batchable, and distributable solver for mathematical programming in JAX, designed to integrate with modern computational and deep learning workflows:

- **Hardware accelerated**: executes on multiple architectures including CPUs, GPUs and TPUs.
- **Differentiable**: computes derivatives of solutions with respect to inputs through implicit or unrolled differentiation.
- **Batchable**: solves multiple problem instances of the same shape simultaneously.
- **Distributed**: executes in parallel across multiple devices, such as several GPUs.

MPAX's primary motivation is to integrate mathematical programming with deep learning pipelines. To achieve this, MPAX aligns its algorithms and implementations with the requirements of deep learning hardware, ensuring compatibility with GPUs and TPUs. By being differentiable, MPAX can integrate directly into the backpropagation process of neural network training. Its batchability and distributability further enable scalable deployment in large-scale applications. 

Currently, MPAX supports **linear programming (LP)** and **quadratic programming (QP)**, the foundational problems in mathematical programming. Future releases will expand support to include other problem classes of mathematical programming.

## Installation

You can install the latest released version of MPAX from PyPI via:
```
pip install mpax
```
or you can install the latest development version from GitHub:
```
pip install git+https://github.com/MIT-Lu-Lab/mpax.git
```

## Quickstart

Currently, MPAX focuses on solving linear programming (LP) and quadratic programming (QP) problems of the following form:

```math
\begin{equation}
\tag{LP}
\begin{aligned}
\min_{l \leq x \leq u}\ & c^\top x \\
\text{s.t.}\ & A x = b \\
& Gx \geq h
\end{aligned}
\end{equation}
```

```math
\begin{equation}
\tag{QP}
\begin{aligned}
\min_{l \leq x \leq u}\ & \frac{1}{2} x^\top Q x + c^\top x \\
\text{s.t.}\ & A x = b \\
& Gx \geq h
\end{aligned}
\end{equation}
```

MPAX implements two state-of-the-art first-order methods:
* $\boldsymbol{\mathrm{ra}}$**PDHG**: **restarted average Primal-Dual Hybrid Gradient**, supporting both LP ([paper](https://arxiv.org/abs/2311.12180)) and QP ([paper](https://arxiv.org/abs/2311.07710)). 
* $\boldsymbol{\mathrm{r^2}}$**HPDHG**: **reflected restarted Halpern Primal-Dual Hybrid Gradient**, supporting LP only ([paper](https://arxiv.org/abs/2407.16144)).

### Solving a Single LP/QP Problem
MPAX supports both dense and sparse formats for the constraint matrix, controlled by the `use_sparse_matrix` parameter.
```python
from mpax import create_lp, create_qp, raPDHG, r2HPDHG

# Create LP using sparse matrix format (default)
lp = create_lp(c, A, b, G, h, l, u) # use_sparse_matrix=True by default
# Create LP using dense matrix format
lp = create_lp(c, A, b, G, h, l, u, use_sparse_matrix=False)
solver = r2HPDHG(eps_abs=1e-4, eps_rel=1e-4, verbose=True)
result = solver.optimize(lp)

# Or create QP
qp = create_qp(Q, c, A, b, G, h, l, u)
qp = create_qp(Q, c, A, b, G, h, l, u, use_sparse_matrix=False)
solver = raPDHG(eps_abs=1e-4, eps_rel=1e-4, verbose=True)
result = solver.optimize(lp)
```

### Batch solving
Batch solving allows you to solve multiple LP problems of the same shape simultaneously by using `jax.vmap`:
```python
import jax.numpy as jnp
from mpax import create_lp, r2HPDHG

def single_optimize(c_vector):
    lp = create_lp(c_vector, A, b, G, h, l, u)
    solver = r2HPDHG(eps_abs=1e-4, eps_rel=1e-4, verbose=True)
    result = solver.optimize(lp)
    obj = jnp.dot(c_vector, result.primal_solution)
    return result.primal_solution, obj

batch_size = 100
batch_c = jnp.tile(c, (batch_size, 1))
batch_optimize = jax.vmap(single_optimize)

result = batch_optimize(batch_c)
```

### Device parallelism
Distribute computations across devices using JAX’s sharding capabilities:

```python
import jax
from mpax import create_lp

# Data sharding
mesh = jax.make_mesh((2,), ('x',))
sharding = jax.sharding.NamedSharding(mesh, P('x',))

A_sharded = jax.device_put(A, sharding)
lp_sharded = create_lp(c, A_sharded, b, G, h, l, u)

solver = r2HPDHG(eps_abs=1e-4, eps_rel=1e-4, verbose=True)
jit_optimize = jax.jit(solver.optimize)
result = jit_optimize(lp_sharded)
```

### Differentiation
An Example of computing the forward and backward passes of the "Smart Predict-then-Optimize+" loss using MPAX and `jax.custom_jvp()`.
```python
import jax
import jax.numpy as jnp

@jax.custom_vjp
def pso_fun(pred_cost, true_cost, true_sol, true_obj):
    sol, obj = batch_optimize(2*pred_cost - true_cost)
    loss = -obj + 2 * jnp.sum(pred_cost * true_sol, axis=1) - true_obj
    loss = jnp.mean(loss)
    return loss, sol

def spo_fwd(pred_cost, true_cost, true_sol, true_obj):
    loss, sol = pso_fun(pred_cost, true_cost, true_sol, true_obj)
    return loss, (sol, true_sol)

def spo_bwd(res, g):
    sol, true_sol = res
    grad = 2 * (true_sol - sol)
    # No gradients needed for true_cost, true_sol, or true_obj
    return grad * g, None, None, None

pso_fun.defvjp(spo_fwd, spo_bwd)
```

### Solver Options

**General options**
| Parameter                     | Type   | Default   | Description                                                             |
|:-------------------------------:|:--------:|:-----------:|-------------------------------------------------------------------------|
| `verbose`                    | bool   | `False`   | Enables detailed logging of the solver's progress.                     |
| `debug`                      | bool   | `False`   | Activates additional debugging information.                            |
| `display_frequency`          | int    | `10`      | Frequency (in every termination check) for displaying solver statistics.            |
| `jit`                        | bool   | `True`    | Enables JIT (Just-In-Time) compilation for faster execution.            |
| `unroll`                     | bool   | `False`   | Unrolls iteration loops  |
| `warm_start`                 | bool   | `False`   | Whether to perform warm starting  |
| `feasibility_polishing`      | bool   | `False`   | Whether to perform feasibility polishing  |

**Termination**
| Parameter                        | Type   | Default     | Description                                                           |
|:----------------------------------:|:--------:|:-------------:|-----------------------------------------------------------------------|
| `eps_abs`                       | float  | `1e-4`      | Absolute tolerance for convergence.                                   |
| `eps_rel`                       | float  | `1e-4`      | Relative tolerance for convergence.                                   |
| `eps_primal_infeasible`         | float  | `1e-8`      | Tolerance for detecting primal infeasibility.                         |
| `eps_dual_infeasible`           | float  | `1e-8`      | Tolerance for detecting dual infeasibility                           |
| `eps_feas_polish`               | float  | `1e-6`      | Tolerance for feasibility polishing |
| `iteration_limit`               | int    | `max_int`   | Maximum number of iterations allowed (interpreted as unlimited by default) |

**Precision**

By default, MPAX uses single-precision (32-bit). To enable double-precision (64-bit), add the following at the start of your script:

```python
jax.config.update("jax_enable_x64", True)
```

**Determinism**

Floating-point computations on GPUs in JAX may produce non-deterministic results. To ensure deterministic results, set:
```python
os.environ["XLA_FLAGS"] = "--xla_gpu_deterministic_ops=true"
```
**Important**: If you are using batch solving, do not enable `--xla_gpu_deterministic_ops=true`, as it can significantly degrade performance.

## Citation
If MPAX is useful or relevant to your research, please kindly recognize our contributions by citing our paper:
```bibtex
@article{lu2024mpax,
  title={MPAX: Mathematical Programming in JAX},
  author={Lu, Haihao and Peng, Zedong and Yang, Jinwen},
  journal={arXiv preprint arXiv:2412.09734},
  year={2024}
}
```