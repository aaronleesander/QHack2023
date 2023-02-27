import pennylane as qml
import pennylane.numpy as np

from .noise_models import apply_depolarizing


def R_XX(angle, wire, num_wires, p, backend):
    qml.CNOT([wire,(wire+1)%num_wires][::-1])
    apply_depolarizing(wire, p)
    qml.RX(angle, wires=(wire+1)%num_wires)
    qml.CNOT([wire,(wire+1)%num_wires][::-1])
    apply_depolarizing(wire, p)


def R_YY(angle, wire, num_wires, p, backend):
    qml.RZ(np.pi/2, wires=wire)
    qml.RZ(np.pi/2, wires=(wire+1)%num_wires)
    qml.CNOT([wire,(wire+1)%num_wires][::-1])
    apply_depolarizing(wire, p)
    qml.RX(angle, wires=(wire+1)%num_wires)
    qml.CNOT([wire,(wire+1)%num_wires][::-1])
    apply_depolarizing(wire, p)
    qml.RZ(-np.pi/2, wires=wire)
    qml.RZ(-np.pi/2, wires=(wire+1)%num_wires)


def R_ZZ(angle, wire, num_wires, p, backend):
    qml.CNOT([wire,(wire+1)%num_wires])
    apply_depolarizing(wire, p)
    qml.RZ(angle, wires=(wire+1)%num_wires)
    qml.CNOT([wire,(wire+1)%num_wires])
    apply_depolarizing(wire, p)

def R_X(angle, wire):
    qml.RX(angle, wires=wire)
