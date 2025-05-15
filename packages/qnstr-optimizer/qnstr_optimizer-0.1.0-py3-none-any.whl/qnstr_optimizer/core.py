import copy

import autograd.numpy as np
from autograd import elementwise_grad


class QNSTR:
    """
    Main class for the QNSTR algorithm

    Args:
        loss (callable): Objective function, e.g., f(x, y)
        domain (list): Variable constraint intervals, e.g., [[-2,2], [-2,2]]
    """

    def __init__(self, loss, domain):
        self.loss = loss
        self.domain = domain

    def get_dim(self, var):
        """
        Get the total number of elements in a tensor

        Args:
            var (np.ndarray): numpy array

        Returns:
            int: Number of elements
        """
        return np.prod(np.array(var.shape))

    def get_dim_list(self, t_vars):
        """
        Get the total number of elements in a list of tensors

        Args:
            t_vars (list): List of variables

        Returns:
            int: Total number of elements
        """
        return sum([self.get_dim(var) for var in t_vars])

    def vectorwise(self, x):
        """
        Flatten x with unknown number of elements and each element's length into a column vector

        Args:
            x (list): List of variables

        Returns:
            np.ndarray: Column vector
        """
        dim = self.get_dim(x[0])
        res = x[0].reshape([dim, 1], order="F")
        for i in range(len(x) - 1):
            dim = self.get_dim(x[i + 1])
            res = np.vstack((res, x[i + 1].reshape([dim, 1], order="F")))
        return res

    def new_F(self, x, domain):
        """
        Project variables x and gradients to obtain the transformed F(x).
        Used for subsequent least squares and trust region subproblems.

        Args:
            x (list): List of variables
            domain (list): Variable constraint intervals

        Returns:
            list: List of F(x)
        """
        F_value = []
        grad1 = elementwise_grad(self.loss, argnum=0)
        grad2 = elementwise_grad(self.loss, argnum=1)
        gradient = grad1(x[0], x[1])
        gradient = np.concatenate((gradient, -grad2(x[0], x[1])), 0)
        x = self.vectorwise(x)
        for i in range(len(x)):
            F_value.append(x[i] - np.clip(x[i] - gradient[i], domain[i][0], domain[i][1]))
        return F_value

    def new_f(self, x, mu_s, domain):
        """
        Smooth approximation of F(x) for subsequent least squares processing.

        Args:
            x (list): List of variables
            mu_s (float): Smoothing parameter
            domain (list): Variable constraint intervals

        Returns:
            list: Smoothed list of F(x)
        """
        F_x = self.new_F(x, domain)
        f_value = []
        grad1 = elementwise_grad(self.loss, argnum=0)
        grad2 = elementwise_grad(self.loss, argnum=1)
        gradient = grad1(x[0], x[1])
        gradient = np.concatenate((gradient, -grad2(x[0], x[1])), 0)
        x = self.vectorwise(x)
        for i in range(len(x)):
            condition1 = mu_s / 2 > np.abs(x[i] - gradient[i] - domain[i][1])
            operation1 = (
                0.5 * (gradient[i] + x[i])
                + 1 / (2 * mu_s) * np.square(gradient[i] - x[i] + domain[i][1])
                + mu_s / 8
                - domain[i][1] / 2
            )

            condition2 = mu_s / 2 > np.abs(x[i] - gradient[i] - domain[i][0])
            operation2 = (
                0.5 * (gradient[i] + x[i])
                - 1 / (2 * mu_s) * np.square(gradient[i] - x[i] + domain[i][0])
                - mu_s / 8
                - domain[i][0] / 2
            )
            f_value.append(np.where(condition1, operation1, np.where(condition2, operation2, F_x[i])))
        return f_value

    def least_square_smooth(self, x, mu_s, domain):
        """
        Least squares objective for smoothed F(x), returns 0.5*||F(x)||^2.

        Args:
            x (list): List of variables
            mu_s (float): Smoothing parameter
            domain (list): Variable constraint intervals

        Returns:
            float: Scalar
        """
        smooth_F = self.new_f(x, mu_s, domain)
        Vec_smooth_F = self.vectorwise(smooth_F)
        result = Vec_smooth_F.T @ Vec_smooth_F
        return 0.5 * result

    def grad1(self, x, mu_s, domain):
        """
        Compute the gradient of the smoothed least squares objective.

        Args:
            x (list): List of variables
            mu_s (float): Smoothing parameter
            domain (list): Variable constraint intervals

        Returns:
            np.ndarray: Gradient vector
        """
        grad = elementwise_grad(self.least_square_smooth)
        dx = grad(x, mu_s, domain)
        return dx

    def deal(self, *args):
        """
        Deep copy parameters (used to save historical points)

        Args:
            *args (any): Any parameters

        Returns:
            any: Deep copy of the first parameter
        """
        A1 = []
        for i in range(len(args)):
            a = copy.deepcopy(args[i])
            A1.append(a)
        return A1[0]

    def least_square(self, x, domain):
        """
        Unsmooth least squares objective, returns 0.5*||F(x)||^2.

        Args:
            x (list): List of variables
            domain (list): Variable constraint intervals

        Returns:
            float: Scalar
        """
        F1 = self.new_F(x, domain)
        Vec_F1 = self.vectorwise(F1)
        result = Vec_F1.T @ Vec_F1
        return 0.5 * result

    def update_Vk_g(self, Vk, gk):
        """
        Insert the current gradient gk into the historical gradient matrix Vk.

        Args:
            Vk (np.ndarray): Historical gradient matrix
            gk (np.ndarray): Current gradient

        Returns:
            np.ndarray: Updated Vk
        """
        dim, L = Vk.shape
        for i in range(L):
            Vk[:, L - i : L - i + 1] = Vk[:, L - i - 1 : L - i].reshape([dim, 1], order="F")
        Vk[:, 0:1] = -gk.reshape([dim, 1], order="F")
        return Vk

    def vector_matrix(self, a, b, c):
        """
        Vector-matrix transformation for quasi-Newton formula.

        Args:
            a (np.ndarray): Vector
            b (np.ndarray): Vector
            c (np.ndarray): Vector

        Returns:
            np.ndarray: Transformation result
        """
        dim = self.get_dim(a)
        op = (
            (a.reshape([1, dim], order="F") @ c.reshape([dim, 1], order="F"))
            / (a.reshape([1, dim], order="F") @ b.reshape([dim, 1], order="F"))
            * a.reshape([dim, 1], order="F")
        )
        return op

    def GN_BFGS(self, vk, Ak_sk, sk_vector, zk_vector, L):
        """
        Quasi-Newton (BFGS) direction update.

        Args:
            vk (np.ndarray): Current vector
            Ak_sk (np.ndarray): Historical information
            sk_vector (np.ndarray): Historical information
            zk_vector (np.ndarray): Historical information
            L (int): Step count

        Returns:
            np.ndarray: Update result
        """
        result = vk
        for i in range(L):
            result = (
                result
                - self.vector_matrix(Ak_sk[:, i], sk_vector[:, i], vk)
                + self.vector_matrix(zk_vector[:, i], sk_vector[:, i], vk)
            )
        return result

    def update_Gk(self, Vk):
        """
        Compute Gk = Vk^T Vk

        Args:
            Vk (np.ndarray): Historical gradient matrix

        Returns:
            np.ndarray: Gk
        """
        Gk = Vk.T @ Vk
        return Gk

    def update_ck(self, Vk, gk):
        """
        Compute ck = Vk^T gk

        Args:
            Vk (np.ndarray): Historical gradient matrix
            gk (np.ndarray): Current gradient

        Returns:
            np.ndarray: ck
        """
        ck = Vk.T @ gk
        return ck

    def update_Qk(
        self,
        x,
        Hk_vector,
        Vk,
        zk_sk_value,
        epsilon_criteria,
        rk_norm,
        L,
        mu_s,
        domain,
    ):
        """
        Second-order matrix Qk update for trust region subspace.

        Args:
            x (list): List of variables
            Hk_vector (np.ndarray): BFGS direction
            Vk (np.ndarray): Historical gradient matrix
            zk_sk_value (float): BFGS criterion
            epsilon_criteria (float): BFGS criterion threshold
            rk_norm (float): Residual norm
            L (int): Subspace dimension
            mu_s (float): Smoothing parameter
            domain (list): Variable constraint intervals

        Returns:
            np.ndarray: Qk
        """
        for i in range(L):
            if i == 0:
                Jk_vector = self.vectorwise(self.grad2(x, mu_s, domain, Vk[:, i : i + 1]))
            else:
                Jk_vector = np.concatenate(
                    (
                        Jk_vector,
                        self.vectorwise(self.grad2(x, mu_s, domain, Vk[:, i : i + 1])),
                    ),
                    1,
                )

        if zk_sk_value >= epsilon_criteria:
            Qk = Jk_vector.T @ Jk_vector + Hk_vector.T @ Vk
        else:
            Qk = Jk_vector.T @ Jk_vector + rk_norm * Vk.T @ Vk

        return Qk

    def QNSTR_subproblem_1d(self, Qk, ck, ls):
        """
        Step size solution in one-dimensional subspace.

        Args:
            Qk (np.ndarray): Second-order matrix
            ck (np.ndarray): Linear term
            ls (float): Step size

        Returns:
            np.ndarray: alpha
        """
        dim = Qk.shape[0]
        Q11 = Qk[0, 0]
        if Q11 > 0:
            alpha = -ck[0, 0] / Q11 * ls
            # dq_value = -alpha * Q11 * alpha - alpha * ck[0, 0]
        else:
            alpha = 0.1 * ls
            # dq_value = alpha * ck[0, 0]
        alpha = np.vstack((alpha, np.zeros((dim - 1, 1))))
        return alpha

    def update_parameter(self, x, alpha, Vk):
        """
        Update variable x with step size alpha and direction Vk.

        Args:
            x (list): List of variables
            alpha (np.ndarray): Step size
            Vk (np.ndarray): Direction

        Returns:
            list: Updated x
        """
        pk = Vk @ alpha
        dim1 = 0
        for i in range(len(x)):
            dim = self.get_dim(x[i])
            pk_ = pk[dim1 : dim1 + dim, 0].reshape(x[i].shape, order="F")
            x[i] = x[i] + pk_
            dim1 = dim1 + dim

        return x

    def Quadratic(self, alpha, ck, Qk):
        """
        Quadratic objective function.

        Args:
            alpha (np.ndarray):
            ck (np.ndarray):
            Qk (np.ndarray):

        Returns:
            float: Scalar
        """
        return alpha.T @ ck + 0.5 * alpha.T @ Qk @ alpha

    def inverse(self, Qk, ck):
        """
        Solve the linear system Qk x = ck

        Args:
            Qk (np.ndarray):
            ck (np.ndarray):

        Returns:
            np.ndarray: Solution
        """
        L = np.linalg.cholesky(Qk)
        y = np.linalg.solve(L, ck)
        zin_kj = np.linalg.solve(L.T, y)
        return zin_kj

    def method(self, Qk, Gk, ck, Delta_k, epsilon):
        """
        Bisection method for trust region subproblem

        Args:
            Qk (np.ndarray):
            Gk (np.ndarray):
            ck (np.ndarray):
            Delta_k (float):
            epsilon (float):

        Returns:
            np.ndarray: alpha_k
        """
        lambda_l = 0
        lambda_u = 1
        for i in range(1000):
            lambda_k = (lambda_u + lambda_l) / 2
            try:
                alpha_k = -self.inverse(Qk + lambda_k * Gk, ck)
            except:  # noqa: E722
                alpha_k = -np.linalg.pinv(Qk + lambda_k * Gk) @ ck

            if (alpha_k.T @ Gk @ alpha_k) ** (1 / 2) < Delta_k - epsilon:
                lambda_u = lambda_k

            elif (alpha_k.T @ Gk @ alpha_k) ** (1 / 2) > Delta_k + epsilon:
                lambda_l = lambda_k
                lambda_u = 2 * lambda_u
            else:
                break
        return alpha_k

    def solver(self, Qk, Gk, ck, Delta_k, L, epsilon):
        """
        Trust region subproblem solver

        Args:
            Qk (np.ndarray):
            Gk (np.ndarray):
            ck (np.ndarray):
            Delta_k (float):
            L (int):
            epsilon (float):

        Returns:
            np.ndarray: alpha_k
        """
        try:
            alpha_k = -self.inverse(Qk, ck)
        except:  # noqa: E722
            alpha_k = -np.linalg.pinv(Qk) @ ck
        if alpha_k.T @ Gk @ alpha_k <= Delta_k**2:
            return alpha_k
        else:
            alpha_k = self.method(Qk, Gk, ck, Delta_k, epsilon)
            return alpha_k

    def QNSTR_subproblem_Delta(self, Qk, Gk, ck, Delta, L, L1, epsilon):
        """
        Trust region subproblem solution in multi-dimensional subspace.

        Args:
            Qk (np.ndarray):
            Gk (np.ndarray):
            ck (np.ndarray):
            Delta (float):
            L (int):
            L1 (int):
            epsilon (float):

        Returns:
            np.ndarray: alpha_k
        """
        Qk_ = Qk[0:L, 0:L]
        Gk_ = Gk[0:L, 0:L]
        ck_ = ck[0:L, 0:1]

        alpha_k = self.solver(Qk_, Gk_, ck_, Delta, L, epsilon)

        if alpha_k.shape[0] < L1:
            a = L1 - alpha_k.shape[0]
            alpha_k = np.vstack((alpha_k, np.zeros([a, 1])))
        return alpha_k

    def vectorwise_(self, x, mu_s, domain):
        """
        Vectorize F(x) (smoothed version)

        Args:
            x (list): List of variables
            mu_s (float): Smoothing parameter
            domain (list): Variable constraint intervals

        Returns:
            np.ndarray: Column vector
        """
        res = self.vectorwise(self.new_f(x, mu_s, domain))
        return res

    def vector_vector(self, x, mu_s, domain, y1):
        """
        Compute the dot product of F(x) and y

        Args:
            x (list): List of variables
            mu_s (float): Smoothing parameter
            domain (list): Variable constraint intervals
            y1 (np.ndarray): Vector

        Returns:
            float: Scalar
        """
        a = self.vectorwise_(x, mu_s, domain)
        return a.T @ y1

    def grad2(self, x, mu_s, domain, y1):
        """
        Compute the gradient of F(x) @ y1 (for quasi-Newton update)

        Args:
            x (list): List of variables
            mu_s (float): Smoothing parameter
            domain (list): Variable constraint intervals
            y1 (np.ndarray): Vector

        Returns:
            np.ndarray: Gradient
        """
        grad = elementwise_grad(self.vector_vector)
        Jk_v = grad(x, mu_s, domain, y1)
        return Jk_v

    def update_vk(self, x, xk, Fk, rk_norm, rk_norm_, mu_s):
        """
        Update for quasi-Newton direction

        Args:
            x (list): Current variables
            xk (list): Historical variables
            Fk (np.ndarray): F(x)
            rk_norm (float): Current residual norm
            rk_norm_ (float): Historical residual norm
            mu_s (float): Smoothing parameter

        Returns:
            np.ndarray: vk
        """
        Jk_gk = self.grad2(x, mu_s, self.domain, Fk)
        Jk1_gk = self.grad2(xk, mu_s, self.domain, Fk)

        Jk_gk_vector = self.vectorwise(Jk_gk)
        Jk1_gk_vector = self.vectorwise(Jk1_gk)
        return (Jk_gk_vector - Jk1_gk_vector) * rk_norm / rk_norm_

    def update_vector(self, x, v, L):
        """
        Insert historical vector

        Args:
            x (np.ndarray): Historical vector matrix
            v (np.ndarray): New vector
            L (int): Insert position

        Returns:
            np.ndarray: Updated matrix
        """
        dim = self.get_dim(v)
        x[:, L : L + 1] = v.reshape([dim, 1], order="F")
        return x

    def run(
        self,
        x,
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
        """
        Main QNSTR process: Trust region quasi-Newton method for solving saddle point/VI problems

        Args:
            x (list): Initial point (list of variables)
            zeta1, zeta2, beta1, beta2, eta, nu, tau, epsilon, epsilon_criteria (float): Hyperparameters
            memory_size (int): Subspace dimension (original L)
            bfgs_dir_count (int): Number of BFGS directions (original L1)
            max_step (int): Maximum number of iterations
            mu_s (float): Smoothing parameter

        Returns:
            tuple: (final point x, optimization trajectory)
        """
        trust_region_radius = 1.0
        trajectory = []
        loss = self.least_square_smooth(x, mu_s, self.domain)
        iter_count = 0
        while iter_count < max_step:
            # 1. Check for convergence (objective function and gradient norm)
            grad = self.grad1(x, mu_s, self.domain)
            grad_vec = self.vectorwise(grad)
            grad_norm = np.linalg.norm(grad_vec)  # Euclidean norm of grad_vec
            trajectory.append(self._extract_point(x))
            if self._is_converged(loss, grad_norm, epsilon):
                break
            # 2. Trust region subspace inner loop
            x, trust_region_radius, mu_s, inner_steps = self._trust_region_inner_loop(
                x,
                trust_region_radius,
                mu_s,
                memory_size,
                bfgs_dir_count,
                max_step,
                iter_count,
                zeta1,
                zeta2,
                beta1,
                beta2,
                eta,
                nu,
                tau,
                epsilon,
                epsilon_criteria,
            )
            iter_count += inner_steps if inner_steps > 0 else 1
        return x, trajectory

    def _is_converged(self, loss, grad_norm, tol):
        """
        Check for convergence

        Args:
            loss (float): Current loss
            grad_norm (float): Gradient norm
            tol (float): Tolerance

        Returns:
            bool: Whether converged
        """
        return (2 * loss) ** 0.5 < tol or grad_norm <= tol

    def _extract_point(self, x):
        """
        Extract current point for trajectory recording

        Args:
            x (list): Current variables

        Returns:
            tuple: Current point
        """
        return tuple(xi.flatten()[0] for xi in x)

    def _trust_region_inner_loop(
        self,
        x,
        trust_region_radius,
        mu_s,
        memory_size,
        bfgs_dir_count,
        max_step,
        iter_count,
        zeta1,
        zeta2,
        beta1,
        beta2,
        eta,
        nu,
        tau,
        epsilon,
        epsilon_criteria,
    ):
        """
        Trust region subspace inner loop, returns updated x, trust region radius, mu_s, and actual steps

        Args:
            x (list): Current variables
            trust_region_radius (float): Trust region radius
            mu_s (float): Smoothing parameter
            memory_size (int): Subspace dimension
            bfgs_dir_count (int): Number of BFGS directions
            max_step (int): Maximum number of iterations
            iter_count (int): Current iteration count
            zeta1, zeta2, beta1, beta2, eta, nu, tau, epsilon, epsilon_criteria (float): Hyperparameters

        Returns:
            tuple: (x, trust_region_radius, mu_s, inner_iter)
        """
        dim = self.get_dim_list(x)
        inner_iter = 0
        line_search_step = 1.0
        zk_sk_value = 0.0
        # Initialize historical information
        Vk = np.zeros([dim, bfgs_dir_count])
        sk_vector = np.ones([dim, memory_size])
        Ak_sk = np.ones([dim, memory_size])
        zk_vector = np.ones([dim, memory_size])
        while inner_iter < memory_size and iter_count + inner_iter < max_step:
            old_loss = self.least_square(x, self.domain)
            grad = self.grad1(x, mu_s, self.domain)
            grad_vec = self.vectorwise(grad)
            grad_norm = np.linalg.norm(grad_vec)
            if self._is_converged(old_loss, grad_norm, epsilon):
                break
            Vk = self.update_Vk_g(Vk, grad_vec)
            x_prev = self.deal(x)
            # Compute BFGS direction
            for ii in range(bfgs_dir_count):
                if ii == 0:
                    Hk_vector = self.GN_BFGS(Vk[:, ii : ii + 1], Ak_sk, sk_vector, zk_vector, inner_iter)
                else:
                    Hk_vector = np.concatenate(
                        (
                            Hk_vector,
                            self.GN_BFGS(
                                Vk[:, ii : ii + 1],
                                Ak_sk,
                                sk_vector,
                                zk_vector,
                                inner_iter,
                            ),
                        ),
                        1,
                    )
            new_loss = self.least_square_smooth(x, mu_s, self.domain)
            ck = self.update_ck(Vk, grad_vec)
            Qk = self.update_Qk(
                x,
                Hk_vector,
                Vk,
                zk_sk_value,
                epsilon_criteria,
                (2 * new_loss) ** 0.5,
                bfgs_dir_count,
                mu_s,
                self.domain,
            )
            Gk = self.update_Gk(Vk)
            # Step size and trust region adjustment
            for k in range(1, memory_size):
                if np.sum(Vk[:, k : k + 1] ** 2) == 0:
                    if k == 1:
                        for _ in range(500):
                            alpha = self.QNSTR_subproblem_1d(Qk, ck, line_search_step)
                            x = self.update_parameter(x, alpha, Vk)
                            new_loss = self.least_square_smooth(x, mu_s, self.domain)
                            mka = -self.Quadratic(alpha, ck, Qk)
                            rho_k = (old_loss - new_loss) / mka
                            x = self.deal(x_prev)
                            if (
                                rho_k > eta and old_loss > new_loss
                            ):  # Indicates new x performs well, reassign new x to x variable
                                x = self.update_parameter(x, alpha, Vk)
                                line_search_step = 1.0
                                trust_region_radius = 1.0
                                rho_k = 0
                                break
                            else:
                                line_search_step *= 0.5
                        break
                    else:
                        for _ in range(500):
                            alpha = self.QNSTR_subproblem_Delta(
                                Qk, Gk, ck, trust_region_radius, k, bfgs_dir_count, 1e-8
                            )
                            x = self.update_parameter(x, alpha, Vk)
                            new_loss = self.least_square_smooth(x, mu_s, self.domain)
                            mka = -self.Quadratic(alpha, ck, Qk)
                            rho_k = (old_loss - new_loss) / mka
                            x = self.deal(x_prev)
                            if rho_k < zeta1 or old_loss < new_loss:
                                trust_region_radius = beta1 * trust_region_radius
                            elif rho_k > zeta2 and (alpha.T @ Gk @ alpha) ** 0.5 >= trust_region_radius - 1e-8:
                                trust_region_radius = min(10000, beta2 * trust_region_radius)
                            if old_loss - new_loss == 0 and trust_region_radius <= 1e-10:
                                Vk = np.zeros([dim, memory_size])
                                zk_sk_value = 0
                                inner_iter = 0
                                break
                            if rho_k > eta and old_loss - new_loss > 0:
                                x = self.update_parameter(x, alpha, Vk)
                                break
                        break
            # Check if variables have changed, update historical information
            dk = self.vectorwise(x) - self.vectorwise(x_prev)
            norm_dk = np.linalg.norm(dk)
            if norm_dk == 0:
                break
            else:
                Fk = self.vectorwise_(x, mu_s, self.domain)
                vk = self.update_vk(x, x_prev, Fk, old_loss**0.5, new_loss**0.5, mu_s)
                zk_sk_value = vk.T @ dk / (dk.T @ dk)
                if zk_sk_value >= epsilon_criteria:
                    BFGS_sk = self.GN_BFGS(dk, Ak_sk, sk_vector, zk_vector, inner_iter)
                    sk_vector = self.update_vector(sk_vector, dk, inner_iter)
                    Ak_sk = self.update_vector(Ak_sk, BFGS_sk, inner_iter)
                    zk_vector = self.update_vector(zk_vector, vk, inner_iter)
                    inner_iter += 1
                grad = self.grad1(x, mu_s, self.domain)
                grad_vec = self.vectorwise(grad)
                if np.linalg.norm(grad_vec) <= nu * mu_s:
                    mu_s = tau * mu_s
        return x, trust_region_radius, mu_s, inner_iter


if __name__ == "__main__":
    demo = QNSTR(
        loss=lambda x, y: x**2 - 5 * x * y - y**2,
        domain=[[-2.0, 2.0], [-2.0, 2.0]],
    )
    x_, rk_list_ = demo.run(
        x=[np.array([[1.0]]), np.array([[1.0]])],
        zeta1=0.1,
        zeta2=0.4,
        beta1=0.5,
        beta2=5,
        eta=0.5,
        nu=200,
        tau=0.9,
        epsilon=1e-8,
        epsilon_criteria=1e-4,
        memory_size=30,
        bfgs_dir_count=5,
        max_step=1000,
        mu_s=1e-2,
    )
    print(x_, rk_list_)
