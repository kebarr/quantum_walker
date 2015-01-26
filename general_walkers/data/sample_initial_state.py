import numpy as np

def sample_initial_state(n):
    vector = np.zeros((4*n))
    vector[:n] = n**-0.5
    return vector
