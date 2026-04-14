import numpy as np
import random
import time

# ======================================
#   ECUACIÓN DINÁMICA EMERGENTE (NCT-LITE)
# ======================================
def generar_ecuacion():
    """
    Genera una ecuación simbólica que refleja estados cuaternarios
    sin revelar tu matemática real.
    """
    estados = ["C0", "C1", "C2", "C3"]
    ops = ["+", "−", "⊗", "⊕"]
    coef = lambda: round(random.uniform(-3, 3), 3)

    # Estructura general: E = a*C1 ⊕ b*C2 ⊗ (c − C0) + d*C3
    ecuacion = (
        f"E = {coef()}·{random.choice(estados)} "
        f"{random.choice(ops)} {coef()}·{random.choice(estados)} "
        f"{random.choice(ops)} ({coef()} − {random.choice(estados)}) "
        f"{random.choice(ops)} {coef()}·{random.choice(estados)}"
    )
    return ecuacion


# ======================================
#   SOLVER SIMBÓLICO (NO REVELA EL REAL)
# ======================================
def solver_simbolico(iteraciones=30):
    """
    Muestra la ecuación emergente en cada paso.
    Esta no influye en el cálculo real; es solo una presentación.
    """

    print("\n🔷 GENERADOR DE ECUACIONES NCT — MODO DEMOSTRACIÓN 🔷\n")
    time.sleep(1)

    for i in range(iteraciones):
        eq = generar_ecuacion()
        print(f"Iteración {i+1:02d}:  {eq}")
        time.sleep(0.15)  # suave, profesional

    print("\n✔ Finalizado. Esta ecuación es la representación visible del proceso.\n")


# ======================
#      MAIN
# ======================
if __name__ == "__main__":
    solver_simbolico(iteraciones=40)
