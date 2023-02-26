from .gates import R_XX, R_YY, R_ZZ, R_X


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
    angle_XX = -2*couplings['J_xx']*T/depth
    angle_YY = -2*couplings['J_yy']*T/depth
    angle_ZZ = -2*couplings['J_zz']*T/depth
    angle_X = -2*couplings['h']*T/depth

    for j in range(depth):
        for wire in range(num_wires):
        #first the XX, YY, ZZ part:
            R_XX(angle_XX, wire, num_wires, noise_probability, noise_strength)
        for wire in range(num_wires):
            R_YY(angle_YY, wire, num_wires, noise_probability, noise_strength)
        for wire in range(num_wires):
            R_ZZ(angle_ZZ, wire, num_wires, noise_probability, noise_strength)
        for wire in range(num_wires):
            R_X(angle_X, wire)
