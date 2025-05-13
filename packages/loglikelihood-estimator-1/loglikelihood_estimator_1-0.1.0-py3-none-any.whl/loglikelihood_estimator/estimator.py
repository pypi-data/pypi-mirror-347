import numpy as np
import pandas as pd

def simulate_instruments(n, k):
    """
    Simulate instruments (Z) from a normal distribution.
    """
    return np.random.normal(0, 1, size=(n, k))

def simulate_endogenous_regressors(Z, k, endog_idx):
    """
    Simulate endogenous regressors (X_endog) from a reduced-form model.
    """
    Pi = np.random.normal(0, 1, size=(k, len(endog_idx)))  # first-stage coefficients
    eta = np.random.normal(0, 1, size=(n, len(endog_idx)))  # reduced-form error terms
    X_endog = Z @ Pi + eta
    return X_endog, eta

def simulate_exogenous_regressors(n, p, endog_idx):
    """
    Simulate exogenous regressors (X_exog) from a normal distribution.
    """
    X_exog = np.random.normal(0, 1, size=(n, p - len(endog_idx)))
    return X_exog

def generate_data(n=1000, p=4, k=3, endog_idx=[0, 1], true_beta=None, sigma_v=1.0, sigma_u=1.0):
    """
    Generate a dataset with endogenous and exogenous variables.
    """
    if true_beta is None:
        true_beta = np.array([1.0, -0.5, 0.8, -1.2])  # Default values for validation

    # 1. Simulate instruments (Z)
    Z = simulate_instruments(n, k)

    # 2. Simulate endogenous regressors (X_endog) and reduced-form residuals (eta)
    X_endog, eta = simulate_endogenous_regressors(Z, k, endog_idx)

    # 3. Simulate exogenous regressors (X_exog)
    X_exog = simulate_exogenous_regressors(n, p, endog_idx)

    # 4. Full regressor matrix X = [X_endog | X_exog]
    X = np.hstack([X_endog, X_exog])

    # 5. Generate composite error: noise + inefficiency
    v = np.random.normal(0, sigma_v, size=n)  # two-sided noise
    u = np.abs(np.random.normal(0, sigma_u, size=n))  # one-sided inefficiency
    epsilon = v - u

    # 6. Generate dependent variable (y)
    y = X @ true_beta + epsilon

    # Create DataFrame for inspection
    df = pd.DataFrame(X, columns=[f"x{i+1}" for i in range(p)])
    df["y"] = y

    return df, X, eta, true_beta, sigma_v, sigma_u, epsilon

def calculate_mu_ci_and_sigma_c2(eta, sigma_v2=1.0, Sigma_veta=None):
    """
    Calculate μ_ci and σ_c^2 based on reduced-form residuals (eta).
    """
    n, k2 = eta.shape
    # Set default Sigma_veta if not provided (example values)
    if Sigma_veta is None:
        Sigma_veta = np.array([0.5, -0.3])  # Shape should match (k2,)

    # 1. Compute Σ_{ηη}: sample covariance matrix of eta
    Sigma_eta = np.cov(eta, rowvar=False)  # shape: (k2, k2)

    # 2. Compute inverse of Σ_{ηη}
    Sigma_eta_inv = np.linalg.inv(Sigma_eta)

    # 3. Compute μ_ci for each observation
    mu_ci = eta @ Sigma_eta_inv @ Sigma_veta.T  # shape: (n,)

    # 4. Compute conditional variance σ_c^2
    sigma_c2 = sigma_v2 - Sigma_veta @ Sigma_eta_inv @ Sigma_veta.T

    return mu_ci, sigma_c2

def simulate_and_display_sample_data():
    """
    Simulate the data, calculate μ_ci and σ_c^2, and display the results.
    """
    # Generate data
    df, X, eta, true_beta, sigma_v, sigma_u, epsilon = generate_data()

    # Calculate μ_ci and σ_c^2
    mu_ci, sigma_c2 = calculate_mu_ci_and_sigma_c2(eta)

    # Display the first few rows of the simulated dataset
    print("Simulated dataset sample:")
    print(df.head())

    # Display the calculated values
    print("\nμ_ci (first 5):", mu_ci[:5])
    print("σ_c^2:", sigma_c2)
