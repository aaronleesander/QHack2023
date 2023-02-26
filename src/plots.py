import matplotlib.pyplot as plt


def plot_runtimes_vs_qubits(runtimes_model1, runtimes_model2, depth):
    plt.plot(runtimes_model1, label="CPU")
    plt.plot(runtimes_model2, label="GPU")

    plt.title("Runtime vs. Wires (Heisenberg Model, Depth=%d)" % depth)
    plt.xlabel("# Wires")
    plt.ylabel("Runtime (s)")
    plt.legend()
    plt.show()


def plot_fidelities_vs_noise(noise_probability_list, fidelities, depth):
    plt.plot(noise_probability_list, fidelities)
    plt.xscale('log')
    plt.title("Fidelity vs. Noise (Heisenberg Model, Depth=%d)" % depth)
    plt.xlabel("p")
    plt.ylabel("Fidelity")
    plt.show()


def plot_fidelities_vs_noise_changing_depth(noise_probability_list, fidelities, depth_list):
    for i, depth in enumerate(depth_list):
        plt.loglog(noise_probability_list, fidelities[i], label="Depth = "+str(depth))

    plt.title("Fidelity vs. Noise (Heisenberg Model)")
    plt.xlabel("p")
    plt.ylabel("Fidelity")
    plt.legend()
    plt.show()


def plot_entropies_vs_time(entropies_list, noise_probability_list):
    for i, noise_probability in enumerate(noise_probability_list):
        plt.plot(entropies_list[i], label="Prob = "+str(noise_probability))
    plt.title("Entropy vs. Time (Heisenberg Model)")
    plt.xlabel("Time")
    plt.ylabel("Entropy")
    plt.legend()
    plt.show()
