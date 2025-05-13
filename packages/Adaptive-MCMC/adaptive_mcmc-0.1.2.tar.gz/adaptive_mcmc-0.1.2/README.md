# Adaptive-MCMC

Adaptive Markov Chain Monte Carlo (MCMC) algorithms

## Install

```{bash}
pip install adaptive-mcmc
```

## Examples

```{python}
import numpy as np
from adaptive_mcmc.mala import ESJDMALA
from scipy.stats import multivariate_normal

dim = 20
cov = 0.5 * np.eye(dim) + 0.5
inv_cov = np.linalg.inv(cov)


def logp(x):
    return multivariate_normal.logpdf(x, mean=np.zeros(dim), cov=cov)


def grad_logp(x):
    return -inv_cov @ x


mala = ESJDMALA(logp, grad_logp, initial_sample=np.zeros(dim), eps0=0.5)
samples, acc, eps_hist, esjd_hist = mala.run(20_000)
print(f"Acceptance: {acc:.3f}, Final epsilon = {eps_hist[-1]:.4f}")

pmala = PrecondESJDMALA(logp, grad_logp, initial_sample=np.zeros(dim), initial_covariance=np.eye(dim), eps0=0.5)
samples, acc, eps_hist, esjd_hist = pmala.run(20_000)
print(f"Acceptance: {acc:.3f}, Final epsilon = {eps_hist[-1]:.4f}")
```
