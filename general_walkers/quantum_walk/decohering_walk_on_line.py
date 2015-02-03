from quantum_walk.walk_on_line import QuantumWalkOnLine
import numpy as np
import matplotlib.pyplot as plt


class DecoheringWalkOnLine(QuantumWalkOnLine):
    """ Initialise and run a quantum walk with simple (Markovian) open system 
    dynamics- otherwise known as decoherence as the coherence terms of the density 
    matrix reduce. To model this process we must use the density matrix formalism 
    rather than state vect or formalism. The density matrix evolves according to a 
    master equation.

        Arguments:
        as for QuantumWalkOnLine except-
        coin_decoherence_rate- probability of making a measurement of a coin basis state during a timestep
        position_decoherence_rate- probability of making a measurement of a position basis state during a timestep

    As decoherence rate increases to 1, we recover classical random walk dynamics
    """
    def __init__(self, max_steps, coin_bias=0.5, initial_state_bias=0.5, coin_decoherence_rate=None, position_decoherence_rate=None):
        super(DecoheringWalkOnLine, self).__init__(max_steps, coin_bias, initial_state_bias)
        self.initialise_density_matrix()
        print coin_decoherence_rate, 'coin dec rate'
        if coin_decoherence_rate > 0:
            if position_decoherence_rate > 0:
                if position_decoherence_rate != coin_decoherence_rate:
                    raise ValueError("Coin and position decoherence rates must be the same, instead got %f (coin), %f (position)" % (coin_decoherence_rate, position_decoherence_rate))
                self._decoherence_rate = self.coin_decoherence_rate
            self.coin_decoherence_rate = coin_decoherence_rate
            self.initialise_coin_projection_operators()
        elif position_decoherence_rate > 0:
            self.position_decoherence_rate = position_decoherence_rate
            self.initialise_position_projection_operators()

        
    def initialise_density_matrix(self):
        state_vector = self.initial_state
        self._initial_density_matrix = state_vector[:, np.newaxis]*np.conjugate(state_vector)
        self.current_state = self._initial_density_matrix

    @property
    def initial_density_matrix(self):
        return self._initial_density_matrix


    def initialise_coin_projection_operators(self):        
        # can measure either going left state, or going right state
        proj_left = np.zeros_like(self.time_ev_operator)
        proj_right = np.zeros_like(self.time_ev_operator)
        for i, row in enumerate(proj_left):
            if i % 2 == 0:
                row[i] = 1
            else:
                proj_right[i][i] = 1
        self.coin_projection_operators = [proj_left, proj_right]
        self._decoherence_rate = self.coin_decoherence_rate
        self._projection_operators = self.coin_projection_operators

    def initialise_position_projection_operators(self):
        number_positions = self.line_length
        position_projection_operators = []
        for i in range(number_positions):
            projection_operator = np.zeros_like(self.time_ev_operator)
            projection_operator[2*i][2*i] = 1
            projection_operator[2*i + 1][2*i + 1] = 1
            position_projection_operators.append(projection_operator)
        self.position_projection_operators = position_projection_operators
        self._decoherence_rate = self.position_decoherence_rate
        self._projection_operators = self.position_projection_operators

    def initialise_coin_position_projection_operators(self):
        number_positions = self.line_length
        projection_operators = []
        for i in range(number_positions):
            projection_operator_l = np.zeros_like(self.time_ev_operator)
            projection_operator_r = np.zeros_like(self.time_ev_operator)
            projection_operator_l[2*i][2*i] = 1
            projection_operator_r[2*i + 1][2*i + 1] = 1
            projection_operators.append(projection_operator_l)
            projection_operators.append(projection_operator_r)
        self._projection_operators = projection_operators

    # don't think there's actually any point in this function
    def initialise_projection_operators(self):
        if self.coin_projection_operators is not None:
            self._decoherence_rate = self.coin_decoherence_rate
            self._projection_operators = self.coin_projection_operators
        elif self.position_projection_operators is not None:
            self._decoherence_rate = self.position_decoherence_rate
            self._projection_operators = self.position_projection_operators
        else:
            # WORK OUT WHY I DID THIS!!
            self._decoherence_rate = 1
            self._projection_operators = np.eye(self.time_ev_operator.shape[0])

    @property 
    def decoherence_rate(self):
        return self._decoherence_rate

    @property 
    def projection_operators(self):
        return self._projection_operators

    # don't need to reimplement steps
    def step(self):
        print 'dec steo', self.current_state.shape
        quantum = np.dot(self.time_ev_operator, np.dot(self.current_state, np.conjugate(self.time_ev_operator.transpose())))
        decohered = np.zeros_like(quantum)
        projs = self.projection_operators
        for proj in projs:
            decohered += np.dot(proj, np.dot(self.current_state, proj))
        decoherence_rate = self.decoherence_rate
        self.current_state = (1-decoherence_rate)*quantum + decoherence_rate*decohered
        
        
    def calculate_probabilities(self):
        # in density matrix formalism probs are diagonals
        probs = np.diagonal(self.current_state)
        probs_final = [probs[i] + probs[i+1] for i in xrange(len(probs)) if i % 2 ==0]
        print probs_final
        assert np.allclose(np.array([np.sum(probs_final)]), np.array([1]), atol=self.tolerance)
        return probs_final

    # care must be taken with the maths of these.
    def step_back(self):
        raise NotImplementedError("TODO")

    def go_to_step(self):
        raise NotImplementedError("TODO")
