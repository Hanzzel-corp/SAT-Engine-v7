import numpy as np
import optuna
import json
import csv

def E_hodge(s):
    return abs(s[2] - (s[1] * 0.7)) + abs(s[1] - (s[0] * 0.5))

def E_ns(s):
    return abs((s[1] - s[0]) + (s[2] - s[1])) + abs(s[3] * 0.4)

def E_ym(s):
    return abs((s[1] - s[0]) - 0.25)

def E_bsd(s):
    return abs(s[3] - (s[2]**2 - s[1]))

def E_zeta(s):
    return 0.5 * abs(s[0]) + abs(abs(s[1]) - abs(s[2]))

def E_pnp(s):
    return abs(s[1] * s[2] - s[3])

def E_total(s):
    return (
        E_hodge(s) +
        E_ns(s) +
        E_ym(s) +
        E_bsd(s) +
        E_zeta(s) +
        E_pnp(s)
    )

def objective(trial):
    s = np.array([
        trial.suggest_float("C0", -1, 1),
        trial.suggest_float("C1", -1, 1),
        trial.suggest_float("C2", -1, 1),
        trial.suggest_float("C3", -1, 1),
        trial.suggest_float("phi", 0, 1),
        trial.suggest_float("alpha", 0, 1),
        trial.suggest_float("beta", 0, 1),
    ])
    e = E_total(s)
    print(
        f"[Iter] ω={s}  "
        f"E_h={E_hodge(s):.4f}  "
        f"E_ns={E_ns(s):.4f}  "
        f"E_ym={E_ym(s):.4f}  "
        f"E_bsd={E_bsd(s):.4f}  "
        f"E_z={E_zeta(s):.4f}  "
        f"E_pnp={E_pnp(s):.4f}  "
        f"E_tot={e:.4f}"
    )
    with open("historial_optuna.csv","a",newline="") as f:
        w = csv.writer(f)
        w.writerow([*s, E_hodge(s), E_ns(s), E_ym(s), E_bsd(s), E_zeta(s), E_pnp(s), e])
    return e

study = optuna.create_study(direction="minimize", sampler=optuna.samplers.RandomSampler())
with open("historial_optuna.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["C0","C1","C2","C3","phi","alpha","beta",
                "E_hodge","E_ns","E_ym","E_bsd","E_zeta","E_pnp","E_total"])

study.optimize(objective, n_trials=300)

best = study.best_params
s = np.array([
    best["C0"], best["C1"], best["C2"], best["C3"],
    best["phi"], best["alpha"], best["beta"]
])

print("\nEstado Final Optimizado:\n", s)
print("\nE_hodge:", E_hodge(s))
print("E_ns:", E_ns(s))
print("E_ym:", E_ym(s))
print("E_bsd:", E_bsd(s))
print("E_zeta:", E_zeta(s))
print("E_pnp:", E_pnp(s))
print("E_total:", E_total(s))

with open("solucion_milenio.json","w") as f:
    json.dump({
        "state": best,
        "E_hodge": float(E_hodge(s)),
        "E_ns": float(E_ns(s)),
        "E_ym": float(E_ym(s)),
        "E_bsd": float(E_bsd(s)),
        "E_zeta": float(E_zeta(s)),
        "E_pnp": float(E_pnp(s)),
        "E_total": float(E_total(s))
    }, f, indent=4)

with open("solucion_milenio.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["C0","C1","C2","C3","phi","alpha","beta","E_total"])
    w.writerow([*s, E_total(s)])

def ascii_plot(s):
    C0, C1, C2, C3 = s[0], s[1], s[2], s[3]
    a = int((C3 - (-1)) / 2 * 20)
    b = int((C2 - (-1)) / 2 * 20)
    c = int((C1 - (-1)) / 2 * 20)
    d = int((C0 - (-1)) / 2 * 20)
    a = max(0, min(29, a))
    b = max(0, min(29, b))
    c = max(0, min(29, c))
    d = max(0, min(29, d))
    grid = [[" "]*30 for _ in range(25)]
    grid[2][a] = "3"
    grid[6][b] = "2"
    grid[12][c] = "1"
    grid[20][d] = "0"
    print("\nASCII Geometry:\n")
    for row in grid:
        print("".join(row))

ascii_plot(s)

