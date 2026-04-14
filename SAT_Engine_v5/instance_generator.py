import random
from sat_backend import SATInstance

def random_sat(n_vars, m_clauses):
    inst = SATInstance()
    inst.n_vars = n_vars
    inst.clauses = []

    for _ in range(m_clauses):
        clause = []
        for _ in range(3):
            v = random.randint(1, n_vars)
            if random.random() < 0.5:
                v = -v
            clause.append(v)
        inst.clauses.append(clause)
    return inst
