from scipy.linalg import hadamard

from complete_graph import WalkOnCompleteGraph


def f(n):
    if n == 1:
        result = 2
    else:
        result = 2**(2**(n-1))
    return result

def g(n):
    return 1


class LevyWalkerCoinModel(WalkOnCompleteGraph):

    def __init__(self, n,a_amp=2**-0.5,b_amp=2**-0.5, g_function=g, f_function=f):
        self.n = n
        self.size = 2**(self.n+1)+1
        self.g_function = g_function
        self.f_function = f_function
        self.create_initial_state(a_amp=a_amp,b_amp=b_amp)
        self.create_coin_operator()
        super(LevyWalkerCoinModel, self).__init__(size, initial_state=self.initial_state, coin_operator=self.coin_operator)

    def create_coin_operator(self):
        size = self.size
        m_matrix = self.m_matrix
        self.coin_operator = np.kron(np.identity(size), m_matrix)
        print self.coin_operator.shape

    def create_initial_state(self, a_amp=2**-0.5, b_amp=2**-0.5):
        n = self.n
        total_probability = np.array([a_amp*np.conjugate(a_amp) + b_amp*np.conjugate(b_amp)])
        assert np.allclose(np.array([1]), total_probability)
        graph_size = 2**(n+1) + 1
        size = graph_size*(graph_size-1)
        # all sites being equal, select site 1 as initial- so always s
        state_vector = np.zeros(size, dtype=complex)
        state_vector[graph_size] = a_amp
        state_vector[graph_size+1] = b_amp
        self.initial_state =  state_vector
        print self.initial_state.shape


    def hadamard_coins(self):
        n = self.n
        result = hadamard(2**n) # in this hadamard, n is dimension
        result_abs = result**2 # as real, no need for complex conjugate
        normalisation_coeffs = result_abs.sum(axis=1)**0.5
        final = np.array([[float(result[i][j])/normalisation_coeffs[j] for j in range(len(result[0]))] for i in range(len(result))])
        return final

    @property
    def x_matrix(self):
        n = self.n
        pauli_x = np.array([[0,1],[1,0]])
        result = pauli_x
        for i in range(1, n):
            result = np.kron(pauli_x, result)
        return result 

    def r_matrix_coeff(self, i):
        g = self.g_function
        f = self.f_function
        return ((f(i)**2 + g(i)**2)**0.5)**(-1)

    @property
    def r_matrix(self):
        n = self.n
        f_g_matrix = np.array([[f(1), g(1)],[g(1), -f(1)]])*self.r_matrix_coeff(1)
        result = f_g_matrix
        for i in xrange(2,n+1):
            f_g_matrix = np.array([[f(i), g(i)],[g(i), -f(i)]])*self.r_matrix_coeff(i)
            result = np.kron(f_g_matrix, result)
        return result

    @property
    def m_matrix(self):
        n = self.n
        h_coin = self.hadamard_coins()
        r_coin = self.r_matrix
        x_coin = self.x_matrix
        assert x_coin.shape == r_coin.shape == h_coin.shape
        top_right_block = np.dot(np.dot(h_coin, r_coin), h_coin)
        bottom_right_block = np.dot(np.dot(np.dot(-x_coin, h_coin), r_coin), h_coin)
        bottom_left_block = np.dot(x_coin, r_coin)
        top_row = np.hstack([r_coin, top_right_block])
        bottom_row = np.hstack([bottom_left_block,bottom_right_block])
        result = (2**0.5)**(-1)*np.vstack([top_row, bottom_row])
        return result
