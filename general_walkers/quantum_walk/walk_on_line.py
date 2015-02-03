from quantum_walk.walker import QuantumWalk
import numpy as np
import matplotlib.pyplot as plt


class QuantumWalkOnLine(QuantumWalk):
    """Simulate the quantum walk on the line, initialised with configurable
       coin and initial state bias. Inititally walker starts localised at a
       single node, in the center of the line.
       N.b. adjacency matrix specifies a cycle. This cycle is larger than 2 times
       the number of steps in the walk, so amplitude never meets at the other side.
       Hence, it is a valid simulation of the walk on the line.
       Arguments:
       max_steps- this is the maximum number of steps the walk will be run for
       initial_state_bias- initial probability distribution of amplitude in 'going 
       left' and 'going right' states.
       coin_bias- amount of amplitude coin sends left and right on a given step
    """
    def __init__(self, max_steps, coin_bias=0.5, initial_state_bias=0.5):
        self.max_steps = max_steps
        self.line_length = 2*max_steps + 2 # making graph larger than number of steps simulates walk on infinite line
        self.coin_bias = coin_bias
        self.initial_state_bias = initial_state_bias
        self.create_adjacency_matrix()
        self.create_initial_state(initial_state_bias)
        self.create_coin(coin_bias)
        print self.coin.shape, self.initial_state.shape
        self.number_of_steps = 0
        super(QuantumWalkOnLine, self).__init__(self.initial_state, self.coin, self.adjacency_matrix)
        

    def step(self):
        """ Perform one step of walk on line.
            As number of steps we can validly run for is limited by construction
            raise value error if this step would take us beyond limit
        """
        max_steps = self.max_steps
        curr_steps = self.number_of_steps
        if curr_steps < max_steps:
            self.number_of_steps += 1
            super(QuantumWalkOnLine, self).step()
        else:
            raise ValueError("Total number of steps %d must be less than %d" % (curr_steps, max_steps))

    
    def steps(self, n):
        if self.number_of_steps + n < self.max_steps:
            self.number_of_steps += n
            super(QuantumWalkOnLine, self).steps(n)
        else:
            raise ValueError("Total number of steps %d must be less than %d" % (self.number_of_steps, max_steps))

    def go_to_step(self, step):
        if self.number_of_steps + step < self.max_steps:
            self.number_of_steps += step
            super(QuantumWalkOnLine, self).go_to_step(step)
        else:
            raise ValueError("Total number of steps %d must be less than %d" % (curr_steps, max_steps))

    def create_adjacency_matrix(self):
        """ Creates adjacency matrix for a graph of a cycle of length size.
            Each node, n, is connected by single edges to nodes n-1 and n+2
        """
        size = self.line_length
        graph = np.zeros((size, size), dtype=int)
        indices = np.array([i for i in range(size-1)])
        right_links = [i+1 for i in range(size-1)]
        left_links = [(i-1) for i in range(1, size)]
        graph[indices, right_links] = 1
        graph[indices + 1, left_links] = 1
        # join up to create cycle to avoid edge effects, amplitude never reaches here anyway
        graph[0][-1], graph[-1][0] = 1, 1
        self.adjacency_matrix = graph
    

    def create_initial_state(self, initial_state_bias):
        size = self.line_length + 1
        middle = size/2
        vector = np.zeros((2*(size - 1)))
        vector[2*middle] = initial_state_bias**0.5
        vector[2*middle + 1] = (1-initial_state_bias)**0.5
        self.initial_state = vector

    def create_coin(self, coin_bias):
        size = self.line_length
        a = coin_bias**0.5
        b = (1-coin_bias)**0.5
        coin_at_nodes = np.array([[a, b],[b, -a]])
        id = np.eye(size)
        self.coin = np.kron(id, coin_at_nodes)
        print self.coin.shape

    def plot(self):
        xs = self.calculate_probabilities()
        length = self.line_length/2
        fig = plt.figure()
        plt.title("Distribution of walk on line after %d steps" % self.number_of_steps)
        plt.xlabel('Position')
        plt.ylabel('Probabilitiy')
        plt.plot(range(-length, length), xs)
        plt.show()
