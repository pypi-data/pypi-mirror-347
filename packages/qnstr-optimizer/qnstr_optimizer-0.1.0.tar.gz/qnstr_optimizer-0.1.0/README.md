# QNSTR-Optimizer

**QNSTR-Optimizer** is a Python implementation of the algorithm proposed in  
[A Quasi-Newton Subspace Trust Region Algorithm for Nonmonotone Variational Inequalities in Adversarial Learning over Box Constraints](https://arxiv.org/abs/2302.05935).

This package provides a robust and efficient optimizer for solving nonmonotone variational inequality (VI) problems, particularly those arising in adversarial learning and min-max optimization under box constraints. The algorithm leverages a quasi-Newton subspace trust region (QNSTR) approach, offering improved convergence properties for challenging saddle-point and VI problems.

---

## Features

- **Quasi-Newton Subspace Trust Region (QNSTR) Algorithm**: Efficiently solves nonmonotone VI problems with box constraints.
- **PyTorch Integration**: Easily integrates as a custom optimizer for PyTorch models.
- **Flexible Loss Function**: Supports user-defined loss functions for a wide range of applications.
- **Reproducible and Extensible**: Designed for research and practical use in adversarial learning and related fields.

---

## Installation

We recommend using [uv](https://github.com/astral-sh/uv) for dependency management:

```bash
uv sync
```

---

## Usage Example

Below is a minimal example demonstrating the use of `QnstrOptimizer` with a custom loss function in PyTorch:

```python
import torch
from qnstr_optimizer.optimizer import QnstrOptimizer

def loss_fn(x, y):
    return x**2 - 5 * x * y - y**2

x = torch.tensor([1.0], requires_grad=False)
y = torch.tensor([1.0], requires_grad=False)
params = [x, y]

optimizer = QnstrOptimizer(
    params,
    loss_fn,
    zeta1=0.1,
    zeta2=0.4,
    beta1=0.5,
    beta2=5,
    eta=0.5,
    nu=200,
    tau=0.9,
    epsilon=1e-6,
    epsilon_criteria=1e-4,
    memory_size=10,
    bfgs_dir_count=3,
    max_step=100,
    mu_s=1e-2,
)
optimizer.step()
assert abs(x.item()) < 0.1 and abs(y.item()) < 0.1
```

---

## Citation

If you use this code or algorithm in your research, please cite the following paper:

```
@article{Qiu_2024,
   title={A Quasi-Newton Subspace Trust Region Algorithm for Nonmonotone Variational Inequalities in Adversarial Learning over Box Constraints},
   volume={101},
   ISSN={1573-7691},
   url={http://dx.doi.org/10.1007/s10915-024-02679-y},
   DOI={10.1007/s10915-024-02679-y},
   number={2},
   journal={Journal of Scientific Computing},
   publisher={Springer Science and Business Media LLC},
   author={Qiu, Zicheng and Jiang, Jie and Chen, Xiaojun},
   year={2024},
   month=oct }
```

---

## References

- [A Quasi-Newton Subspace Trust Region Algorithm for Nonmonotone Variational Inequalities in Adversarial Learning over Box Constraints](https://arxiv.org/abs/2302.05935)

---

## License

This project is licensed under the MIT License.

