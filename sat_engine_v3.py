import random
import time
import numpy as np
import matplotlib.pyplot as plt

# ===========================================
#  Generador de instancias 3-SAT
# ===========================================
def random_3sat(n_vars, n_clauses):
    formula = []
    for _ in range(n_clauses):
        clause = []
        for _ in range(3):
            v = random.randint(1, n_vars)
            if random.random() < 0.5:
                v = -v
            clause.append(v)
        formula.append(clause)
    return formula

# ===========================================
#  Verificador SAT (polinomial)
# ===========================================
def is_satisfied(formula, assignment):
    for clause in formula:
        if not any((lit > 0 and assignment[abs(lit)]) or
                   (lit < 0 and not assignment[abs(lit)]) for lit in clause):
            return False
    return True

# ===========================================
#  GSAT / WalkSAT (heurísticos)
# ===========================================
def gsat(formula, n_vars, max_steps=2000):
    assign = {i: random.choice([True, False]) for i in range(1, n_vars+1)}

    for step in range(max_steps):
        if is_satisfied(formula, assign):
            return True, step

        best_var = None
        best_score = -1
        for v in range(1, n_vars+1):
            assign[v] = not assign[v]
            score = sum(is_clause_satisfied(cl, assign) for cl in formula)
            assign[v] = not assign[v]

            if score > best_score:
                best_score = score
                best_var = v

        assign[best_var] = not assign[best_var]

    return False, None

def is_clause_satisfied(clause, assignment):
    return any((lit > 0 and assignment[abs(lit)]) or
               (lit < 0 and not assignment[abs(lit)]) for lit in clause)

def walksat(formula, n_vars, max_steps=2000, p=0.5):
    assign = {i: random.choice([True, False]) for i in range(1, n_vars+1)}

    for step in range(max_steps):
        if is_satisfied(formula, assign):
            return True, step

        unsat = [cl for cl in formula if not is_clause_satisfied(cl, assign)]
        clause = random.choice(unsat)

        if random.random() < p:
            v = abs(random.choice(clause))
        else:
            best_v = None
            best_score = -1
            for lit in clause:
                v = abs(lit)
                assign[v] = not assign[v]
                score = sum(is_clause_satisfied(cl, assign) for cl in formula)
                assign[v] = not assign[v]
                if score > best_score:
                    best_score = score
                    best_v = v
            v = best_v

        assign[v] = not assign[v]

    return False, None

# ===========================================
#  SAT Engine v3 — Phase Transition Analyzer
# ===========================================
def run_phase_transition(n_vars=40, trials=20):
    ratios = np.linspace(1.0, 7.0, 25)
    sat_prob = []
    avg_time = []
    avg_steps = []

    print("\n==============================")
    print("     SAT Engine v3 START")
    print("==============================\n")

    for ratio in ratios:
        m = int(ratio * n_vars)

        sats = 0
        time_total = 0
        steps_total = 0
        attempts = 0

        for _ in range(trials):
            F = random_3sat(n_vars, m)

            t0 = time.time()
            result_gsat, steps = gsat(F, n_vars)
            t1 = time.time()

            attempts += 1
            if result_gsat:
                sats += 1
                steps_total += steps
            time_total += (t1 - t0)

        sat_prob.append(sats / attempts)
        avg_time.append(time_total / attempts)
        avg_steps.append(steps_total / attempts if sats > 0 else None)

        print(f"m/n={ratio:.2f} | SAT prob={sat_prob[-1]:.2f} | time={avg_time[-1]:.4f}s")

    # -----------------------------------------
    #       GRAFICAR RESULTADOS
    # -----------------------------------------
    plt.figure(figsize=(13,5))

    plt.subplot(1,3,1)
    plt.plot(ratios, sat_prob, "bo-")
    plt.title("Probabilidad SAT vs m/n")
    plt.xlabel("m/n")
    plt.ylabel("Probabilidad SAT")

    plt.subplot(1,3,2)
    plt.plot(ratios, avg_time, "ro-")
    plt.title("Tiempo promedio vs m/n")
    plt.xlabel("m/n")
    plt.ylabel("Tiempo (s)")

    plt.subplot(1,3,3)
    plt.plot(ratios, [s if s else 0 for s in avg_steps], "go-")
    plt.title("Pasos GSAT vs m/n")
    plt.xlabel("m/n")

    plt.tight_layout()
    plt.show()

    print("\n==============================")
    print("     SAT Engine v3 END")
    print("==============================\n")


if __name__ == "__main__":
    run_phase_transition()
