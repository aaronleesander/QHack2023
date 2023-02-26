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


def calculate_heisenberg_fidelity_vs_noise(backend, wires, couplings, T, depth, noise_probability, noise_strength_list):
    fidelities = []
    for noise_strength in noise_strength_list:
        dev = qml.device(backend, wires=wires)

        # TODO: Only calculate noiseless state once rather than in fidelity
        @qml.qnode(dev)
        def heisenberg_trotter(couplings, T, depth, noise_probability, noise_strength):
            simulate_heisenberg_model(wires, couplings, T, depth, noise_probability, noise_strength)
            return qml.state()
        noiseless_state = heisenberg_trotter(couplings, T, depth, noise_probability=0, noise_strength=0)
        fidelity = qml.math.fidelity(noiseless_state, heisenberg_trotter(couplings, T, depth, noise_probability, noise_strength))

        fidelities.append(fidelity)

    return fidelities