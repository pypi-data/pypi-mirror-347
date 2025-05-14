from pennylane import numpy as np
import pennylane as qml
def quantum_relative_entropy(rho, sigma):
    eigvals_rho, eigvecs_rho = np.linalg.eigh(rho)
    log_rho = eigvecs_rho @ np.diag(np.log2(np.clip(eigvals_rho, 1e-10, 1.0))) @ eigvecs_rho.conj().T
    eigvals_sigma, eigvecs_sigma = np.linalg.eigh(sigma)
    log_sigma = eigvecs_sigma @ np.diag(np.log2(np.clip(eigvals_sigma, 1e-10, 1.0))) @ eigvecs_sigma.conj().T
    return np.real(np.trace(rho @ (log_rho - log_sigma)))