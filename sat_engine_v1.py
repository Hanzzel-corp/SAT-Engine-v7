import random
import time

# ============================================================
# 1) GENERADOR DE INSTANCIAS SAT EN CNF
# ============================================================

def generate_cnf(nvars, mclauses, k=3):
    """Genera una fórmula CNF aleatoria con m cláusulas de tamaño k."""
    clauses = []
    for _ in range(mclauses):
        clause = []
        for _ in range(k):
            var = random.randint(1, nvars)
            if random.random() < 0.5:
                var = -var
            clause.append(var)
        clauses.append(clause)
    return clauses

# ============================================================
# 2) VERIFICADOR (P)
# ============================================================

def verify(clauses, assignment):
    """Verifica si un assignment satisface todas las cláusulas."""
    for clause in clauses:
        ok = False
        for lit in clause:
            var = abs(lit)
            val = assignment[var-1]
            if (lit > 0 and val) or (lit < 0 and not val):
                ok = True
                break
        if not ok:
            return False
    return True

# ============================================================
# 3) SOLVER NP (BACKTRACKING)
# ============================================================

def solve_sat(clauses, nvars):
    assignment = [None]*nvars
    sol = backtrack(clauses, assignment, 0)
    return sol

def backtrack(clauses, assignment, idx):
    if idx == len(assignment):
        if verify(clauses, assignment):
            return assignment.copy()
        return None

    for v in [False, True]:
        assignment[idx] = v
        sol = backtrack(clauses, assignment, idx+1)
        if sol is not None:
            return sol
    assignment[idx] = None
    return None

# ============================================================
# 4) MEDICIÓN T(n)
# ============================================================

def experiment(nvars, ratio):
    m = int(ratio * nvars)
    clauses = generate_cnf(nvars, m)

    print(f"\n=== Instancia SAT ===")
    print(f"Variables: {nvars}, Cláusulas: {m}, Ratio m/n = {ratio:.2f}")

    # Verificación dummy
    test_assignment = [random.choice([True, False]) for _ in range(nvars)]
    t0 = time.time()
    verify(clauses, test_assignment)
    t_verify = time.time() - t0

    # Resolución
    t0 = time.time()
    solution = solve_sat(clauses, nvars)
    t_solve = time.time() - t0

    print(f"Tiempo verificación: {t_verify:.6f} s")
    print(f"Tiempo resolución  : {t_solve:.6f} s")
    print("Resultado:", "SAT" if solution else "UNSAT")

    return t_verify, t_solve

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("\n==============================")
    print("      SAT Engine v1 START")
    print("==============================\n")

    # Pruebas en tres zonas: subcrítica, crítica, supercrítica
    experiment(12, 3.0)     # FÁCIL
    experiment(12, 4.26)    # FASE CRÍTICA
    experiment(12, 6.0)     # MUY DIFÍCIL

    print("\n==============================")
    print("      SAT Engine v1 END")
    print("==============================\n")
