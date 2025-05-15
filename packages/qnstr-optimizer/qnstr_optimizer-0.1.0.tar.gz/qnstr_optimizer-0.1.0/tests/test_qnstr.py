import torch
from autograd import numpy as np

from qnstr_optimizer.core import QNSTR
from qnstr_optimizer.optimizer import QnstrOptimizer


def test_qnstr_demo_convergence():
    demo = QNSTR(
        loss=lambda x, y: x**2 - 5 * x * y - y**2,
        domain=[[-2.0, 2.0], [-2.0, 2.0]],
    )
    x_final, trace = demo.run(
        x=[np.array([[1.0]]), np.array([[1.0]])],
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
    assert len(trace) >= 2
    x_val, y_val = x_final[0].item(), x_final[1].item()
    assert abs(x_val) < 0.1 and abs(y_val) < 0.1


def test_qnstr_torch_optimizer():
    def loss_fn(x, y):
        return x**2 - 5 * x * y - y**2

    x = torch.tensor([1.0], requires_grad=False)
    y = torch.tensor([1.0], requires_grad=False)
    params = [x, y]
    optimizer = QnstrOptimizer(
        params,
        loss_fn,
        **dict(
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
        ),
    )
    optimizer.step()
    assert abs(x.item()) < 0.1 and abs(y.item()) < 0.1
