import pennylane as qml
import pennylane.numpy as np

def create_ising(h, wires):
    """
    create ising hamiltonian

    Args:
        h (float): magnetic field strength
        wires (int): number of wires/qubits in circuit

    Returns:
        (qml.Hamiltonian): Hamiltonian of Ising model
    """
    couplings = [-h]
    ops = [qml.PauliX(wires-1)]

    for i in range(wires-1):
        couplings = [-h] + couplings
        ops = [qml.PauliX(i)] + ops   
    
    for i in range(wires):
        couplings = [-1] + couplings
        ops = [qml.PauliZ(i)@qml.PauliZ((i+1)%wires)] + ops

    return qml.Hamiltonian(couplings,ops)

def create_heisenberg(couplings, wires):
    """
    create ising hamiltonian

    Args:
        couplings (list(float)): 
            A list with the J_x, J_y, J_z and h parameters in the Heisenberg Hamiltonian
        wires (int): number of wires/qubits in circuit

    Returns:
        (qml.Hamiltonian): Hamiltonian of Heisenberg model
    """

    couplings = [-couplings[-1]]
    ops = [qml.PauliX(wires-1)]

    for i in range(wires-1):
        couplings = [-couplings[-1]] + couplings
        ops = [qml.PauliX(i)] + ops        

    for i in range(4):
        couplings = [-couplings[-2]] + couplings
        ops = [qml.PauliZ(i)@qml.PauliZ((i+1)%wires)] + ops

    for i in range(4):
        couplings = [-couplings[-3]] + couplings
        ops = [qml.PauliY(i)@qml.PauliY((i+1)%wires)] + ops

    for i in range(4):
        couplings = [-couplings[0]] + couplings
        ops = [qml.PauliX(i)@qml.PauliX((i+1)%wires)] + ops    

    return qml.Hamiltonian(couplings,ops)