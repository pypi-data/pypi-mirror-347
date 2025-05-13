from abc import ABC, abstractmethod
from typing import Callable, Iterable, Optional, Tuple

import numpy as np
from numpy import typing as npt
from tqdm.auto import trange


class MALAInterface(ABC):
    """
    Interface for MALA samplers.
    """

    @abstractmethod
    def step(self) -> Tuple[npt.NDArray[np.floating], float, float]:
        """
        Performs a single step of the MALA algorithm.

        Returns:
            Tuple[npt.NDArray[np.floating], float, float]: New sample point, ESJD value, and current step size.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def run(self, n_samples: int, thin: int = 1) -> Tuple[
        npt.NDArray[np.floating],
        float,
        npt.NDArray[np.floating],
        npt.NDArray[np.floating],
    ]:
        """
        Runs the MALA sampler for a specified number of samples.

        Args:
            n_samples (int): Number of samples to generate.
            thin (int): Thinning interval.

        Returns:
            Tuple[npt.NDArray[np.floating], float, npt.NDArray[np.floating], npt.NDArray[np.floating]]: Generated samples, acceptance rate, ESJD trajectory, and step size trajectory.
        """
        raise NotImplementedError("Subclasses should implement this method.")


class ESJDMALA(MALAInterface):
    """
    ESJD-maximizing adaptive MALA sampler.
    """

    def __init__(
        self,
        log_target_pdf: Callable[
            [Iterable[float] | npt.NDArray[np.floating]], float | np.floating
        ],
        grad_target_pdf: Callable[
            [Iterable[float] | npt.NDArray[np.floating]],
            Iterable[float] | npt.NDArray[np.floating],
        ],
        initial_sample: npt.NDArray[np.floating],
        eps0: float = 0.1,
        window: int = 100,
        eta: float = 0.05,
        adapt_steps: int = 5_000,
        eps_min: float = 1e-4,
        eps_max: float = 2.0,
        random_seed: int = 42,
    ) -> None:
        """
        Initializes the ESJDMALA sampler.
        This class implements the ESJD-maximizing adaptive MALA algorithm.

        Args:
            log_target_pdf (Callable[Iterable[float] | npt.NDArray[np.floating], float | np.floating]): Log target probability density function.
            grad_target_pdf (Callable[Iterable[float] | npt.NDArray[np.floating], Iterable[float] | npt.NDArray[np.floating]]): Gradient of the log target probability density function.
            initial_sample (npt.NDArray[np.floating]): Initial sample point.
            eps0 (float): Initial step size. Default is 0.1.
            window (int): Window size for adaptive step size. Default is 100.
            eta (float): Learning rate for adaptive step size. Default is 0.05.
            adapt_steps (int): Number of adaptation steps. Default is 5,000.
            eps_min (float): Minimum step size. Default is 1e-4.
            eps_max (float): Maximum step size. Default is 2.0.
            random_seed (int): Random seed for reproducibility. Default is 42.
        """
        self.logp = log_target_pdf
        self.grad_logp = grad_target_pdf
        self.x = initial_sample.astype(float).copy()
        self.dim = initial_sample.size
        self.eps = eps0
        self.window = window
        self.eta = eta
        self.adapt_steps = adapt_steps
        self.eps_min = eps_min
        self.eps_max = eps_max
        self.rng = np.random.default_rng(seed=random_seed)

        # bookkeeping
        self.delta_buf = np.zeros(window)
        self.delta_idx = 0
        self.esjd_prev = 0.0
        self.accepted = 0
        self.steps = 0

    def _proposal(
        self, x: npt.NDArray[np.floating]
    ) -> Tuple[npt.NDArray[np.floating], float]:
        """
        Proposes a new sample point using the MALA proposal distribution.

        Args:
            x (npt.NDArray[np.floating]): Current sample point.

        Returns:
            Tuple[npt.NDArray[np.floating], float]: Proposed sample point and acceptance probability.
        """
        g = self.grad_logp(x)
        noise = self.rng.normal(size=self.dim)
        y = x + 0.5 * self.eps**2 * g + self.eps * noise

        # log-proposal densities (forward & reverse)
        def log_q(a, b):
            mu = a + 0.5 * self.eps**2 * self.grad_logp(a)
            return -0.5 / (self.eps**2) * np.linalg.norm(b - mu) ** 2

        log_alpha = self.logp(y) - self.logp(x) + log_q(y, x) - log_q(x, y)

        return y, min(1.0, np.exp(log_alpha))

    def step(self) -> Tuple[npt.NDArray[np.floating], float, float]:
        """
        Performs a single step of the MALA algorithm.

        Returns:
            Tuple[npt.NDArray[np.floating], float, float]: New sample point, ESJD value, and current step size.
        """
        y, alpha = self._proposal(self.x)
        if self.rng.uniform() < alpha:
            x_new = y
            self.accepted += 1
        else:
            x_new = self.x

        delta = np.sum((x_new - self.x) ** 2)
        self.x = x_new

        # store ESJD value
        self.delta_buf[self.delta_idx] = delta
        self.delta_idx = (self.delta_idx + 1) % self.window

        self.steps += 1
        if self.steps % self.window == 0 and self.steps <= self.adapt_steps:
            esjd_new = self.delta_buf.mean()
            if esjd_new > self.esjd_prev:
                self.eps = min(self.eps * (1 + self.eta), self.eps_max)
            else:
                self.eps = max(self.eps * (1 - self.eta), self.eps_min)
            self.esjd_prev = esjd_new

        return self.x, delta, self.eps

    def run(self, n_samples: int, thin: int = 1, verbose: bool = True) -> Tuple[
        npt.NDArray[np.floating],
        float,
        npt.NDArray[np.floating],
        npt.NDArray[np.floating],
    ]:
        """
        Runs the MALA sampler for a specified number of samples.

        Args:
            n_samples (int): Number of samples to generate.
            thin (int): Thinning interval. Default is 1.
            verbose (bool): Whether to show progress bar. Default is True.

        Returns:
            Tuple[npt.NDArray[np.floating], float, npt.NDArray[np.floating], npt.NDArray[np.floating]]: Generated samples, acceptance rate, ESJD trajectory, and step size trajectory.
        """
        samples = np.empty((n_samples, self.dim))
        eps_traj = np.empty(n_samples)
        esjd_traj = np.empty(n_samples)
        for i in trange(n_samples, disable=not verbose):
            for _ in range(thin):
                x, delta, eps_now = self.step()
            samples[i] = x
            eps_traj[i] = eps_now
            esjd_traj[i] = delta
        acc_rate = self.accepted / (n_samples * thin)

        return samples, acc_rate, eps_traj, esjd_traj


class PrecondESJDMALA(ESJDMALA):
    def __init__(
        self,
        log_target_pdf: Callable[
            [Iterable[float] | npt.NDArray[np.floating]], float | np.floating
        ],
        grad_target_pdf: Callable[
            [Iterable[float] | npt.NDArray[np.floating]],
            Iterable[float] | npt.NDArray[np.floating],
        ],
        initial_sample: npt.NDArray[np.floating],
        initial_covariance: Optional[npt.NDArray[np.floating]] = None,
        eps0: float = 0.1,
        window: int = 100,
        eta: float = 0.05,
        adapt_steps: int = 5_000,
        eps_min: float = 1e-4,
        eps_max: float = 2.0,
        random_seed: int = 42,
    ) -> None:
        """
        Initializes the PrecondESJDMALA sampler.
        This class implements the ESJD-maximizing adaptive MALA algorithm with preconditioning.
        The preconditioner is defined by the initial covariance matrix.

        Args:
            log_target_pdf (Callable[ [Iterable[float]  |  npt.NDArray[np.floating]], float  |  np.floating ]): Log target probability density function.
            grad_target_pdf (Callable[ [Iterable[float]  |  npt.NDArray[np.floating]], Iterable[float]  |  npt.NDArray[np.floating], ]): Gradient of the log target probability density function.
            initial_sample (npt.NDArray[np.floating]): Initial sample point.
            initial_covariance (Optional[npt.NDArray[np.floating]], optional): Initial covariance matrix. Defaults to None.
            eps0 (float, optional): Initial step size. Defaults to 0.1.
            window (int, optional): Window size for adaptive step size. Defaults to 100.
            eta (float, optional): Step size adaptation rate. Defaults to 0.05.
            adapt_steps (int, optional): Number of adaptation steps. Defaults to 5_000.
            eps_min (float, optional): Minimum step size. Defaults to 1e-4.
            eps_max (float, optional): Maximum step size. Defaults to 2.0.
            random_seed (int, optional): Random seed for reproducibility. Defaults to 42.
        """
        super().__init__(
            log_target_pdf=log_target_pdf,
            grad_target_pdf=grad_target_pdf,
            initial_sample=initial_sample,
            eps0=eps0,
            window=window,
            eta=eta,
            adapt_steps=adapt_steps,
            eps_min=eps_min,
            eps_max=eps_max,
            random_seed=random_seed,
        )
        self.initial_covariance = (
            np.eye(self.dim)
            if initial_covariance is None
            else np.asarray(initial_covariance)
        )
        self.L = np.linalg.cholesky(self.initial_covariance)
        self.initial_covariance_inv = np.linalg.inv(self.initial_covariance)

    def _proposal(
        self, x: npt.NDArray[np.floating]
    ) -> Tuple[npt.NDArray[np.floating], float]:
        """
        Proposes a new sample point using the MALA proposal distribution with preconditioning.

        Args:
            x (npt.NDArray[np.floating]): Current sample point.

        Returns:
            Tuple[npt.NDArray[np.floating], float]: Proposed sample point and acceptance probability.
        """
        g = self.grad_logp(x)
        mu_x = x + 0.5 * self.eps**2 * self.initial_covariance @ g
        noise = self.rng.normal(size=self.dim)
        y = mu_x + self.eps * self.L @ noise

        def log_q(a, b, grad_a):
            mu = a + 0.5 * self.eps**2 * self.initial_covariance @ grad_a
            diff = b - mu
            return -0.5 / self.eps**2 * diff.T @ self.initial_covariance_inv @ diff

        log_alpha = (
            self.logp(y)
            - self.logp(x)
            + log_q(y, x, self.grad_logp(y))
            - log_q(x, y, g)
        )
        return y, min(1.0, np.exp(log_alpha))
