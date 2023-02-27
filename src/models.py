from .gates import R_XX, R_YY, R_ZZ, R_X
import pennylane as qml


def simulate_heisenberg_model(num_wires, couplings, T, depth, p=0):
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

    for _ in range(depth):
        for wire in range(num_wires):
            R_XX(angle_XX, wire, num_wires, p)
        for wire in range(num_wires):
            R_YY(angle_YY, wire, num_wires, p)
        for wire in range(num_wires):
            R_ZZ(angle_ZZ, wire, num_wires, p)
        for wire in range(num_wires):
            R_X(angle_X, wire)


def simulate_heisenberg_model_single_timestep(num_wires, couplings, dt, p):
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
    angle_XX = -2*couplings['J_xx']*dt
    angle_YY = -2*couplings['J_yy']*dt
    angle_ZZ = -2*couplings['J_zz']*dt
    angle_X = -2*couplings['h']*dt

    for wire in range(num_wires):
        R_XX(angle_XX, wire, num_wires, p)
    for wire in range(num_wires):
        R_YY(angle_YY, wire, num_wires, p)
    for wire in range(num_wires):
        R_ZZ(angle_ZZ, wire, num_wires, p)
    for wire in range(num_wires):
        R_X(angle_X, wire)


def create_vqe_ansatz(params, wires):
    """
    VQE ansatz for optimization
    NOTE: len(params) = 4*wires
    Args:
        params (numpy.array): parameters to be used in the variational circuit
        H (qml.Hamiltonian): Hamiltonian used to calculate the expected value

    Returns:
        (float): Expected value with respect to the Hamiltonian H
    """
    for i in range(wires):
        qml.RY(params[i], wires=i)
    
    for i in range(wires):
        qml.CNOT([i,(i+1)%wires])
    for i in range(wires, 2*wires):
        qml.RZ(params[i+4], wires=i)       
    
    for i in range(2*wires, 3*wires):
        qml.RY(params[i+8], wires=i)
    
    for i in range(wires):
        qml.CNOT([i,(i+1)%wires])

    for i in range(3*wires, 4*wires):
        qml.RZ(params[i+12], wires=i)
