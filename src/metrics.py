import pennylane as qml
import pennylane.numpy as np

from .models import simulate_heisenberg_model


def calculate_fidelity(num_wires, couplings, T, depth, noise_probability=0, noise_strength=0):
    """This function returns the fidelity between the final states of the noisy and
    noiseless Trotterizations of the Heisenberg models, using only CNOT and rotation gates
    Args:
        couplings (list(float)): 
            A list with the J_x, J_y, J_z and h parameters in the Heisenberg Hamiltonian, as
            defined in the problem statement.
        p (float): The depolarization probability of the depolarization gate that acts on the
                   target qubit of each CNOT gate.
        time (float): The period of time evolution simulated by the Trotterization.
        depth (int): The Trotterization depth.
    Returns:
        (float): Fidelity between final states of the noisy and noiseless Trotterizations
    """
    return qml.math.fidelity(heisenberg_trotter(num_wires, couplings, T, depth, noise_probability=0, noise_strength=0), heisenberg_trotter(num_wires, couplings, T, depth, noise_probability, noise_strength))
