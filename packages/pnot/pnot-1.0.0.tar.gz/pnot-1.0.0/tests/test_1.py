def test_with_python():
    # Test the following three implementations give the same values (both markovian and non-markovian cases)
    # 1. non-parallel python solver
    # 2. parallel python solver
    # 3. parallel c++ solver

    import numpy as np
    from pnot import nested_ot
    from pnot.utils import adapted_wasserstein_squared, matrixL2paths
    from pnot.py_solver import nested_ot_solver_py

    random_seed = 0
    n_sample = 100
    T = 3

    L = np.array([[1, 0, 0], [1, 1, 0], [1, 1, 1]])
    X, A = matrixL2paths(L, n_sample, seed=random_seed)

    M = np.array([[1, 0, 0], [2, 1, 0], [2, 1, 2]])
    Y, B = matrixL2paths(M, n_sample, seed=random_seed)

    awd2square = adapted_wasserstein_squared(A, B)

    grid_size = 0.1

    for markovian in [True, False]:
        v1 = nested_ot_solver_py(
            X, Y, grid_size, markovian, parallel=False, num_threads=4, power=2
        )
        v2 = nested_ot_solver_py(
            X, Y, grid_size, markovian, parallel=True, num_threads=4, power=2
        )
        v3 = nested_ot(X, Y, grid_size, markovian, num_threads=4, power=2, verbose=True)
        assert np.abs(v1 - v2) < 1e-10
        assert np.abs(v2 - v3) < 1e-10


if __name__ == "__main__":
    test_with_python()
