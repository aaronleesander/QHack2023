import pennylane as qml
from timeit import default_timer as timer

from .models import simulate_heisenberg_model


def calculate_heisenberg_runtime_vs_qubits(backend, num_wires_list, couplings, T, depth, noise_probability, noise_strength):
    runtimes = []
    for wires in num_wires_list:
        dev = qml.device(backend, wires=wires)

        @qml.qnode(dev)
        def heisenberg_trotter(couplings, T, depth, noise_probability, noise_strength):
            simulate_heisenberg_model(wires, couplings, T, depth, noise_probability, noise_strength)
            return qml.state()
    
        start = timer()
        state = heisenberg_trotter(couplings, T, depth, noise_probability, noise_strength)
        end = timer()
        runtimes.append(end - start)

    return runtimes