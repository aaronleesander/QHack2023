import pennylane as qml
import pennylane.numpy as np


def apply_Pauli_noise(wire, noise_probability, noise_strength):
    if np.random.rand() < noise_probability: 
        qml.RX(noise_strength, wires=wire)

    if np.random.rand() < noise_probability: 
        qml.RY(noise_strength, wires=wire)

    if np.random.rand() < noise_probability: 
        qml.RZ(noise_strength, wires=wire)


def apply_depolarizing(wire, p):
    r = np.random.rand()
    # divide range [0,1] in [0, p/3]: X; [p/3, 2p/3]: Y; [2p/3, p]: Z; [p, 1]: Id
    if 0 <= r <= p/3:
        qml.PauliX(wires=wire)
    elif  p/3 < r <= 2*p/3:
        qml.PauliY(wires=wire)
    elif  2*p/3 < r <= p:
        qml.PauliZ(wires=wire)
    else: 
        pass
