from quantum_walk.walker import QuantumWalk
from quantum_walk.decohering_walk_on_line import DecoheringWalkOnLine
import numpy as np
import warnings


# TODO: function which creates adjacency matrix for regular graph size n of degree degree
class WalkOnRegularGraph(QuantumWalk):
    """ Walk on regular graph, i.e. degree at each node is the same. Pass in single size n coin matrix and block diagonalising is taken care of.
    """ 
    def __init__(self, n, degree, adjacency_matrix, initial_state=None, coin_operator=None, state_indicator='localised'):
        self.n = n
        self.degree = degree
        if self.n == self.degree - 1:
            warnings.warn("Use WalkOnCompleteGraph for more functionality in this use case")
        if initial_state is None:
            self.create_default_initial_state(state_indicator)
        else:
            self.initial_state = initial_state
        if coin_operator is None:
            self.create_default_coin()
        else:
            self.coin_operator = coin_operator
        print self.coin_operator.shape, self.initial_state.shape
        super(WalkOnRegularGraph, self).__init__(self.initial_state, self.coin_operator, adjacency_matrix)
        self.check_adjacency_matrix()


    # TODO: selection of coin operators
    def create_default_coin(self):
        #n = self.n
        #joins_per_node = n - 1
        degree = self.degree
        identity = np.eye(degree)
        grover =  2./degree - identity
        self.coin_operator = np.kron(np.eye(self.n),  grover)

    def check_adjacency_matrix(self):
        degrees = np.array([np.sum(node) for node in self.adjacency_matrix])
        if not np.all(degrees==degrees[0]):
            raise ValueError("Irregular graph specified")

    def create_default_initial_state(self, state_indicator):
        state_vector = np.zeros(self.n*self.degree)
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
