import pennylane as qml
import pennylane.numpy as np

from .noise_models import apply_Pauli_noise


def XX(angle, wire, num_wires, noise_probability, noise_strength):
    qml.CNOT([wire,(wire+1)%num_wires][::-1])
    apply_Pauli_noise(wire, noise_probability, noise_strength)
    qml.RX(angle, wires=(wire+1)%num_wires)
    qml.CNOT([wire,(wire+1)%num_wires][::-1])
    apply_Pauli_noise(wire, noise_probability, noise_strength)


def YY(angle, wire, num_wires, noise_probability, noise_strength):
    qml.RZ(np.pi/2, wires=wire)
    qml.RZ(np.pi/2, wires=(wire+1)%num_wires)
    qml.CNOT([wire,(wire+1)%num_wires][::-1])
    apply_Pauli_noise(wire, noise_probability, noise_strength)

    qml.RX(angle, wires=(wire+1)%num_wires)
    qml.CNOT([wire,(wire+1)%num_wires][::-1])
    apply_Pauli_noise(wire, noise_probability, noise_strength)
    qml.RZ(-np.pi/2, wires=wire)
    qml.RZ(-np.pi/2, wires=(wire+1)%num_wires)


def ZZ(angle, wire, num_wires, noise_probability, noise_strength):
    qml.CNOT([wire,(wire+1)%num_wires])
    apply_Pauli_noise(wire, noise_probability, noise_strength)
    qml.RZ(angle, wires=(wire+1)%num_wires)
    qml.CNOT([wire,(wire+1)%num_wires])
    apply_Pauli_noise(wire, noise_probability, noise_strength)


def X(angle, wire):
    qml.RX(angle, wires=wire)