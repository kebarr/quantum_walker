from quantum_walk.walker import QuantumWalk
from quantum_walk.decohering_walk_on_line import DecoheringWalkOnLine
import numpy as np


# TODO: function which creates adjacency matrix for regular graph size n of degree degree
class WalkOnRegularGraph(QuantumWalk):
    """ Walk on regular graph, i.e. degree at each node is the same. Pass in single size n coin matrix and block diagonalising is taken care of.
    """ 
    def __init__(self, n, degree, adjacency_matrix, initial_state=None, coin_operator=None, state_indicator='localised'):
        self.n = n
        self.degree = degree
        if initial_state is None:
            self.create_default_initial_state(state_indicator)
        else:
            self.initial_state = initial_state
        if coin_operator is None:
            self.create_default_coin()
        else:
            self.coin_operator = coin_operator
        self.check_adjacency_matrix()
        super(WalkOnRegularGraph, self).__init__(self.initial_state, self.coin_operator, adjacency_matrix)

    # TODO: selection of coin operators
    def create_default_coin(self):
        n = self.n
        joins_per_node = n - 1
        identity = np.eye(joins_per_node)
        grover =  2./joins_per_node - identity
        self.coin_operator = np.kron(np.eye(n),  grover)

    def check_adjacency_matrix(self):
        degrees = np.array([np.sum(node) for node in self.adjacency_matrix])
        if not np.all(degrees==degrees[0]):
            raise ValueError("Irregular graph specified")

    def create_default_initial_state(self, state_indicator):
        state_vector = np.zeros(self.n*self.degree)
        print state_vector, 'ss', state_indicator
        if state_indicator == 'superposition':
            val = self.n**-0.5
            state_vector += val
        elif state_indicator == 'localised':
            state_vector[0] = 1
            print state_vector
        else:
            raise NotImplementedError("Default initial state format %s not implements" % state_indicator)
        self.initial_state = state_vector
        print self.initial_state, 'inti'


class WalkOnCompleteGraph(WalkOnRegularGraph):
    """ A walk which runs on a graph of size n where every node is connected to every other node.

    This walk could be run by passing in appropriate pickled data/functions, 
    however, by having a class, we can subclass it with appropriate decoherence operators. I still need to work out how to do decoherence in the coin state on non-regular graphs. 
    """
    def __init__(self, n, initial_state=None, coin_operator=None, state_indicator='localised'):
        self.n = n
        self.create_adjacency_matrix()
        super(WalkOnCompleteGraph, self).__init__(n, n-1, initial_state=initial_state, coin_operator=coin_operator, adjacency_matrix=self.adjacency_matrix, state_indicator=state_indicator)

    def create_adjacency_matrix(self):
        n = self.n
        matrix = np.ones((n, n))
        np.fill_diagonal(matrix, 0)
        self.adjacency_matrix = matrix

    
