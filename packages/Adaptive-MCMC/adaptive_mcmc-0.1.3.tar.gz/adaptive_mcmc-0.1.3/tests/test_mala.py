import numpy as np
import pytest

from adaptive_mcmc.mala import ESJDMALA


class TestESJDMALA:
    def setup_method(self):
        """Set up common test fixtures."""
        # Standard normal distribution log pdf and gradient
        self.log_normal_pdf = lambda x: -0.5 * np.sum(x**2)
        self.grad_normal_pdf = lambda x: -x

        # Initial sample
        self.initial_sample = np.zeros(2)

        # Default sampler
        self.sampler = ESJDMALA(
            log_target_pdf=self.log_normal_pdf,
            grad_target_pdf=self.grad_normal_pdf,
            initial_sample=self.initial_sample,
            random_seed=42,
        )

    def test_initialization(self):
        """Test that the ESJDMALA initializes correctly with different parameters."""
        # Default initialization
        sampler = ESJDMALA(
            log_target_pdf=self.log_normal_pdf,
            grad_target_pdf=self.grad_normal_pdf,
            initial_sample=self.initial_sample,
        )

        assert sampler.eps == 0.1  # Default step size
        assert sampler.window == 100  # Default window
        assert sampler.steps == 0
        assert sampler.accepted == 0
        assert sampler.x.shape == (2,)
        assert sampler.dim == 2

        # Custom initialization
        custom_sampler = ESJDMALA(
            log_target_pdf=self.log_normal_pdf,
            grad_target_pdf=self.grad_normal_pdf,
            initial_sample=np.ones(3),
            eps0=0.2,
            window=50,
            eta=0.1,
            adapt_steps=1_000,
            eps_min=1e-5,
            eps_max=1.0,
            random_seed=12345,
        )

        assert custom_sampler.eps == 0.2
        assert custom_sampler.window == 50
        assert custom_sampler.eta == 0.1
        assert custom_sampler.adapt_steps == 1_000
        assert custom_sampler.eps_min == 1e-5
        assert custom_sampler.eps_max == 1.0
        assert custom_sampler.dim == 3
        assert custom_sampler.delta_buf.shape == (50,)

    def test_proposal(self):
        """Test the proposal function."""
        # For zero initial position in standard normal, we expect:
        # 1. The proposal to be normally distributed noise (since gradient is zero)
        # 2. The acceptance probability to be high

        # Fix the random state for reproducibility
        self.sampler.rng = np.random.default_rng(seed=42)

        x = np.zeros(2)
        y, alpha = self.sampler._proposal(x)

        # With zero gradient, proposal should be just noise scaled by eps
        assert y.shape == x.shape
        assert (
            alpha > 0.5
        )  # Acceptance probability should be high for symmetric proposal

        # For non-zero position, the gradient should push proposal towards origin
        x = np.array([1.0, 1.0])
        y, alpha = self.sampler._proposal(x)

        # Should be pushing towards the origin due to the gradient
        assert np.all(np.abs(y) < np.abs(x)) or alpha < 1.0

    def test_step(self):
        """Test the step function."""
        # Set a fixed random seed for reproducibility
        self.sampler.rng = np.random.default_rng(seed=42)

        # Initial state
        initial_x = self.sampler.x.copy()
        initial_steps = self.sampler.steps
        initial_accepted = self.sampler.accepted

        # Perform a step
        new_x, delta, eps = self.sampler.step()

        # Check return values
        assert new_x.shape == (2,)
        assert isinstance(delta, (int, float))
        assert delta >= 0  # ESJD should be non-negative
        assert eps == self.sampler.eps

        # Check state updates
        assert self.sampler.steps == initial_steps + 1
        assert self.sampler.delta_idx == (0 + 1) % self.sampler.window
        assert np.any(self.sampler.delta_buf != 0) or np.all(new_x == initial_x)

        # Check that accepted was updated if the move was accepted
        if not np.array_equal(new_x, initial_x):
            assert self.sampler.accepted == initial_accepted + 1

    def test_adaptation(self):
        """Test the adaptation of step size."""
        # Create sampler with smaller window for faster adaptation testing
        sampler = ESJDMALA(
            log_target_pdf=self.log_normal_pdf,
            grad_target_pdf=self.grad_normal_pdf,
            initial_sample=self.initial_sample,
            window=5,
            eps0=0.1,
            eta=0.2,
            random_seed=42,
        )

        initial_eps = sampler.eps

        # Run for exactly window steps to trigger adaptation
        for _ in range(5):
            sampler.step()

        # After window steps, adaptation should have happened once
        assert sampler.steps == 5
        assert sampler.eps != initial_eps

    def test_run(self):
        """Test the run function for generating samples."""
        n_samples = 20
        thin = 2

        samples, acc_rate, eps_traj, esjd_traj = self.sampler.run(n_samples, thin)

        # Check output shapes
        assert samples.shape == (n_samples, 2)
        assert eps_traj.shape == (n_samples,)
        assert esjd_traj.shape == (n_samples,)

        # Check acceptance rate is between 0 and 1
        assert 0 <= acc_rate <= 1

        # Check steps were taken
        assert self.sampler.steps == n_samples * thin

    def test_sampling_distribution(self):
        """Test that samples from standard normal have approximately correct statistics."""
        # This is a statistical test, so we use a larger number of samples
        sampler = ESJDMALA(
            log_target_pdf=self.log_normal_pdf,
            grad_target_pdf=self.grad_normal_pdf,
            initial_sample=np.array([5.0, 5.0]),  # Start far from mean
            random_seed=42,
        )

        # Run for enough steps to converge
        samples, _, _, _ = sampler.run(5_000, thin=1)

        # Discard burn-in
        post_burnin = samples[500:]

        # Check sample mean is close to zero (true mean of standard normal)
        sample_mean = np.mean(post_burnin, axis=0)
        assert np.all(
            np.abs(sample_mean) < 0.5
        ), f"Mean too far from zero: {sample_mean}"

        # Check sample variance is close to one (true variance of standard normal)
        sample_var = np.var(post_burnin, axis=0)
        assert np.all(
            np.abs(sample_var - 1) < 0.5
        ), f"Variance too far from one: {sample_var}"

    def test_fixed_step_size(self):
        """Test sampler with no adaptation (fixed step size)."""
        sampler = ESJDMALA(
            log_target_pdf=self.log_normal_pdf,
            grad_target_pdf=self.grad_normal_pdf,
            initial_sample=self.initial_sample,
            adapt_steps=0,  # No adaptation
            eps0=0.2,
            random_seed=42,
        )

        initial_eps = sampler.eps

        # Run sampler
        _, _, eps_traj, _ = sampler.run(100)

        # Step size should remain constant
        assert np.all(eps_traj == initial_eps)

    def test_thin_parameter(self):
        """Test that thinning works correctly."""
        n_samples = 10
        thin = 5

        # Record total steps before run
        steps_before = self.sampler.steps

        samples, _, _, _ = self.sampler.run(n_samples, thin)

        # Check correct number of steps were taken
        assert self.sampler.steps - steps_before == n_samples * thin
        assert samples.shape[0] == n_samples
