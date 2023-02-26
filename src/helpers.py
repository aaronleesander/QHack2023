from . import helpers
import matplotlib.pyplot as plt
import pennylane as qml

def helper_test():
    # Write code here
    pass

def draw_circuit_nice(function:qml.qnode, **kwargs):
    "draw quantum function from pennylane in a nice visual format"
    qml.drawer.use_style("black_white")
    fig, ax = qml.draw_mpl(function)(**kwargs)
    plt.show()