import json
import pennylane as qml
import pennylane.numpy as np

num_wires = 4 #increase this

dev = qml.device("default.mixed", wires=num_wires) #lightning.qubit # lightning.gpu




def create_hamiltonian(params):

        couplings = [-params[-1]]
        ops = [qml.PauliX(3)]

        for i in range(3):

            couplings = [-params[-1]] + couplings
            ops = [qml.PauliX(i)] + ops        

        for i in range(4):

            couplings = [-params[-2]] + couplings
            ops = [qml.PauliZ(i)@qml.PauliZ((i+1)%4)] + ops

        for i in range(4):

            couplings = [-params[-3]] + couplings
            ops = [qml.PauliY(i)@qml.PauliY((i+1)%4)] + ops

        for i in range(4):

            couplings = [-params[0]] + couplings
            ops = [qml.PauliX(i)@qml.PauliX((i+1)%4)] + ops    

        return qml.Hamiltonian(couplings,ops)

@qml.qnode(dev)
def evolve(params, time, depth):

    qml.ApproxTimeEvolution(create_hamiltonian(params), time, depth)

    return qml.state()



def calculate_fidelity(couplings, p, time, depth):
    """This function returns the fidelity between the final states of the noisy and
    noiseless Trotterizations of the Heisenberg models, using only CNOT and rotation gates
    Args:
        couplings (list(float)): 
            A list with the J_x, J_y, J_z and h parameters in the Heisenberg Hamiltonian, as
            defined in the problem statement.
        p (float): The depolarization probability of the depolarization gate that acts on the
                   target qubit of each CNOT gate.
        time (float): The period of time evolution simulated by the Trotterization.
        depth (int): The Trotterization depth.
    Returns:
        (float): Fidelity between final states of the noisy and noiseless Trotterizations
    """
    return qml.math.fidelity(heisenberg_trotter(couplings,0,time, depth),heisenberg_trotter(couplings,p,time,depth))

qml.math.fidelity(heisenberg_trotter(random_params,0,1,2),evolve(random_params,1,2))