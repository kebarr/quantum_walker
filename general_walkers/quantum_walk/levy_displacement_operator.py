from walk_on_line import QuantumWalkOnLine
import numpy as np

class LevyWalker(QuantumWalkOnLine):
    """Two of Tim's models are of the form U = S.(I \otimes C \otimes L), varying L
    To measure project onto line? L represents the shift length. How is this correlated with the position? shift goes from |x, c, l \rangle to |x + cl, c, l \rangle
    """
    def __init__(self, max_steps, max_shift_length, coin_bias=0.5, initial_state_bias=0.5):
        self.l = max_shift_length
        super(LevyWalker, self).__init__(max_steps, coin_bias=coin_bias, initial_state_bias=initial_state_bias, jump=max_shift_length)
    
    def create_adjacency_matrix(self):
        print 'creating adj'
        size = self.line_length
        l = self.l
        graph = np.zeros((size, size), dtype=int)
        right_links = [[position + shift for shift in range(l)] for position in range(1, size - l + 1)]
        left_links = [[position - shift for shift in range(l)] for position in range(l, size)]
        for i, jump_to in enumerate(right_links):
                graph[i, jump_to] = 1
                graph[left_links[i], i] = 1
        for i in range(l):
            graph[size-l-i][-i] = 1
            graph[-i][size-l-i] = 1
        # join up at end to make shift operator creation work
        for i in range(l+1):
            for j in range(i):
                print i, j
                graph[-j][-i] = 1
                graph[-i][-j] = 1
                graph[i-j][-j] = 1
                graph[-j][i-j] = 1
        print graph
        self.adjacency_matrix = graph

    #def create_coin(self):
        #coin_at_nodes = np.kron(self.c, self.l_matrix)
        #id = np.eye(size)
        #self.coin = np.kron(id, coin_at_nodes)


    # CHECK CAREFULLY!!!
    def create_initial_state(self):
        print 'creating init'
        initial_state_bias = self.initial_state_bias
        size = self.line_length + 1
        l = self.l*2 # times by 2 as links go in both directions
        middle = size/2
        vector = np.zeros((l*(size - 1)))
        vector[l*middle] = initial_state_bias**0.5
        vector[l*middle + 1] = (1-initial_state_bias)**0.5
        self.initial_state = vector
        print vector




def create_adjacency_matrx(l, size):
        graph = np.zeros((size, size), dtype=int)
        indices = np.array([i for i in range(size-1)])
        right_links = [[position + shift for shift in range(l)] for position in range(1, size - l + 1)]
        left_links = [[position - shift for shift in range(l)] for position in range(l, size)]
        print left_links, right_links
        print len(left_links), len(right_links)
        for i, jump_to in enumerate(right_links):
                print i, jump_to
                graph[i, jump_to] = 1
                graph[left_links[i], i] = 1
        for i in range(l+1):
            for j in range(i):
                print i, j
                graph[-j][-i] = 1
                graph[-i][-j] = 1
                graph[i-j][-j] = 1
                graph[-j][i-j] = 1
        return graph


def create_adjacency_matrix2(line_length):
        """ Creates adjacency matrix for a graph of a cycle of length size.
            Each node, n, is connected by single edges to nodes n-1 and n+1
        """
        size = line_length
        graph = np.zeros((size, size), dtype=int)
        indices = np.array([i for i in range(size-1)])
        right_links = [i+1 for i in range(size-1)]
        left_links = [(i-1) for i in range(1, size)]
        graph[indices, right_links] = 1
        graph[indices + 1, left_links] = 1
        # join up to create cycle to avoid edge effects, amplitude never reaches here anyway
        graph[0][-1], graph[-1][0] = 1, 1
        print graph

# verify expected size of coin
def create_coin(coin_bias, size, l):
        a = coin_bias**0.5
        b = (1-coin_bias)**0.5
        coin_at_nodes = np.array([[a, b],[b, -a]])
        id = np.eye(size)
        l = np.eye(l)
        coin = np.kron(id, np.kron(coin_at_nodes, l))
        print coin.shape
