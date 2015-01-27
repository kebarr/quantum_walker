Simulate quantum walks
======================

A command line application which simulates an arbitrary quantum walk, given a coin and suitable adjacency matrix. At each step of the simulation probabilities of measuring the walker at each node are either printed or saved to file. A quantum walk is a quantum mechanical analogue of a classical random walk. Roughly, it is a process which evolves accoding to a sucession of 'coin flips' followed by shift operations, in such a way that it is reversible. 

An adjacency matrix is a matrix representation of a graph G(E,V) where V is a set of vertices, and E a set of edges connecting these. This can be passed in either as a pickled numpy array, or a function which, for integer argument n, produces an appropriately sized array. 

The coin matrix determines how, at each node of the graph, probability (really amplitude) arriving from a given node will leave. This probability can interfere with probability which has arrived from other nodes. This is passed in in the same way as the adjacency matrix, the mode must be the same for both.

There is an option to run a walk on a line, which is configured with the number of timesteps to run for. The probability distribution after this number of timesteps is then plotted.

In the data folder, there are samples for both reading in operators from pickled files, and functions to generate operators.

Quantum walks are quantum mechanical analogues of classical random walks. There is extensive literature on them. This library has been written to facilitate ongoing research into these processes.

Features hopefully to come
----------------------------------

* Decoherence in both coin and position space.
* Analysis- e.g. look for high probability at particular node, or whether probability is roughly even at each node
* Creation of random initial conditions
* Multiple runs, stats gathering
