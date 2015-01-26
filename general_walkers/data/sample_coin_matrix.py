def sample_coin(n):
     dft = fft(np.eye(n))
     end_nodes_coin = dft/scipy.linalg.norm(dft)
     a = 2**-0.5
     hadamard = np.array([[a, a],[a, -a]])
     all_coins = [end_nodes_coin]
     for i in range(n):
          all_coins.append(hadamard)
     all_coins.append(end_nodes_coin)
     return scipy.linalg.block_diag(*all_coins)

