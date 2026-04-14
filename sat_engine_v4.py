import random
import time
import numpy as np

# ===============================================================
#   SAT ENGINE v4 — WalkSAT + GSAT + Restart + Noise Adaptativo
# ===============================================================

def generate_3sat_instance(n_vars, m_clauses):
    """Genera fórmula 3-SAT aleatoria."""
    F = []
    for _ in range(m_clauses):
        clause = []
        vars_ = random.sample(range(1, n_vars+1), 3)
        for v in vars_:
            lit = v if random.random() < 0.5 else -v
            clause.append(lit)
        F.append(clause)
    return F

def evaluate_clause(clause, assignment):
    """True si la cláusula está satisfecha."""
    return any(assignment[abs(l)] == (l > 0) for l in clause)

def evaluate_formula(F, assignment):
    """Número de cláusulas insatisfechas."""
    return sum(0 if evaluate_clause(c, assignment) else 1 for c in F)

# ---------------------------------------------------------------
#   GSAT Mejorado con Reinicios
# ---------------------------------------------------------------
def gsat_restart(F, n_vars, max_steps=5000, max_restarts=20):
    for r in range(max_restarts):
        assignment = {i: random.choice([True, False]) for i in range(1, n_vars+1)}
        for step in range(max_steps):
            unsat = [c for c in F if not evaluate_clause(c, assignment)]
            if not unsat:
                return True, step + r * max_steps

            var_flip = None
            best_score = 10**9
            for v in range(1, n_vars+1):
                assignment[v] = not assignment[v]
                score = evaluate_formula(F, assignment)
                assignment[v] = not assignment[v]

                if score < best_score:
                    best_score = score
                    var_flip = v

            assignment[var_flip] = not assignment[var_flip]

    return False, None

# ---------------------------------------------------------------
#   WalkSAT Avanzado (noise adaptativo estilo "novelty+")
# ---------------------------------------------------------------
def walksat_advanced(F, n_vars, max_steps=20000, p_noise=0.5):
    assignment = {i: random.choice([True, False]) for i in range(1, n_vars+1)}

    for step in range(max_steps):
        unsat = [c for c in F if not evaluate_clause(c, assignment)]
        if not unsat:
            return True, step

        clause = random.choice(unsat)
        if random.random() < p_noise:
            # ruido estocástico: flip aleatorio
            v = abs(random.choice(clause))
            assignment[v] = not assignment[v]
        else:
            # heurística novelty+: elegir flip que más reduce insatisfacción
            best_v = None
            best_score = 10**9
            for lit in clause:
                v = abs(lit)
                assignment[v] = not assignment[v]
                score = evaluate_formula(F, assignment)
                assignment[v] = not assignment[v]

                if score < best_score:
                    best_score = score
                    best_v = v

            assignment[best_v] = not assignment[best_v]

        # Ajuste dinámico de ruido
        if step % 500 == 0 and step > 0:
            p_noise = min(0.9, p_noise + 0.05)

    return False, None

# ---------------------------------------------------------------
#   Experimento principal: detección del umbral
# ---------------------------------------------------------------
def experiment():
    print("\n==============================")
    print("        SAT Engine v4")
    print("==============================\n")

    n_vars = 40
    ratios = np.linspace(1.0, 6.0, 20)

    for r in ratios:
        m = int(r * n_vars)

        sats = 0
        times = []
        REPS = 20

        for _ in range(REPS):
            F = generate_3sat_instance(n_vars, m)
            t0 = time.time()

            # dual solver: GSAT + WalkSAT Advanced
            res_g, s1 = gsat_restart(F, n_vars)
            if res_g:
                sats += 1
                times.append(time.time() - t0)
                continue

            res_w, s2 = walksat_advanced(F, n_vars)
            if res_w:
                sats += 1

            times.append(time.time() - t0)

        sat_prob = sats / REPS
        avg_time = sum(times) / len(times)

        print(f"m/n={r:.2f} | SAT={sat_prob:.2f} | time={avg_time:.3f}s")

    print("\n==============================")
    print("       SAT Engine v4 END")
    print("==============================\n")

if __name__ == "__main__":
    experiment()
