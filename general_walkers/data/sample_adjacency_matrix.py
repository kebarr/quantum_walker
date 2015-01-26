def sample_graph(n):
    number_of_nodes = n + 2
    adj = np.zeros((number_of_nodes, number_of_nodes), dtype=int)
    for i in xrange(1, number_of_nodes - 1):
        # join every node to first and last
        adj[i][0], adj[i][-1] = 1, 1
        adj[0][i], adj[-1][i] = 1, 1
    return adj
