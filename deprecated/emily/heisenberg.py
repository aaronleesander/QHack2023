import json
from xxlimited import Xxo
import pennylane as qml
import pennylane.numpy as np
from timeit import default_timer as timer

#num_wires = 10 #increase this

#dev = qml.device("default.mixed", wires=num_wires) #lightning.qubit # lightning.gpu




def simulate(dev, couplings, p, time, depth):
    @qml.qnode(dev)
    def heisenberg_trotter(couplings, p, time, depth):
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


        def XX(i):
            # XX
            qml.RY(0,wires=1)
            print([i,(i+1)%num_wires][::-1])
            qml.CNOT([i,(i+1)%num_wires][::-1])
            if np.random.rand() < p: 
                qml.RX(0.01, wires=i)
                qml.RY(0.01, wires=i)
                qml.RZ(0.01, wires=i)
            qml.RX(-2*couplings[0]*time/depth, wires=(i+1)%num_wires)
            qml.CNOT([i,(i+1)%num_wires][::-1])
            if np.random.rand() < p: 
                qml.RX(0.01, wires=i)
                qml.RY(0.01, wires=i)
                qml.RZ(0.01, wires=i)


        def YY(i):
            #YY
            qml.RZ(np.pi/2, wires=i)
            qml.RZ(np.pi/2, wires=(i+1)%4)
            qml.CNOT([i,(i+1)%num_wires][::-1])
            if np.random.rand() < p: 
                qml.RX(0.01, wires=i)
                qml.RY(0.01, wires=i)
                qml.RZ(0.01, wires=i)
            qml.RX(-2*couplings[1]*time/depth, wires=(i+1)%num_wires)
            qml.CNOT([i,(i+1)%num_wires][::-1])
            if np.random.rand() < p: 
                qml.RX(0.01, wires=i)
                qml.RY(0.01, wires=i)
                qml.RZ(0.01, wires=i)
            qml.RZ(-np.pi/2, wires=i)
            qml.RZ(-np.pi/2, wires=(i+1)%num_wires)

        def ZZ(i):
            #ZZ
            qml.CNOT([i,(i+1)%num_wires])
            if np.random.rand() < p: 
                qml.RX(0.01, wires=i)
                qml.RY(0.01, wires=i)
                qml.RZ(0.01, wires=i)
            qml.RZ(-2*couplings[2]*time/depth, wires=(i+1)%num_wires)
            qml.CNOT([i,(i+1)%num_wires])
            if np.random.rand() < p: 
                qml.RX(0.01, wires=i)
                qml.RY(0.01, wires=i)
                qml.RZ(0.01, wires=i)


        def magnet(i):
            #magnetic field
            qml.RX(-2*couplings[3]*time/depth, wires=i)
        for j in range(depth):
            for i in num_wires:
            #first the XX, YY, ZZ part:
                XX(i)
            for i in num_wires:
                YY(i)
            for i in num_wires:
                ZZ(i)
            for i in num_wires:
                magnet(i)

        return qml.state()

    return heisenberg_trotter(couplings, p, time, depth)

def our_depolarising_noise(p): 
    qml.Identity(wires=i) * np.sqrt(1-p)
    qml.PauliX(wires=i) * np.sqrt(p/3)
    qml.PauliY(wires=i) * np.sqrt(p/3)
    qml.PauliZ(wires=i) * np.sqrt(p/3)



def calculate_fidelity(dev, couplings, p, time, depth):
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
    return qml.math.fidelity(simulate(dev, couplings,0,time, depth),simulate(dev, couplings,p,time,depth))


num_wires = np.arange(2, 5)

timing = []
for t in num_wires:
    dev = qml.device("default.mixed", wires=num_wires) #lightning.gpu
    start = timer()
    calculated_fidelity_results = calculate_fidelity(dev, [1,2,1,0.3],0.5,2.5,1)
    end = timer()
    print(calculated_fidelity_results)
    timing.append(end - start)

print(qml.numpy.mean(timing))

#print(calculated_fidelity_results)