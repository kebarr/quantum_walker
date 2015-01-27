import numpy as np
import math
from time_ev_operators import createshift

def is_unitary(operator, tolerance=0.0001):
    h, w = operator.shape
    if not h == w:
        return False
    adjoint = np.conjugate(operator.transpose())
    product1 = np.dot(operator, adjoint)
    product2 = np.dot(adjoint, operator)
    id = np.eye(h)
    return np.allclose(product1, id) & np.allclose(product2, id)



class QuantumWalk(object):
    """Basic quantum walk, where the user defines the initial state and time evolution operators
    """
    def __init__(self, initial_state, coin_operator, adjacency_matrix):
        print adjacency_matrix
        if not is_unitary(coin_operator):
            raise ValueError("Coin operator must be unitary")
        else:
            self.coin_operator = coin_operator
        self.shift_operator = createshift(adjacency_matrix)
        print self.shift_operator.shape
        # if invalid adjacency matrix passed in, shift operator isn't validly quantum mechanical
        if not is_unitary(self.shift_operator):
            raise ValueError("Adjacency matirx must have a maximum of 1 link between each pair of nodes and contain no self loops")
        self.time_ev_operator = np.dot(self.shift_operator, coin_operator)
        if initial_state is None:
            self.create_default_initial_state()
        else:
            self.initial_state = initial_state
        self.current_state = initial_state
        self.adjacency_matrix = adjacency_matrix
        self.tolerance = 0.0001
        self.degree = len(adjacency_matrix)
    

    def create_default_initial_state(self):
        basis_states = self.time_ev_operator.shape[0]
        vector = np.zeros((basis_states))
        vector[0] = 1
        self.initial_state = vector

    def step(self):
        self.current_state = np.dot(self.time_ev_operator, self.current_state)

    def step_back(self):
        self.current_state = np.dot(np.conjugate(self.time_ev_operator.transpose()), self.current_state)

    def steps(self, n):
        for i in xrange(n):
            state = np.dot(self.time_ev_operator, self.current_state)
        self.current_state = state

    @property
    def node_degrees(self):
        adj = self.adjacency_matrix
        return [int(np.sum(adj[i])) for i in xrange(len(adj))]

    def probability_at_node(self, index):
        if index > len(self.adjacency_matrix):
            raise ValueError("Graph doesn't contain %d nodes" % index)
        probs = self.calculate_probabilities()
        return probs[index]

    def calculate_probabilities(self):
        graph_size = len(self.adjacency_matrix)
        # how many coin states at each node dictates how amplitude should be distributed
        node_degrees = self.node_degrees
        probs = [0 for i in range(graph_size)]
        index = 0
        # for each node, sum probability at each coin state
        for i in xrange(graph_size):
            for j in xrange(node_degrees[i]):
                amp_at_coin_state_j = self.current_state[index]  
                probs[i] += amp_at_coin_state_j*np.conjugate(amp_at_coin_state_j)
                # nodes can be of variable degree so track total coin states summed
                index += 1
        # sanity check
        assert np.allclose(np.array([np.sum(probs)]), np.array([1]), atol=self.tolerance)
        return probs

    def go_to_step(self, step):
        if step == 0:
            self.current_state = self.initial_state
            return self.current_state
        time_ev_op = self.time_ev_operator
        eig = LA.eig(time_ev_op)[1]
        inverse = LA.inv(eig)
        diag = np.dot(np.dot(inverse, time_ev_op), eig)
        for i in range(len(diag)):
            transition_prob = diag[i][i]
            x = transition_prob.real
            y = transition_prob.imag
            theta = math.atan2(y, x)
            z = (x**2 + y**2)**0.5
            # de moivre
            diag[i][i] = math.cos(step*theta) + complex(0, math.sin(step*theta))
        # need to transform basis of state as well as matrix
        transformed_basis_vector = np.dot(inverse, self.initial_state)
        evolved = np.dot(diag, transformed_basis_vector)
        transformed_back = np.dot(eig, evolved)
        self.current_state = transformed_back
        return transformed_back


# for sample, do first few steps of hadamard on cycle
def create_sample_inputs():
    initial_state = [0 for i in range(2*4)]
    a = 2**-0.5
    initial_state[0], initial_state[1] = a, complex(0, a)
    hadamard = np.array([[a, a],[a, -a]])
    id_4 = np.eye(4)
    coin = np.kron(id_4, hadamard)
    adjacency_matrix = [[0,1,0,1],[1,0,1,0],[0,1,0,1],[1,0,1,0]]
    return initial_state, coin, adjacency_matrix


def create_sample_initial_state():
    initial_state = [0 for i in range(2*4)]
    a = 2**-0.5
    initial_state[0], initial_state[1] = a, complex(0, a)
    return initial_state


def create_sample_time_ev_operators():
    a = 2**-0.5
    hadamard = np.array([[a, a],[a, -a]])
    id_4 = np.eye(4)
    coin = np.kron(id_4, hadamard)
    adjacency_matrix = [[0,1,0,1],[1,0,1,0],[0,1,0,1],[1,0,1,0]]
    return coin, adjacency_matrix
