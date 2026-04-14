import random
import time
from statistics import median
from sat_backend import SATInstance, solve_parallel

def random_sat(n, m):
    clauses = []
    for _ in range(m):
        C = []
        for _ in range(3):
            v = random.randint(1, n)
            if random.random() < 0.5:
                v = -v
            C.append(v)
        clauses.append(C)
    return SATInstance(n, clauses)

def sweep():
    ratios = [1 + 0.1 * i for i in range(40)]
    for r in ratios:
        n = 40
        m = int(n*r)

        times = []
        successes = 0

        for _ in range(10):
            inst = random_sat(n, m)
            t0 = time.time()
            res = solve_parallel(inst, 50000, 8)
            t1 = time.time()
            if res["found"]:
                successes += 1
            times.append(t1-t0)

        print(f"m/n={r:.2f} | SAT_rate={successes/10:.2f} | avg={sum(times)/10:.3f}s")

if __name__ == "__main__":
    print("==============================")
    print("     SAT Engine v7 START")
    print("==============================")
    sweep()
    print("==============================")
    print("     SAT Engine v7 END")
    print("==============================")



