# eventimpact/analyzer.py

import numpy as np
from scipy.stats import invgamma

class EventImpactAnalyzer:
    """
    Bayesian impact analysis for a bounded event (e.g. promotion, campaign, feature launch, competitor).

    The model uses a conjugate Bayesian linear regression with four predictors:
      1. Intercept
      2. Linear time trend
      3. Event indicator (1 during event, 0 otherwise)
      4. Event elapsed time   (time - event_start, during event; 0 outside)

    Parameters
    ----------
    time : array-like, shape (n_samples,)
        Monotonic numeric time stamps (e.g., [0,1,2,…] or ordinal dates).
    values : array-like, shape (n_samples,)
        Observed metric (e.g. sales, web traffic).
    event_start : float
        Inclusive start time of the event window.
    event_end : float
        Exclusive end time of the event window.
    """

    def __init__(self, time, values, event_start, event_end):
        # Convert inputs to numpy arrays
        self.time = np.asarray(time, dtype=float)
        self.values = np.asarray(values, dtype=float)
        self.event_start = float(event_start)
        self.event_end   = float(event_end)
        self._fitted = False
        self._post   = {}

    def fit(self,
            tau: float = 10.0,
            a0:  float = 1.0,
            b0:  float = 1.0,
            num_samples: int = 5000,
            seed: int = None):
        """
        Fit the Bayesian regression model via conjugate updates.

        Hyperparameters:
        ------------
        tau : float
            Prior standard deviation for each regression coefficient β ~ N(0, τ²).
        a0 : float
            Shape parameter of Inv-Gamma prior on σ².
        b0 : float
            Scale parameter of Inv-Gamma prior on σ².
        num_samples : int
            Number of posterior draws for β and σ².
        seed : int or None
            Random seed for reproducibility.
        """
        if seed is not None:
            np.random.seed(seed)

        n = len(self.time)
        # 1. Build design matrix
        indicator = ((self.time >= self.event_start) & (self.time < self.event_end)).astype(int)
        duration  = np.where(indicator==1, self.time - self.event_start, 0.0)

        X = np.column_stack([
            np.ones(n),        # intercept
            self.time,         # linear trend
            indicator,         # immediate jump
            duration           # slope during event
        ])
        p = X.shape[1]

        # 2. Conjugate posterior analytic forms
        XtX = X.T @ X
        Vn  = np.linalg.inv(XtX + np.eye(p)/(tau**2))        # scaled precision
        beta_n = Vn @ (X.T @ self.values)                    # posterior mean for β

        a_n = a0 + n/2
        resid_term = (
            self.values @ self.values
            - beta_n @ (XtX + np.eye(p)/(tau**2)) @ beta_n
        )
        b_n = b0 + 0.5 * resid_term

        # 3. Draw posterior samples
        betas = np.zeros((num_samples, p))
        sig2  = np.zeros(num_samples)
        for i in range(num_samples):
            s2 = invgamma.rvs(a=a_n, scale=b_n)
            sig2[i] = s2
            betas[i] = np.random.multivariate_normal(beta_n, s2 * Vn)

        # 4. Store posterior
        self._post = {
            "beta_samples": betas,
            "sigma2_samples": sig2,
            "beta_mean": beta_n,
            "Vn": Vn,
            "a_n": a_n,
            "b_n": b_n
        }
        self._fitted = True

    def summary(self, cred_mass: float = 0.95) -> dict:
        """
        Summarize the two event-related effects:

        - 'immediate': jump at event start
        - 'slope':     additional slope DURING the event

        Returns
        -------
        summary : dict
            {
              'immediate': { 'mean': float,
                             'ci': (low, high),
                             'p_positive': float },
              'slope':     { 'mean': float,
                             'ci': (low, high),
                             'p_positive': float }
            }
        """
        if not self._fitted:
            raise RuntimeError("Model must be fitted via .fit() before summary().")

        draws = self._post["beta_samples"]
        results = {}
        for name, idx in [("immediate", 2), ("slope", 3)]:
            vals = draws[:, idx]
            mean = vals.mean()
            lower, upper = np.percentile(
                vals,
                [ (1 - cred_mass)/2 * 100, (1 + cred_mass)/2 * 100 ]
            )
            p_pos = float((vals > 0).mean())
            results[name] = {
                "mean": mean,
                "ci": (lower, upper),
                "p_positive": p_pos
            }
        return results
