from quantum_walk.walker import QuantumWalk
import numpy as np



class QuantumWalkOnLine(QuantumWalk):
    def __init__(self, max_steps, coin_bias, initial_state_bias):
        self.line_length = max_steps + 2 # making graph larger than number of steps simulates walk on infinite line
        self.coin_bias = coin_bias
        self.initial_state_bias = initial_state_bias
        self.create_adjacency_matrix()
        self.create_initial_state(initial_state_bias)
        self.create_coin(coin_bias)
        super(QuantumWalkOnLine, self).__init__(self.initial_state, self.coin, self.adjacency_matrix)


    def create_adjacency_matrix(self):
        """ Creates adjacency matrix for a graph of a line of length size.
            Each node, n, is connected by single edges to nodes n-1 and n+2
        """
        size = self.line_length
        graph = np.zeros((size, size), dtype=int)
        indices = np.array([i for i in range(size-1)])
        right_links = [i+1 for i in range(size-1)]
        left_links = [(i-1) for i in range(1, size)]
        graph[indices, right_links] = 1
        graph[indices + 1, left_links] = 1
        self.adjacency_matrix = graph
    

    def create_initial_state(self, initial_state_bias):
        size = self.line_length
        middle = size/2
        vector = [0 for i in range(2*size)]
        vector[2*middle] = initial_state_bias**0.5
        vector[2*middle] = (1-initial_state_bias)**0.5
        self.initial_state = vector

    def create_coin(self, coin_bias):
        size = self.line_length
        coin_states = 2*(size + 1)
        coin_matrix = np.zeros((coin_states, coin_states))
        a = coin_bias**0.5
        b = (1-coin_bias)**0.5
        coin_at_nodes = np.array([[a, b],[a, b]])
        id = np.eye(size)
        self.coin = np.kron(id, coin_at_nodes)
