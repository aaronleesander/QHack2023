import matplotlib.pyplot as plt
import os


# def plot_runtimes_vs_qubits(runtimes_model1, runtimes_model2, depth, p=0, labels=["CPU", "GPU"], samples=1, save=True):
#     plt.figure(figsize=[10, 8])
#     plt.plot(runtimes_model1, label=labels[0])
#     plt.plot(runtimes_model2, label=labels[1])
#     plt.title(f"Runtime vs. Wires (Heisenberg Model, Depth={depth}, p={p}), samples={samples})")
#     plt.xlabel("# Wires")
#     plt.ylabel("Runtime (s)")
#     plt.legend()
#     if save:
#         plt.savefig(f"time_p{p}_samples{samples}.pdf", format="pdf", bbox_inches='tight')
#     plt.show()


def plot_runtimes_vs_qubits(num_wires_list, runtimes1, runtimes2):
    script_dir = os.path.dirname(__file__) 
    rel_path = "runtime_vs_qubits.pdf"
    abs_file_path = os.path.join(script_dir, rel_path)
    plt.plot(range(2, len(runtimes1)+2), runtimes1, label='CPU', marker='*', color='tab:blue')
    plt.plot(range(2, len(runtimes2)+2), runtimes2, label='Nvidia A100', marker='*', color='tab:green')

    plt.xlabel("Qubits")
    plt.ylabel("Runtime(s)")
    plt.yscale('log')
    plt.legend()
    plt.savefig(abs_file_path, dpi=400)
    plt.show()


def plot_fidelities_vs_noise(p_list, fidelities, depth):
    script_dir = os.path.dirname(__file__) 
    rel_path = "fidelity_vs_noise.pdf"
    abs_file_path = os.path.join(script_dir, rel_path)
    plt.plot(p_list, fidelities, marker='*')
    plt.xscale('log')
    plt.xlabel("p")
    plt.ylabel("Fidelity")
    plt.savefig(abs_file_path, dpi=400)
    plt.show()


def plot_fidelities_vs_qubits(num_wires_list, fidelities, depth):
    script_dir = os.path.dirname(__file__) 
    rel_path = "fidelity_vs_wires.pdf"
    abs_file_path = os.path.join(script_dir, rel_path)
    plt.plot(num_wires_list, fidelities, marker='*')
    plt.xlabel("Wires")
    plt.ylabel("Fidelity")
    plt.savefig(abs_file_path, dpi=400)
    plt.show()


def plot_error_vs_qubits(num_wires_list, errors, depth, p=0, samples=1, save=True):
    plt.figure(figsize=[10, 8])
    plt.plot(num_wires_list, errors, marker='*', linestyle='--')
    plt.title(f"Runtime vs. Wires (Heisenberg Model, Depth={depth}, p={p}, samples={samples})")
    plt.xlabel("# wires")
    plt.ylabel("Error")
    if save:
        plt.savefig(f"error_p{p}_samples{samples}.pdf", format="pdf", bbox_inches='tight')
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
    script_dir = os.path.dirname(__file__) 
    rel_path = "entropy_vs_time.pdf"
    abs_file_path = os.path.join(script_dir, rel_path)
    for i, p in enumerate(p_list):
        if p == 0:
            continue
        plt.plot(entropies_list[i], label="p = "+str(p))

    plt.plot(entropies_list[0], linestyle='--', color='black', label="Noiseless")
    plt.xlabel("Depth")
    plt.ylabel("Entropy")
    plt.legend()
    plt.savefig(abs_file_path, dpi=400)
    plt.show()

def plot_runtime_sampling(times_dm, times_q_cpu, times_q_GPU):
    script_dir = os.path.dirname(__file__) 
    rel_path = "runtime_sampling.pdf"
    abs_file_path = os.path.join(script_dir, rel_path)

    plt.plot(range(2, len(times_dm)+2), times_dm, marker='*', linestyle='--', color='tab:orange', label=f'default.mixed')
    plt.plot(range(2, len(times_q_cpu)+1), times_q_cpu[-1], marker='*', linestyle='--', color='tab:blue', label=f'lightning.qubit')
    plt.plot(range(2, len(times_q_GPU)+6), times_q_GPU[-1], marker='*', linestyle='--', color='tab:green', label=f'lightning.gpu')
    plt.xlabel("Qubits")
    plt.ylabel("Runtime")
    plt.yscale('log')
    plt.legend()
    plt.savefig(abs_file_path, dpi=400)

    plt.show()