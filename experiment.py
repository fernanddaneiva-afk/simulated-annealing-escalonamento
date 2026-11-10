"""Mini-experimento: RPD médio em relação ao limitante inferior, por esquema de
perturbação, em instâncias sintéticas geradas como na dissertação
(p ~ U(1,99), s ~ U(1,49), r ~ U(1,49) / U(1,99) / U(50,149))."""
import statistics as st
import time

from sa_scheduling import (PERTURBATIONS, initial_solution, lower_bounds,
                           makespan, random_instance, rpd, simulated_annealing)

NS, MS = (10, 30, 100), (2, 5)
R_RANGES = [(1, 49), (1, 99), (50, 149)]
REPS = 10


def main():
    res = {k: [] for k in ["SI", *PERTURBATIONS]}
    t0 = time.time()
    for n in NS:
        for m in MS:
            for rr in R_RANGES:
                for rep in range(REPS):
                    p, s, r = random_instance(n, rr, seed=hash((n, m, rr, rep)) % 10**6)
                    lb = lower_bounds(p, s, r, m)["LB"]
                    res["SI"].append(rpd(makespan(initial_solution(p, s, r, m), p, s, r), lb))
                    for name in PERTURBATIONS:
                        _, c = simulated_annealing(p, s, r, m, ps=name, seed=rep)
                        res[name].append(rpd(c, lb))
    print(f"{len(res['SI'])} instâncias, {time.time() - t0:.1f}s")
    print("método  RPD médio vs LB (%)")
    for k, v in res.items():
        print(f"{k:<6}  {st.mean(v):6.2f}")


if __name__ == "__main__":
    main()
