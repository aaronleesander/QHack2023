import matplotlib.pyplot as plt


def plot_runtimes_vs_qubits(runtimes_model1, runtimes_model2, depth, p=0, labels=["CPU", "GPU"]):
    plt.plot(runtimes_model1, label=labels[0])
    plt.plot(runtimes_model2, label=labels[1])

    plt.title(f"Runtime vs. Wires (Heisenberg Model, Depth={depth}, p={p})")
    plt.xlabel("# Wires")
    plt.ylabel("Runtime (s)")
    plt.legend()
    plt.show()


def plot_fidelities_vs_noise(p_list, fidelities, depth):
    plt.plot(p_list, fidelities, marker='*', linestyle='')
    plt.xscale('log')
    plt.title("Fidelity vs. Noise (Heisenberg Model, Depth=%d)" % depth)
    plt.xlabel("p")
    plt.ylabel("Fidelity")
    plt.show()


def plot_fidelities_vs_noise_changing_depth(p_list, fidelities, depth_list):
    for i, depth in enumerate(depth_list):
        plt.loglog(p_list, fidelities[i], label="Depth = "+str(depth))

    plt.title("Fidelity vs. Noise (Heisenberg Model)")
    plt.xlabel("p")
    plt.ylabel("Fidelity")
    plt.legend()
    plt.show()


def plot_entropies_vs_time(entropies_list, p_list):
    for i, p in enumerate(p_list):
        plt.plot(entropies_list[i], label="p = "+str(p))
    plt.title("Entropy vs. Time (Heisenberg Model)")
    plt.xlabel("Time")
    plt.ylabel("Entropy")
    plt.legend()
    plt.show()
