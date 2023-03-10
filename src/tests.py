import numpy as np
import pennylane as qml
from timeit import default_timer as timer

from .models import simulate_heisenberg_model, simulate_heisenberg_model_single_timestep


def calculate_heisenberg_runtime_vs_qubits(backend, num_wires_list, couplings, T, depth, p, samples=1):
    runtimes = []
    for wires in num_wires_list:
        start = timer()
        if backend == 'default.mixed':
            samples = 1
        for _ in range(samples):
            dev = qml.device(backend, wires=wires)

            @qml.qnode(dev)
            def heisenberg_trotter(couplings, T, depth, p):
                simulate_heisenberg_model(wires, couplings, T, depth, p, backend)
                return qml.state()

            _ = heisenberg_trotter(couplings, T, depth, p)
        end = timer()
        runtimes.append(end - start)

    return runtimes


def calculate_heisenberg_runtime_fidelity_vs_qubits(backend, num_wires_list, couplings, T, depth, p, samples=1):
    """this function returns both the runtime and fidelity"""
    runtimes = []
    states = []
    for wires in num_wires_list:
        if backend == 'default.mixed':
            samples = 1
        state = np.zeros((2**wires,2**wires), dtype=complex)
        start = timer()
        state_list = []
        for _ in range(samples):
            dev = qml.device(backend, wires=wires)

            @qml.qnode(dev)
            def heisenberg_trotter(couplings, T, depth, p):
                simulate_heisenberg_model(wires, couplings, T, depth, p, backend)
                return qml.state()

            s = heisenberg_trotter(couplings, T, depth, p)

            state_list.append(s)
        end = timer()

        if backend == 'default.mixed':
            for s in state_list:
                state += s
        else:
            for s in state_list:
                state += np.outer(s, s.conj())

        runtimes.append(end - start)
        states.append(state/samples)
    return runtimes, states


def calculate_sv_samples(couplings, backend='lightning.qubit', T=1, depth=100, wires=5, p=0.0033, samples=1500):
    """this function returns both the runtime and fidelity for statevector simulation"""
    runtimes = [] # will store time it took from start -> time_k for k = {100, 200,...1500}
    states = [] # will the final state after all the 1500 samples
    
    start = timer()
    for k in range(samples):
        dev = qml.device(backend, wires=wires)
        @qml.qnode(dev)
        def heisenberg_trotter(couplings, T, depth, p):
            simulate_heisenberg_model(wires, couplings, T, depth, p, backend)
            return qml.state()

        state = heisenberg_trotter(couplings, T, depth, p)
        if (k+1)%100 == 0:
            time_k = timer()
            runtimes.append(time_k - start)

        states.append(state) # append all the 1500 states for convergence calculation

    return runtimes, states


def calculate_heisenberg_fidelity_vs_noise(backend, wires, couplings, T, depth, p_list, samples=1):
    all_fidelities = []
    if backend == 'default.mixed':
            samples = 1
    for i in range(samples):
        fidelities = []
        for p in p_list:
            dev = qml.device(backend, wires=wires)

            # TODO: Only calculate noiseless state once rather than in fidelity
            @qml.qnode(dev)
            def heisenberg_trotter(couplings, T, depth, p):
                simulate_heisenberg_model(wires, couplings, T, depth, p, backend)
                return qml.state()
            noiseless_state = heisenberg_trotter(couplings, T, depth, p=0)
            fidelity = qml.math.fidelity(noiseless_state, heisenberg_trotter(couplings, T, depth, p))

            fidelities.append(fidelity)
        all_fidelities.append(fidelities)

    all_fidelities = np.transpose(all_fidelities)
    avg_fidelities = []
    for fidelities in all_fidelities:
        avg_fidelities.append(np.mean(fidelities, axis=0))

    return avg_fidelities


def calculate_heisenberg_fidelity_vs_qubits(backend, num_wires_list, couplings, T, depth, p, samples=1):
    all_fidelities = []
    if backend == 'default.mixed':
            samples = 1
    for i in range(samples):
        fidelities = []
        for wires in num_wires_list:
            dev = qml.device(backend, wires=wires)

            # TODO: Only calculate noiseless state once rather than in fidelity
            @qml.qnode(dev)
            def heisenberg_trotter(couplings, T, depth, p, backend):
                simulate_heisenberg_model(wires, couplings, T, depth, p, backend)
                return qml.state()
            if i == 0:
                noiseless_state = heisenberg_trotter(couplings, T, depth, p=0, backend='default.mixed')
            fidelity = qml.math.fidelity(noiseless_state, heisenberg_trotter(couplings, T, depth, p))

            fidelities.append(fidelity)
        all_fidelities.append(fidelities)

    all_fidelities = np.transpose(all_fidelities)
    avg_fidelities = []
    for fidelities in all_fidelities:
        avg_fidelities.append(np.mean(fidelities, axis=0))

    return avg_fidelities


def calculate_heisenberg_entropy_vs_time(backend, wires, couplings, T, depth, p, samples):
    all_entropies = []
    for i in range(samples):
        dev = qml.device(backend, wires=wires)

        @qml.qnode(dev)
        def heisenberg_trotter(init_state, couplings, dt, p):
            qml.QubitStateVector(init_state, wires=range(wires))
            simulate_heisenberg_model_single_timestep(wires, couplings, dt, p, backend)
            return qml.state()

        init_state = np.zeros(2**wires)
        init_state[0] = 1
        entropies = []

        dt = T / depth
        for i in range(depth):
            state = heisenberg_trotter(init_state, couplings, dt, p)
            entropy = qml.math.vn_entropy(state, indices=[w for w in range(wires//2)])
            entropies.append(entropy)
            init_state = state
        all_entropies.append(entropies)

    all_entropies = np.transpose(all_entropies)
    avg_entropies = []
    for entropies in all_entropies:
        avg_entropies.append(np.mean(entropies, axis=0))

    return avg_entropies

