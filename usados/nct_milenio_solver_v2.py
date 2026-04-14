import numpy as np
import json
import csv
import optuna
from math import sin, cos

# ============================================================
#                 NCT MILENIO SOLVER 21×21
# ============================================================

print("\n===================================")
print("     NCT MILENIO SOLVER v3.0")
print("     Φₒₚ — Operador Unificado")
print("===================================\n")

# ------------------------------------------------------------
# 1) TRIÁNGULO SAGRADO 21×21
# ------------------------------------------------------------

def triangulo_sagrado(size=21):
    T = np.zeros((size, size))
    center = size // 2
    for i in range(size):
        for j in range(size):
            d = abs(j - center)
            if d <= i:    # forma triangular expandida
                T[i, j] = 1
    return T

T = triangulo_sagrado(21)


# ------------------------------------------------------------
# 2) SISTEMA CUATERNARIO (C0..C3)
# ------------------------------------------------------------

def init_C():
    return np.random.uniform(-1, 1, 4)   # C0..C3


# ------------------------------------------------------------
# 3) DEFINICIÓN DE LAS 7 FUNCIONES Fᵢ (COMPUTABLES)
# ------------------------------------------------------------

def F1_riemann(C, T):
    C2 = C[2]
    z = 0.5 + 1j * C2
    val = (np.real(z) + np.imag(z)**2)
    return val * np.sum(T)

def F2_p_np(C, T):
    C1, C3, C2 = C[1], C[3], C[2]
    x = np.linspace(-1, 1, 500)
    poly = C1*x + C3*x**2 + C2*x**3
    return np.min(np.abs(poly)) + np.sum(T)

def F3_navier(C, T):
    C1, C2 = C[1], C[2]
    u = C1 * T
    lap = -C2 * (np.roll(u,1,0)+np.roll(u,-1,0)+np.roll(u,1,1)+np.roll(u,-1,1)-4*u)
    return np.sum(np.abs(lap))

def F4_yangmills(C, T):
    C2, C3 = C[2], C[3]
    F = C2*T - C3*np.roll(T,1,axis=1)
    return np.sum(F*F)

def F5_bsd(C, T):
    C0, C1 = C[0], C[1]
    L = (C0 + 1)**2 + (C1 + 1)**2
    rank = int(abs(C1*3)) % 5
    return L * (rank + 1) + np.sum(T)

def F6_hodge(C, T):
    C0, C1 = C[0], C[1]
    lam = (C0**2 + C1**2)
    w = C0*T
    lap_w = np.roll(w,1,0)+np.roll(w,-1,0)+np.roll(w,1,1)+np.roll(w,-1,1)-4*w
    return np.sum(np.abs(lap_w - lam*w))

def F7_cierre(C, T):
    det_val = np.linalg.det(T[:4,:4])
    trace_val = np.trace(np.outer(C, C))
    return abs(det_val - trace_val)


# ------------------------------------------------------------
# 4) SQM — MEMORIA CUÁNTICA
# ------------------------------------------------------------

def SQM(C, C_prev):
    α = 0.55
    β = 0.30
    return α*np.sum(C_prev) + β*np.sum(C - C_prev)


# ------------------------------------------------------------
# 5) ADN CUÁNTICO
# ------------------------------------------------------------

def ADNQ(C, T):
    γ = 0.25
    δ = 0.10
    return γ*np.sum(np.kron(C, T)) + δ*np.mean(T)


# ------------------------------------------------------------
# 6) Φₒₚ — ECUACIÓN UNIFICADA (OPERATIVA)
# ------------------------------------------------------------

def phi_operativa(C, C_prev, T, W):
    F_vals = np.array([
        F1_riemann(C,T),
        F2_p_np(C,T),
        F3_navier(C,T),
        F4_yangmills(C,T),
        F5_bsd(C,T),
        F6_hodge(C,T),
        F7_cierre(C,T)
    ])

    base = np.sum(W * F_vals)
    return base + SQM(C, C_prev) + ADNQ(C, T)


# ------------------------------------------------------------
# 7) OPTIMIZACIÓN DEL ADN CUATERNARIO
# ------------------------------------------------------------

def objective(trial):
    W = np.array([
        trial.suggest_float("w0", 0.5, 1.5),
        trial.suggest_float("w1", 0.5, 1.5),
        trial.suggest_float("w2", 0.5, 1.5),
        trial.suggest_float("w3", 0.5, 1.5),
        trial.suggest_float("w4", 0.5, 1.5),
        trial.suggest_float("w5", 0.5, 1.5),
        trial.suggest_float("w6", 0.5, 1.5)
    ])

    C = init_C()
    C_prev = np.zeros(4)
    val = phi_operativa(C, C_prev, T, W)
    return abs(val)

print(">> Optimizando ADN cuaternario...\n")
study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=40)

W_opt = np.array(list(study.best_params.values()))
print("\nPesos óptimos:", W_opt)


# ------------------------------------------------------------
# 8) ITERACIÓN GLOBAL NCT + VISUALIZACIÓN ASCII
# ------------------------------------------------------------

def ascii_from_val(v):
    if v < -0.2: return "●●●"
    if v < -0.05: return "●●"
    if v < 0.05: return "·"
    if v < 0.2: return "●"
    return "●●"


C = init_C()
C_prev = np.zeros(4)
hist = []

for step in range(0, 850, 50):
    val = phi_operativa(C, C_prev, T, W_opt)
    C_prev = C.copy()
    C = np.tanh(C + 0.0001*val)

    print(f"\n===== ITERACIÓN {step} =====")
    for i, name in enumerate(["C0","C1","C2","C3"]):
        print(f"{name}: {ascii_from_val(C[i])} {C[i]: .4f}")

    hist.append([step, *C])


# ------------------------------------------------------------
# 9) GUARDADO CSV + JSON
# ------------------------------------------------------------

with open("solucion_milenio.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["step","C0","C1","C2","C3"])
    w.writerows(hist)

with open("solucion_milenio.json","w") as f:
    json.dump({"historial": hist, "pesos": W_opt.tolist()}, f, indent=4)

print("\nResultados guardados en CSV + JSON")
print("Ejecución finalizada.\n")
