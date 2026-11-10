"""Simulated Annealing para escalonamento em máquinas paralelas idênticas (P||Cmax).

Minimiza o makespan: o instante em que a última máquina termina. Implementação
didática e independente, com instâncias aleatórias. Compara SA com o baseline
LPT (Longest Processing Time first) e com o limite inferior clássico.
"""
import math
import random


def makespan(assign, times, m):
    loads = [0.0] * m
    for job, mach in enumerate(assign):
        loads[mach] += times[job]
    return max(loads)


def lower_bound(times, m):
    """max(maior tarefa, carga média): nenhum escalonamento pode ser melhor."""
    return max(max(times), sum(times) / m)


def lpt(times, m):
    """Heurística gulosa: tarefas em ordem decrescente na máquina menos carregada."""
    loads = [0.0] * m
    assign = [0] * len(times)
    for job in sorted(range(len(times)), key=lambda j: -times[j]):
        mach = min(range(m), key=loads.__getitem__)
        assign[job] = mach
        loads[mach] += times[job]
    return assign


def simulated_annealing(times, m, t0=None, alpha=0.995, iters=20000, seed=0):
    rng = random.Random(seed)
    n = len(times)
    cur = lpt(times, m)                      # solução inicial: LPT
    cur_cost = makespan(cur, times, m)
    best, best_cost = cur[:], cur_cost
    temp = t0 if t0 is not None else 0.1 * cur_cost
    for _ in range(iters):
        cand = cur[:]
        if rng.random() < 0.5:               # vizinhança 1: mover tarefa
            cand[rng.randrange(n)] = rng.randrange(m)
        else:                                # vizinhança 2: trocar duas tarefas
            a, b = rng.randrange(n), rng.randrange(n)
            cand[a], cand[b] = cand[b], cand[a]
        cost = makespan(cand, times, m)
        delta = cost - cur_cost
        if delta <= 0 or rng.random() < math.exp(-delta / max(temp, 1e-12)):
            cur, cur_cost = cand, cost
            if cost < best_cost:
                best, best_cost = cand[:], cost
        temp *= alpha
    return best, best_cost


def random_instance(n, seed):
    rng = random.Random(seed)
    return [rng.randint(10, 100) for _ in range(n)]


if __name__ == "__main__":
    m = 5
    print(f"{'n':>4} {'LB':>8} {'LPT':>8} {'SA':>8}  ganho SA vs LPT")
    for n in (20, 40, 60, 100):
        times = random_instance(n, seed=n)
        lb = lower_bound(times, m)
        c_lpt = makespan(lpt(times, m), times, m)
        _, c_sa = simulated_annealing(times, m, seed=1)
        print(f"{n:>4} {lb:>8.1f} {c_lpt:>8.1f} {c_sa:>8.1f}  {(c_lpt - c_sa) / c_lpt:6.2%}")
