import matplotlib.pyplot as plt
import pennylane as qml
import pennylane.numpy as np


def draw_circuit_nice(function:qml.qnode, **kwargs):
    "draw quantum function from pennylane in a nice visual format"
    qml.drawer.use_style("black_white")
    plt.figure(dpi=400)
    fig, ax = qml.draw_mpl(function)(**kwargs)
    plt.savefig(f"./final_plots/circuit.pdf", format="pdf", bbox_inches='tight')
    plt.show()


def calculate_error(approx, exact):
    "approx: sv, exact: dm"
    #sigma_exact = np.sqrt(np.diag(exact))
    #error = 1 - np.abs(np.vdot(approx,sigma_exact))**2

    return  abs(1 - qml.math.fidelity(approx, exact))


def calculate_mean(obs:np.ndarray, vectors:list[np.ndarray]):
    """
    Calculate the mean (expectation value) of F(vectors)=fidelity.
    See pennylane.math.fidelity for details
    Args:
        obs (np.ndarray): observable object to use for the calculation of mean and deviation. 
        Real density matrix from density matrix evolution
    Returns:
        expectation value of observable
    """
    R = len(vectors)
    m = 0
    for v in vectors:
        m += qml.math.fidelity(obs,v)
    return m/R


def calculate_mean_paper(obs:np.ndarray, vectors:list[np.ndarray]):
    s = np.zeros_like(vectors[0])
    R = len(vectors)
    for v in vectors:
        s += abs(v)**2
    phi = s/R
    sigma_exact = np.diag(obs)
    f = abs(np.vdot(np.sqrt(phi), np.sqrt(sigma_exact)))**2
    return f


def calculate_avg_dms(vectors:list[np.ndarray]):
    r"calculate average density matrix for list of \ket{phi^r}"
    
    R = len(vectors)
    d = len(vectors[0])
    rho = np.zeros((d,d), dtype=complex)
    print(rho.shape)
    for v in vectors:
        rho += np.outer(v, v.conj())
    rho_avg = (rho/R)
    return rho_avg


def calculate_std(obs:np.ndarray, vectors:list[np.ndarray], means=None, bias:bool=False, mode=str):
    """
    Calculate the standard deviation for the observable F(vectors)=fidelity 

    Args:
        obs (np.ndarray): observable object to use for the calculation of mean and deviation. 
        Real density matrix from density matrix evolution
        bias (Optional(bool)): Determines the factor in denominator for calculation. Defaults to False -> R(R-1) (unbiased)
        else R (bias)
    Returns:
       standard deviation of observable
    """
   
    R = len(vectors)
    if not bias:
        if R == 1:
            factor = 1
        else:
            factor = R*(R-1)
    else:
        factor = R

    if not means:
        if mode=='normal':
            mean = calculate_mean(obs=obs, vectors=vectors)
        if mode=='paper':
            mean = calculate_mean_paper(obs=obs, vectors=vectors)
    s = 0
    for v in vectors:
        if mode=='normal':
            s += (qml.math.fidelity(obs,v) - mean)**2
        if mode=='paper':
            phi = abs(v)**2
            rho_exact = np.diag(obs)
            f =  abs(np.vdot(np.sqrt(phi), np.sqrt(rho_exact)))**2
            s += ( f - mean)**2
    return np.sqrt(s/factor)


def calculate_std_vs_ntraj(obs:np.ndarray, vectors:list[np.ndarray], mode='paper'):
    "states: "

    stds = []
    Rmax = len(vectors)
    ntrajs = list(np.arange(0,Rmax+1,10))
    for idx in ntrajs[1:]:
        stds.append(calculate_std(obs=obs,vectors=vectors[:idx], mode=mode))

    exp = 1/np.sqrt(ntrajs[1:])
    scale = exp[1]/stds[1]
    return ntrajs, stds, exp, scale

def calculate_mean_vs_ntraj(obs:np.ndarray, vectors:list[np.ndarray], mode='paper'):
    "states: "

    means = []
    Rmax = len(vectors)
    ntrajs = list(np.arange(0,Rmax+1,10))
    for idx in ntrajs[1:]:
        if mode=='paper':
            means.append(calculate_mean_paper(obs=obs,vectors=vectors[:idx]))
        if mode =='normal':
            means.append(calculate_mean(obs=obs,vectors=vectors[:idx]))

    return ntrajs, means