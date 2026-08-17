# ============================================================
# CLAUSE 22.4.1 — YIELD STRESS VARIATION WITH TEMPERATURE
# ============================================================

def yield_stress_temperature(f_y_20, T):

    reduction_factor = (905 - T) / 690
    reduction_factor = min(reduction_factor, 1.0)

    return reduction_factor * f_y_20


print("===== CLAUSE 22.4.1 TEST =====")

fy_20 = 250

temperatures = [20, 400, 600, 800]

for T in temperatures:
    fy_T = yield_stress_temperature(fy_20, T)
    print(f"Yield stress at {T}°C = {fy_T:.3f} MPa")