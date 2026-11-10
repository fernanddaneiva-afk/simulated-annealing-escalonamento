from sa_scheduling import (lower_bound, lpt, makespan, random_instance,
                           simulated_annealing)


def test_makespan_simples():
    assert makespan([0, 1, 0], [3, 4, 5], 2) == 8


def test_lower_bound_valido():
    times = random_instance(30, 1)
    m = 4
    assert lower_bound(times, m) <= makespan(lpt(times, m), times, m)


def test_sa_nunca_pior_que_lpt():
    times = random_instance(40, 2)
    m = 5
    _, c_sa = simulated_annealing(times, m, iters=3000, seed=0)
    assert c_sa <= makespan(lpt(times, m), times, m)


def test_sa_reprodutivel():
    times = random_instance(25, 3)
    a = simulated_annealing(times, 3, iters=2000, seed=7)
    b = simulated_annealing(times, 3, iters=2000, seed=7)
    assert a == b


def test_atribuicao_completa():
    times = random_instance(20, 4)
    assign, _ = simulated_annealing(times, 3, iters=500)
    assert len(assign) == 20 and set(assign) <= {0, 1, 2}
