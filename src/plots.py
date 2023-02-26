import matplotlib.pyplot as plt


def plot_runtimes_vs_qubits(runtimes_model1, runtimes_model2, depth):
    plt.plot(runtimes_model1, label="CPU")
    plt.plot(runtimes_model2, label="GPU")

    plt.title("Runtime vs. Wires (Heisenberg Model, depth=%d" % depth)
    plt.xlabel("# Wires")
    plt.ylabel("Runtime (s)")
    plt.legend()
    plt.show()