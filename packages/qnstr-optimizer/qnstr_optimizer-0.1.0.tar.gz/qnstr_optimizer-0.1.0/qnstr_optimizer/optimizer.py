# import numpy as np
import autograd.numpy as np
import torch
from torch.optim import Optimizer

from qnstr_optimizer.core import QNSTR


class QnstrOptimizer(Optimizer):
    def __init__(
        self,
        params,
        loss_fn,
        /,
        zeta1,
        zeta2,
        beta1,
        beta2,
        eta,
        nu,
        tau,
        epsilon,
        epsilon_criteria,
        memory_size,
        bfgs_dir_count,
        max_step,
        mu_s,
    ):
        defaults = dict(
            zeta1=zeta1,
            zeta2=zeta2,
            beta1=beta1,
            beta2=beta2,
            eta=eta,
            nu=nu,
            tau=tau,
            epsilon=epsilon,
            epsilon_criteria=epsilon_criteria,
            memory_size=memory_size,
            bfgs_dir_count=bfgs_dir_count,
            max_step=max_step,
            mu_s=mu_s,
        )
        super().__init__(params, defaults)
        self.loss_fn = loss_fn
        self.qnstr = QNSTR(loss=self.loss_fn, domain=[[-100, 100], [-100, 100]])

    @torch.no_grad()
    def step(self, closure=None):
        # Only supports 2 parameters (x, y)
        params = list(self.param_groups[0]["params"])
        assert len(params) == 2, "QnstrOptimizer only supports 2 parameters (x, y)"
        x, y = params
        # Convert to numpy
        x_np = x.detach().cpu().numpy().reshape(1, 1)
        y_np = y.detach().cpu().numpy().reshape(1, 1)
        # Call QNSTR algorithm to run one step
        x_final, _ = self.qnstr.run(x=[np.array(x_np), np.array(y_np)], **self.defaults)
        # Update torch parameters
        x.copy_(torch.tensor(x_final[0], dtype=x.dtype, device=x.device).reshape(-1))
        y.copy_(torch.tensor(x_final[1], dtype=y.dtype, device=y.device).reshape(-1))

    def zero_grad(self):
        # QNSTR does not require gradients, but provide an empty implementation for interface compatibility
        pass
