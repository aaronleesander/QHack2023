num_wires_list_CPU = range(2, 21)
num_wires_list_GPU = range(2, 25)
couplings = [1, 2, 1, 0.3]
T = 2.5
depth = 100

noise_probability = 0
noise_strength = 0


# Run:
runtimes_CPU = calculate_heisenberg_runtime_vs_qubits("lightning.qubit", num_wires_list_CPU, couplings, T, depth, noise_probability, noise_strength)

runtimes_GPU = calculate_heisenberg_runtime_vs_qubits("lightning.gpu", num_wires_list_GPU, couplings, T, depth, noise_probability, noise_strength)

# Plot:

import matplotlib.pyplot as plt
plot_runtimes_vs_qubits(runtimes_CPU, runtimes_GPU, depth)
plt.savefig('../../runtime_gpu_cpu.png', bbox_inches='tight')
