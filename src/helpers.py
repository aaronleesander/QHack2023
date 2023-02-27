from . import helpers
import matplotlib.pyplot as plt
import pennylane as qml
import pennylane.numpy as np

def helper_test():
    # Write code here
    pass

def draw_circuit_nice(function:qml.qnode, **kwargs):
    "draw quantum function from pennylane in a nice visual format"
    qml.drawer.use_style("black_white")
    fig, ax = qml.draw_mpl(function)(**kwargs)
    plt.show()

def calculate_error(approx, exact):
    "approx: sv, exact: dm"
    #sigma_exact = np.sqrt(np.diag(exact))
    #error = 1 - np.abs(np.vdot(approx,sigma_exact))**2

    return  abs(1 - qml.math.fidelity(approx, exact))