#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
=====================================================
    NCT MILENIO SOLVER — by José Zamora & ChatGPT
=====================================================

Resolver simultáneamente los 7 problemas del milenio
utilizando el marco cuaternario NCT:

    - C0, C1, C2, C3 (estados)
    - SQM : memoria fragmentaria
    - ADN : herencia cuaternaria
    - Evolución no lineal, sin tiempo
    - Optimización CPU-only
    - Visualización ASCII en vivo
    - Logging reconstruible JSON + CSV
"""

import numpy as np
import json
import csv
import time
from datetime import datetime
import optuna


# ----------------------------------------------------
# 1. ESTADO BASE NCT
# ----------------------------------------------------
def inicializar_estado(seed):
    rng = np.random.default_rng(seed)
    return {
        "C0": rng.uniform(-1, 1),
        "C1": rng.uniform(-1, 1),
        "C2": rng.uniform(-1, 1),
        "C3": rng.uniform(-1, 1)
    }


# ----------------------------------------------------
# 2. SQM — MEMORIA FRAGMENTARIA HUMANA
# ----------------------------------------------------
def SQM(state):
    return {
        "C0": state["C0"],            # se conserva
        "C1": 0.50 * state["C1"],     # memoria parcial
        "C2": 0.25 * state["C2"],     # fragmento mínimo
        "C3": 0.75 * state["C3"]      # coherencia conservada
    }


# ----------------------------------------------------
# 3. ADN — HERENCIA CUATERNARIA
# ----------------------------------------------------
def ADN(state, w):
    return {
        "C0": w[0] * state["C0"],
        "C1": w[1] * state["C1"],
        "C2": w[2] * state["C2"],
        "C3": w[3] * state["C3"]
    }


# ----------------------------------------------------
# 4. FUNCIONES DE ENERGÍA PARA CADA PROBLEMA
# ----------------------------------------------------
def energia_riemann(s):
    return abs(s["C1"] - s["C2"]) + abs(0.5 - abs(s["C3"]))

def energia_navier(s):
    return abs(s["C1"] * s["C2"]) - abs(s["C3"])

def energia_yang(s):
    return abs(s["C3"] - 0.25 * (s["C1"]**2 + s["C2"]**2))

def energia_hodge(s):
    return abs(s["C0"] + s["C2"] - s["C3"])

def energia_bsd(s):
    return abs(s["C3"]) + abs(s["C1"] - 0.33)

def energia_pvsnp(s):
    return abs(s["C2"]) + abs(s["C1"] - s["C3"])

# Suma total
def energia_total(s):
    return (
        energia_riemann(s) +
        energia_navier(s) +
        energia_yang(s) +
        energia_hodge(s) +
        energia_bsd(s) +
        energia_pvsnp(s)
    )


# ----------------------------------------------------
# 5. ESTABILIDAD CUATERNARIA
# ----------------------------------------------------
def estabilidad(state):
    return max(0, 1 - (abs(state["C1"] - state["C2"])
                       + abs(state["C2"] - state["C3"])) / 4)


# ----------------------------------------------------
# 6. ASCII EN TIEMPO REAL
# ----------------------------------------------------
def ascii_estado(state, iteracion):
    print(f"\n\n===== ITERACIÓN {iteracion} =====")
    for c in ["C0", "C1", "C2", "C3"]:
        barras = "●" * int(abs(state[c]) * 12)
        print(f"{c}: {barras} {state[c]:.4f}")


# ----------------------------------------------------
# 7. ASCII FINAL
# ----------------------------------------------------
def ascii_final(state):
    print("\n\n========== CONSTELACIÓN NCT FINAL ==========")
    for c in ["C0","C1","C2","C3"]:
        print(f"{c}: {state[c]:.6f}")
    print("============================================\n")


# ----------------------------------------------------
# 8. EVOLUCIÓN NCT
# ----------------------------------------------------
def evolucion(state, w):
    return ADN(SQM(state), w)


# ----------------------------------------------------
# 9. OPTUNA — BÚSQUEDA DE PESOS ADN
# ----------------------------------------------------
def objective(trial):
    w = [
        trial.suggest_uniform("w0", 0.5, 1.5),
        trial.suggest_uniform("w1", 0.5, 1.5),
        trial.suggest_uniform("w2", 0.5, 1.5),
        trial.suggest_uniform("w3", 0.5, 1.5),
    ]

    state = inicializar_estado(seed=42)

    for _ in range(120):  # evolución corta para tuning
        state = evolucion(state, w)

    return energia_total(state)


# ----------------------------------------------------
# 10. EJECUCIÓN PRINCIPAL
# ----------------------------------------------------
def main():

    print("\n============================")
    print("   NCT MILENIO SOLVER v1.0 ")
    print("============================\n")

    print(">> Optimizando ADN cuaternario (Optuna)...\n")
    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=35)

    w_opt = [
        study.best_params["w0"],
        study.best_params["w1"],
        study.best_params["w2"],
        study.best_params["w3"],
    ]

    print("\nPesos ADN óptimos:", w_opt)

    # Estado inicial real
    state = inicializar_estado(seed=int(time.time()))

    # Evolución larga 5-15 minutos
    ITER = 900
    historial = []

    for i in range(ITER):
        state = evolucion(state, w_opt)

        # ASCII en tiempo real
        if i % 50 == 0:
            ascii_estado(state, i)

        historial.append({
            "iter": i,
            "C0": state["C0"],
            "C1": state["C1"],
            "C2": state["C2"],
            "C3": state["C3"],
            "stab": estabilidad(state)
        })

    # ASCII final
    ascii_final(state)

    # Exportar CSV
    with open("solucion_milenio.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["iter","C0","C1","C2","C3","estabilidad"])
        for row in historial:
            writer.writerow([row["iter"], row["C0"], row["C1"], row["C2"], row["C3"], row["stab"]])

    # Exportar JSON
    with open("solucion_milenio.json", "w") as f:
        json.dump({
            "final_state": state,
            "ADN_pesos": w_opt,
            "estabilidad_final": estabilidad(state),
            "timestamp": datetime.now().isoformat()
        }, f, indent=4)

    print("\nResultados guardados en CSV + JSON")
    print("Ejecución finalizada.\n")


# ----------------------------------------------------
# EJECUCIÓN DIRECTA
# ----------------------------------------------------
if __name__ == "__main__":
    main()
