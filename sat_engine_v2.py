import random
import time

# -------------------------------------------------------
#  Utilities
# -------------------------------------------------------

def generate_sat_instance(n_vars, n_clauses, k=3):
    """Generate random k-SAT instance."""
    clauses = []
    for _ in range(n_clauses):
        clause = []
        for _ in range(k):
            var = random.randint(1, n_vars)
            if random.random() < 0.5:
                var = -var
            clause.append(var)
        clauses.append(clause)
    return clauses

def evaluate_clause(clause, assignment):
    return any((lit > 0 and assignment[abs(lit)]) or
               (lit < 0 and not assignment[abs(lit)])
               for lit in clause)

def count_satisfied(clauses, assignment):
    return sum(1 for c in clauses if evaluate_clause(c, assignment))

# -------------------------------------------------------
#  GSAT
# -------------------------------------------------------

def gsat(clauses, n_vars, max_steps=500):
    assignment = {i: bool(random.getrandbits(1)) for i in range(1, n_vars+1)}

    for step in range(max_steps):
        sat = count_satisfied(clauses, assignment)
        if sat == len(clauses):
            return assignment, step

        best_var = None
        best_gain = -1

        for v in range(1, n_vars+1):
            assignment[v] = not assignment[v]   # flip
            new_sat = count_satisfied(clauses, assignment)
            gain = new_sat - sat
            assignment[v] = not assignment[v]   # undo flip

            if gain > best_gain:
                best_gain = gain
                best_var = v

        assignment[best_var] = not assignment[best_var]   # flip best var

    return None, None   # failed

# -------------------------------------------------------
#  WalkSAT
# -------------------------------------------------------

def walksat(clauses, n_vars, max_steps=5000, p=0.5):
    assignment = {i: bool(random.getrandbits(1)) for i in range(1, n_vars+1)}

    for step in range(max_steps):
        sat_clauses = [c for c in clauses if evaluate_clause(c, assignment)]
        if len(sat_clauses) == len(clauses):
            return assignment, step

        false_clauses = [c for c in clauses if not evaluate_clause(c, assignment)]
        clause = random.choice(false_clauses)

        if random.random() < p:
            # random flip inside the clause
            var = abs(random.choice(clause))
            assignment[var] = not assignment[var]
        else:
            # flip variable causing least conflicts
            best_var = None
            best_cost = 1e18

            for lit in clause:
                v = abs(lit)
                assignment[v] = not assignment[v]
                cost = len(clauses) - count_satisfied(clauses, assignment)
                assignment[v] = not assignment[v]

                if cost < best_cost:
                    best_cost = cost
                    best_var = v

            assignment[best_var] = not assignment[best_var]

    return None, None

# -------------------------------------------------------
#  SAT Engine v2 Runner
# -------------------------------------------------------

def run_engine():
    print("\n==============================")
    print("     SAT Engine v2 START")
    print("==============================\n")

    for _ in range(3):
        n_vars = 30
        n_clauses = random.randint(120, 180)  # phase transition area

        clauses = generate_sat_instance(n_vars, n_clauses)
        print(f"Instancia: {n_vars} vars, {n_clauses} cláusulas")

        # GSAT
        t0 = time.time()
        sol_gsat, steps_gsat = gsat(clauses, n_vars)
        t1 = time.time()

        # WalkSAT
        t2 = time.time()
        sol_ws, steps_ws = walksat(clauses, n_vars)
        t3 = time.time()

        print(f" GSAT   → {'SAT' if sol_gsat else 'FAIL'}  | "
              f"steps={steps_gsat} | time={t1-t0:.5f}s")

        print(f" WalkSAT → {'SAT' if sol_ws else 'FAIL'} | "
              f"steps={steps_ws} | time={t3-t2:.5f}s\n")

    print("==============================")
    print("     SAT Engine v2 END")
    print("==============================\n")


if __name__ == "__main__":
    run_engine()
