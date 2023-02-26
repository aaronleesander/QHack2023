import matplotlib.pyplot as plt


def plot_runtimes_vs_qubits(runtimes_model1, runtimes_model2, depth):
    plt.plot(runtimes_model1, label="CPU")
    plt.plot(runtimes_model2, label="GPU")

    plt.title("Runtime vs. Wires (Heisenberg Model, Depth=%d)" % depth)
    plt.xlabel("# Wires")
    plt.ylabel("Runtime (s)")
    plt.legend()
    plt.show()


def plot_fidelities_vs_noise(noise_strength_list, fidelities, depth):
    plt.loglog(noise_strength_list, fidelities)

    plt.title("Fidelity vs. Noise (Heisenberg Model, Depth=%d)" % depth)
    plt.xlabel("Noise Strength ($\gamma J$)")
    plt.ylabel("Fidelity")
    plt.show()


def plot_fidelities_vs_noise_changing_depth(noise_strength_list, fidelities, depth_list):
    for i, depth in enumerate(depth_list):
        plt.loglog(noise_strength_list, fidelities[i], label="Depth = "+str(depth))

    plt.title("Fidelity vs. Noise (Heisenberg Model)")
    plt.xlabel("Noise Strength ($\gamma J$)")
    plt.ylabel("Fidelity")
    plt.legend()
    plt.show()
