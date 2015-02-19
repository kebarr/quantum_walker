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


class DecoheringWalkOnCompleteGraph(WalkOnCompleteGraph, DecoheringWalkOnLine):
    def __init__(self, n, initial_state=None, coin_operator=None, state_indicator='localised'):
        self.n = n
        self.create_adjacency_matrix()
        super(DecoheringWalkOnCompleteGraph, self).__init__(n, n-1, initial_state=initial_state, coin_operator=coin_operator, adjacency_matrix=self.adjacency_matrix, state_indicator=state_indicator)

    def initialise_coin_projection_operators(self):        
        n = self.n
        # can measure either going left state, or going right state
        projs = [np.zeros_like(self.time_ev_operator) for i in range(n)]
        for i in range(n):
            coin_states = [j*n + i for j in range(n-1)]
            for index in coin_states:
                projs[i][coin_states][coin_states] = 1
        self.coin_projection_operators = projs
        self._projection_operators = self.coin_projection_operators


# ok apparently this isnt always possible!    
def create_regular_graph(number_nodes, degree):
    if number_nodes % d != 0:
        raise ValueError("number%nodes mod degree must be even for graph to exist")
    matrix = np.zeros((number_nodes, number_nodes))
    # join node x to next degree nodes
    for node in range(number_nodes):        
        if (node + 1 + degree)%number_nodes < node:
            range((node + 1 + degree)%number_nodes), node
            # we wrap round
            edges = range((node + 1 +degree)%number_nodes) + range(node + 1, number_nodes)
        else:
            edges = range(node + 1, node + degree + 1)
        print edges
        for edge in edges:
            print edge, node
            matrix[node][edge], matrix[edge][node] = 1, 1
    return matrix


# nodes > 0 already have joins from previous nodes



def initialise_coin_projection_operators(n):        
        # can measure either going left state, or going right state
        projs = [np.zeros((n**2, n**2)) for i in range(n)]
        for i in range(n):
            coin_states = [j*n + i for j in range(n)]
            print coin_states, i
            for index in coin_states:
                projs[i][index][index] = 1
        return projs


def initialise_coin_projection_operators(n):
    identity = np.eye(4)
    projs = []
    for i in range(n):
        proj = np.zeros_like(identity)
        proj[i][i] = 1
        projs.append(np.kron(identity,proj))
    return projs
        
