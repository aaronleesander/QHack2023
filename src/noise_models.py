import pennylane as qml
import pennylane.numpy as np


def apply_depolarizing(wire, p, backend):
    if backend =='lightning.qubit' or backend =='lightning.gpu':
        r = np.random.rand()
        # divide range [0,1] in [0, p/3]: X; [p/3, 2p/3]: Y; [2p/3, p]: Z; [p, 1]: Id
        if 0 <= r <= p/3:
            qml.PauliX(wires=wire)
        elif  p/3 < r <= 2*p/3:
            qml.PauliY(wires=wire)
        elif  2*p/3 < r <= p:
            qml.PauliZ(wires=wire)
    elif backend == 'default.mixed':
        if p!=0:
            qml.DepolarizingChannel(p, wires=wire)
        else:
            pass

