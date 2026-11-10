"""Simulated Annealing para o problema Pm | r_j, s_j | Cmax.

Reimplementação didática, independente e com dados sintéticos, do método descrito em:
  MESQUITA, F. N. Meta-heurística baseada em Simulated Annealing para programação
  da produção em máquinas paralelas com diferentes datas de liberação e tempos de
  setup. Dissertação (Mestrado Profissional em Gestão Organizacional), UFG, 2015.

Modelo: m máquinas idênticas; cada tarefa j tem processamento p_j, setup s_j
(independente da sequência) e data de liberação r_j. O setup pode ser antecipado:
começa assim que a máquina fica livre, mas o processamento só começa depois de r_j.
  início_j = max(fim_anterior + s_j, r_j);  fim_j = início_j + p_j;  Cmax = max fim_j.
Uma solução é uma lista de sequências, uma por máquina.
"""
import math
import random


# ----------------------------------------------------------------- avaliação
def machine_completion(seq, p, s, r):
    t = 0
    for j in seq:
        t = max(t + s[j], r[j]) + p[j]
    return t


def makespan(sol, p, s, r):
    return max(machine_completion(seq, p, s, r) for seq in sol)


# ---------------------------------------------------------- limitantes inferiores
def lower_bounds(p, s, r, m):
    """LB1..LB4 e o maior deles (eq. 3.3 a 3.7 da dissertação)."""
    n = len(p)
    lb1 = max(s[j] + p[j] for j in range(n))
    lb2 = max(r[j] + p[j] for j in range(n))
    lb3 = sum(s[j] + p[j] for j in range(n)) / m
    ps = sorted(p, reverse=True)
    lb4 = ps[m - 1] + ps[m] if n > m else 0
    return {"LB1": lb1, "LB2": lb2, "LB3": lb3, "LB4": lb4,
            "LB": max(lb1, lb2, lb3, lb4)}


def rpd(c, lb):
    """Desvio relativo percentual em relação ao limitante inferior."""
    return 100.0 * (c - lb) / lb


# ----------------------------------------------------------------- solução inicial
def initial_solution(p, s, r, m):
    """Ordena por r_j/(p_j+s_j) crescente e aloca na máquina de menor carga."""
    order = sorted(range(len(p)), key=lambda j: r[j] / (p[j] + s[j]))
    sol = [[] for _ in range(m)]
    loads = [0] * m
    for j in order:
        k = min(range(m), key=loads.__getitem__)
        sol[k].append(j)
        loads[k] = machine_completion(sol[k], p, s, r)
    return sol


# ----------------------------------------------------------------- perturbações
def _copy(sol):
    return [seq[:] for seq in sol]


def ps1(sol, rng):
    """Troca de tarefas adjacentes na mesma máquina."""
    cand = [k for k, q in enumerate(sol) if len(q) >= 2]
    if not cand:
        return None
    k = rng.choice(cand)
    i = rng.randrange(len(sol[k]) - 1)
    new = _copy(sol)
    new[k][i], new[k][i + 1] = new[k][i + 1], new[k][i]
    return new


def ps2(sol, rng):
    """Troca de duas tarefas quaisquer da mesma máquina."""
    cand = [k for k, q in enumerate(sol) if len(q) >= 2]
    if not cand:
        return None
    k = rng.choice(cand)
    i, j = rng.sample(range(len(sol[k])), 2)
    new = _copy(sol)
    new[k][i], new[k][j] = new[k][j], new[k][i]
    return new


def ps3(sol, rng):
    """Reinserção de uma tarefa em outra posição da mesma máquina."""
    cand = [k for k, q in enumerate(sol) if len(q) >= 2]
    if not cand:
        return None
    k = rng.choice(cand)
    new = _copy(sol)
    i = rng.randrange(len(new[k]))
    job = new[k].pop(i)
    pos = rng.randrange(len(new[k]) + 1)
    new[k].insert(pos, job)
    return new


def ps4(sol, rng):
    """Troca de uma tarefa entre duas máquinas diferentes."""
    cand = [k for k, q in enumerate(sol) if q]
    if len(cand) < 2:
        return None
    a, b = rng.sample(cand, 2)
    new = _copy(sol)
    i, j = rng.randrange(len(new[a])), rng.randrange(len(new[b]))
    new[a][i], new[b][j] = new[b][j], new[a][i]
    return new


def ps5(sol, rng):
    """Realocação de uma tarefa para outra máquina."""
    cand = [k for k, q in enumerate(sol) if q]
    if not cand or len(sol) < 2:
        return None
    a = rng.choice(cand)
    b = rng.choice([k for k in range(len(sol)) if k != a])
    new = _copy(sol)
    job = new[a].pop(rng.randrange(len(new[a])))
    new[b].insert(rng.randrange(len(new[b]) + 1), job)
    return new


def ps6(sol, rng):
    """Realocação de uma subsequência (>= 2 tarefas) para outra máquina."""
    cand = [k for k, q in enumerate(sol) if len(q) >= 2]
    if not cand or len(sol) < 2:
        return None
    a = rng.choice(cand)
    b = rng.choice([k for k in range(len(sol)) if k != a])
    new = _copy(sol)
    i = rng.randrange(len(new[a]) - 1)
    size = rng.randint(2, len(new[a]) - i)
    sub = new[a][i:i + size]
    del new[a][i:i + size]
    pos = rng.randrange(len(new[b]) + 1)
    new[b][pos:pos] = sub
    return new


PERTURBATIONS = {"PS1": ps1, "PS2": ps2, "PS3": ps3, "PS4": ps4, "PS5": ps5, "PS6": ps6}


# ----------------------------------------------------------------- etapa de melhoria
def balance_step(sol, p, s, r):
    """Passo 5: se as cargas estão desequilibradas, move a última tarefa da máquina
    mais carregada para a menos carregada, enquanto isso melhorar o makespan."""
    sol = _copy(sol)
    cmax = makespan(sol, p, s, r)
    while True:
        loads = [machine_completion(q, p, s, r) for q in sol]
        hi, lo = loads.index(max(loads)), loads.index(min(loads))
        if hi == lo or not sol[hi]:
            break
        ju = sol[hi][-1]
        if loads[hi] - loads[lo] <= p[ju] + s[ju]:
            break
        new = _copy(sol)
        new[lo].append(new[hi].pop())
        c_new = makespan(new, p, s, r)
        if c_new < cmax:
            sol, cmax = new, c_new
        else:
            break
    return sol, cmax


# ----------------------------------------------------------------- Simulated Annealing
def simulated_annealing(p, s, r, m, ps="PS4", t_init=60.0, t_final=0.01,
                        cooling=0.85, iters_per_temp=1, seed=0, improve=True):
    """Parâmetros padrão iguais aos do exemplo numérico da dissertação (Ti=60,
    Tf=0.01, r=0.85). ps pode ser PS1..PS6 ou 'random' (esquema sorteado)."""
    rng = random.Random(seed)
    cur = initial_solution(p, s, r, m)
    cur_c = makespan(cur, p, s, r)
    best, best_c = _copy(cur), cur_c
    t = t_init
    while t > t_final:
        for _ in range(iters_per_temp):
            fn = rng.choice(list(PERTURBATIONS.values())) if ps == "random" \
                else PERTURBATIONS[ps]
            cand = fn(cur, rng)
            if cand is None:
                continue
            c = makespan(cand, p, s, r)
            delta = c - cur_c
            if delta <= 0 or rng.random() <= math.exp(-delta / t):
                cur, cur_c = cand, c
                if cur_c < best_c:
                    best, best_c = _copy(cur), cur_c
        t *= cooling
    if improve:
        best, best_c = balance_step(best, p, s, r)
    return best, best_c


# ----------------------------------------------------------------- instâncias
def random_instance(n, r_range, s_range=(1, 49), p_range=(1, 99), seed=0):
    rng = random.Random(seed)
    p = [rng.randint(*p_range) for _ in range(n)]
    s = [rng.randint(*s_range) for _ in range(n)]
    r = [rng.randint(*r_range) for _ in range(n)]
    return p, s, r
