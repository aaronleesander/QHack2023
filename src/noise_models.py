import pennylane as qml
import pennylane.numpy as np


def apply_Pauli_noise(wire, noise_probability, noise_strength):
    if np.random.rand() < noise_probability: 
        qml.RX(noise_strength, wires=wire)

    if np.random.rand() < noise_probability: 
        qml.RY(noise_strength, wires=wire)

    if np.random.rand() < noise_probability: 
        qml.RZ(noise_strength, wires=wire)
