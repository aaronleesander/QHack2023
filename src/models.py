from .gates import XX, YY, ZZ, X


def simulate_heisenberg_model(num_wires, couplings, T, depth, noise_probability=0, noise_strength=0):
    """This QNode returns the final state of the spin chain after evolution for a time t, 
    under the Trotter approximation of the exponential of the Heisenberg Hamiltonian.
    
    Args:
        couplings (list(float)): 
            An array of length 4 that contains the coupling constants and the magnetic field 
            strength, in the order [J_x, J_y, J_z, h].
        p (float): The depolarization probability after each CNOT gate.
        depth (int): The Trotterization depth.
        time (float): Time during which the state evolves
    Returns:
        (numpy.tensor): The evolved quantum state.
    """
    J_x = -2*couplings[0]*T/depth
    J_y = -2*couplings[1]*T/depth
    J_z = -2*couplings[2]*T/depth
    h = -2*couplings[3]*T/depth

    for j in range(depth):
        for wire in range(num_wires):
        #first the XX, YY, ZZ part:
            XX(J_x, wire, num_wires, noise_probability, noise_strength)
        for wire in range(num_wires):
            YY(J_y, wire, num_wires, noise_probability, noise_strength)
        for wire in range(num_wires):
            ZZ(J_z, wire, num_wires, noise_probability, noise_strength)
        for wire in range(num_wires):
            X(h, wire)
