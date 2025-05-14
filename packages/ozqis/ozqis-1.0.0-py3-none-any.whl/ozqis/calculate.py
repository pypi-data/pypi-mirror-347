from pennylane import numpy as np
import pennylane as qml
def calculate(qre_list, epochs, n_qubits):
    d = 2 ** n_qubits
    S_max = np.log2(d)
    OzQIS = 1 - (np.sum(qre_list) / (epochs * S_max))
    OzQIS = np.clip(OzQIS, 0, 1)
    print(OzQIS)
    return OzQIS