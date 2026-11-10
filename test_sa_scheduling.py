import random

import pytest

from sa_scheduling import (PERTURBATIONS, balance_step, initial_solution,
                           lower_bounds, machine_completion, makespan,
                           random_instance, rpd, simulated_annealing)


def jobs_of(sol):
    return sorted(j for q in sol for j in q)


def test_setup_antecipado():
    # r=10 > s=3: o setup ocorre antes da liberação; fim = r + p = 15
    assert machine_completion([0], [5], [3], [10]) == 15
    # r=2 < s=3: o setup domina; fim = s + p = 8
    assert machine_completion([0], [5], [3], [2]) == 8


def test_makespan_duas_maquinas():
    p, s, r = [4, 6], [1, 1], [0, 0]
    assert makespan([[0], [1]], p, s, r) == 7


def test_limitantes_validos():
    p, s, r = random_instance(30, (1, 99), seed=1)
    lb = lower_bounds(p, s, r, 3)
    sol = simulated_annealing(p, s, r, 3, seed=0)[0]
    assert lb["LB"] <= makespan(sol, p, s, r)


def test_solucao_inicial_completa():
    p, s, r = random_instance(25, (1, 49), seed=2)
    sol = initial_solution(p, s, r, 4)
    assert jobs_of(sol) == list(range(25))


@pytest.mark.parametrize("name", list(PERTURBATIONS))
def test_perturbacoes_preservam_tarefas(name):
    p, s, r = random_instance(20, (1, 99), seed=3)
    sol = initial_solution(p, s, r, 3)
    rng = random.Random(0)
    for _ in range(200):
        new = PERTURBATIONS[name](sol, rng)
        if new is not None:
            assert jobs_of(new) == list(range(20))


def test_sa_reprodutivel():
    p, s, r = random_instance(20, (1, 49), seed=4)
    assert simulated_annealing(p, s, r, 3, seed=7) == simulated_annealing(p, s, r, 3, seed=7)


def test_etapa_melhoria_nao_piora():
    p, s, r = random_instance(20, (1, 49), seed=5)
    sol = initial_solution(p, s, r, 3)
    _, c = balance_step(sol, p, s, r)
    assert c <= makespan(sol, p, s, r)


def test_rpd():
    assert rpd(110, 100) == pytest.approx(10.0)
import random

import pytest

from sa_scheduling import (PERTURBATIONS, balance_step, initial_solution,
                           lower_bounds, machine_completion, makespan,
                           random_instance, rpd, simulated_annealing)


def jobs_of(sol):
    return sorted(j for q in sol for j in q)


def test_setup_antecipado():
    # r=10 > s=3: o setup ocorre antes da liberação; fim = r + p = 15
    assert machine_completion([0], [5], [3], [10]) == 15
    # r=2 < s=3: o setup domina; fim = s + p = 8
    assert machine_completion([0], [5], [3], [2]) == 8


def test_makespan_duas_maquinas():
    p, s, r = [4, 6], [1, 1], [0, 0]
    assert makespan([[0], [1]], p, s, r) == 7


def test_limitantes_validos():
    p, s, r = random_instance(30, (1, 99), seed=1)
    lb = lower_bounds(p, s, r, 3)
    sol = simulated_annealing(p, s, r, 3, seed=0)[0]
    assert lb["LB"] <= makespan(sol, p, s, r)


def test_solucao_inicial_completa():
    p, s, r = random_instance(25, (1, 49), seed=2)
    sol = initial_solution(p, s, r, 4)
    assert jobs_of(sol) == list(range(25))


@pytest.mark.parametrize("name", list(PERTURBATIONS))
def test_perturbacoes_preservam_tarefas(name):
    p, s, r = random_instance(20, (1, 99), seed=3)
    sol = initial_solution(p, s, r, 3)
    rng = random.Random(0)
    for _ in range(200):
        new = PERTURBATIONS[name](sol, rng)
        if new is not None:
            assert jobs_of(new) == list(range(20))


def test_sa_reprodutivel():
    p, s, r = random_instance(20, (1, 49), seed=4)
    assert simulated_annealing(p, s, r, 3, seed=7) == simulated_annealing(p, s, r, 3, seed=7)


def test_etapa_melhoria_nao_piora():
    p, s, r = random_instance(20, (1, 49), seed=5)
    sol = initial_solution(p, s, r, 3)
    _, c = balance_step(sol, p, s, r)
    assert c <= makespan(sol, p, s, r)


def test_rpd():
    assert rpd(110, 100) == pytest.approx(10.0)
import random

import pytest

import random

import pytest

from sa_scheduling import (PERTURBATIONS, balance_step, initial_solution,
                           lower_bounds, machine_completion, makespan,
                           random_instance, rpd, simulated_annealing)


def jobs_of(sol):
    return sorted(j for q in sol for j in q)


def test_setup_antecipado():
    # r=10 > s=3: o setup ocorre antes da liberação; fim = r + p = 15
    assert machine_completion([0], [5], [3], [10]) == 15
    # r=2 < s=3: o setup domina; fim = s + p = 8
    assert machine_completion([0], [5], [3], [2]) == 8


def test_makespan_duas_maquinas():
    p, s, r = [4, 6], [1, 1], [0, 0]
    assert makespan([[0], [1]], p, s, r) == 7


def test_limitantes_validos():
    p, s, r = random_instance(30, (1, 99), seed=1)
    lb = lower_bounds(p, s, r, 3)
    sol = simulated_annealing(p, s, r, 3, seed=0)[0]
    assert lb["LB"] <= makespan(sol, p, s, r)


def test_solucao_inicial_completa():
    p, s, r = random_instance(25, (1, 49), seed=2)
    sol = initial_solution(p, s, r, 4)
    assert jobs_of(sol) == list(range(25))


@pytest.mark.parametrize("name", list(PERTURBATIONS))
def test_perturbacoes_preservam_tarefas(name):
    p, s, r = random_instance(20, (1, 99), seed=3)
    sol = initial_solution(p, s, r, 3)
    rng = random.Random(0)
    for _ in range(200):
        new = PERTURBATIONS[name](sol, rng)
        if new is not None:
            assert jobs_of(new) == list(range(20))


def test_sa_reprodutivel():
    p, s, r = random_instance(20, (1, 49), seed=4)
    assert simulated_annealing(p, s, r, 3, seed=7) == simulated_annealing(p, s, r, 3, seed=7)


def test_etapa_melhoria_nao_piora():
    p, s, r = random_instance(20, (1, 49), seed=5)
    sol = initial_solution(p, s, r, 3)
    _, c = balance_step(sol, p, s, r)
    assert c <= makespan(sol, p, s, r)


def test_rpd():
    assert rpd(110, 100) == pytest.approx(10.0)
import random

import pytest

from sa_scheduling import (PERTURBATIONS, balance_step, initial_solution,
                           lower_bounds, machine_completion, makespan,
                           random_instance, rpd, simulated_annealing)


def jobs_of(sol):
    return sorted(j for q in sol for j in q)


def test_setup_antecipado():
    # r=10 > s=3: o setup ocorre antes da liberação; fim = r + p = 15
    assert machine_completion([0], [5], [3], [10]) == 15
    # r=2 < s=3: o setup domina; fim = s + p = 8
    assert machine_completion([0], [5], [3], [2]) == 8


def test_makespan_duas_maquinas():
    p, s, r = [4, 6], [1, 1], [0, 0]
    assert makespan([[0], [1]], p, s, r) == 7


def test_limitantes_validos():
    p, s, r = random_instance(30, (1, 99), seed=1)
    lb = lower_bounds(p, s, r, 3)
    sol = simulated_annealing(p, s, r, 3, seed=0)[0]
    assert lb["LB"] <= makespan(sol, p, s, r)


def test_solucao_inicial_completa():
    p, s, r = random_instance(25, (1, 49), seed=2)
    sol = initial_solution(p, s, r, 4)
    assert jobs_of(sol) == list(range(25))


@pytest.mark.parametrize("name", list(PERTURBATIONS))
def test_perturbacoes_preservam_tarefas(name):
    p, s, r = random_instance(20, (1, 99), seed=3)
    sol = initial_solution(p, s, r, 3)
    rng = random.Random(0)
    for _ in range(200):
        new = PERTURBATIONS[name](sol, rng)
        if new is not None:
            assert jobs_of(new) == list(range(20))


def test_sa_reprodutivel():
    p, s, r = random_instance(20, (1, 49), seed=4)
    assert simulated_annealing(p, s, r, 3, seed=7) == simulated_annealing(p, s, r, 3, seed=7)


def test_etapa_melhoria_nao_piora():
    p, s, r = random_instance(20, (1, 49), seed=5)
    sol = initial_solution(p, s, r, 3)
    _, c = balance_step(sol, p, s, r)
    assert c <= makespan(sol, p, s, r)


def test_rpd():
    assert rpd(110, 100) == pytest.approx(10.0)
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
