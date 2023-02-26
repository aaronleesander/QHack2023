import numpy as np
import pennylane as qml
from timeit import default_timer as timer

from .models import simulate_heisenberg_model, simulate_heisenberg_model_single_timestep


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


def calculate_heisenberg_entropy_vs_time(backend, wires, couplings, T, depth, noise_probability, noise_strength):
    dev = qml.device(backend, wires=wires)

    @qml.qnode(dev)
    def heisenberg_trotter(init_state, couplings, dt, noise_probability, noise_strength):
        qml.QubitStateVector(init_state, wires=range(wires))
        simulate_heisenberg_model_single_timestep(wires, couplings, dt, noise_probability, noise_strength)
        return qml.state()

    init_state = np.zeros(2**wires)
    init_state[0] = 1
    entropies = []

    dt = T / depth
    for i in range(depth):
        state = heisenberg_trotter(init_state, couplings, dt, noise_probability, noise_strength)
        entropy = qml.math.vn_entropy(state, indices=[w for w in range(wires//2)])
        entropies.append(entropy)
        init_state = state

    return entropies