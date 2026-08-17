import math


# G-2.3.1
def test_g_2_3_1(A_sn, f_usa, gamma_MSV, low_ductility=False):
    V_das = (0.5 * A_sn * f_usa) / gamma_MSV

    if low_ductility:
        V_das *= 0.8

    return V_das


# G-2.3.2
def test_g_2_3_2_moment(Vu, lever_arm, alpha_M):
    Mu = Vu * lever_arm / alpha_M
    return Mu


def test_g_2_3_2_Md0(Z_ea, f_usa):
    Md0 = 1.2 * Z_ea * f_usa
    return Md0


def test_g_2_3_2_Mds(Md0, Tu, Tdsa):
    Mds = Md0 * (1 - Tu / Tdsa)
    return Mds


def test_g_2_3_2_shear(alpha_M, Mds, lever_arm, gamma_MSV):
    V_das = (alpha_M * Mds) / (lever_arm * gamma_MSV)
    return V_das


# G-2.3.3
def test_g_2_3_3(hef, Tdca):
    if hef < 60:
        k = 1
    else:
        k = 2

    V_dcp = k * Tdca
    return V_dcp


# G-2.3.4
def test_g_2_3_4(
        da, hef, fck, c1, gamma_MCV,
        A_cv, A0_cv,
        psi_sv, psi_av, psi_ecv, psi_ucrv, psi_hv):

    V_dac = (
        0.45
        * math.sqrt(da)
        * (hef / da) ** 0.2
        * math.sqrt(fck)
        * c1 ** 1.5
        / gamma_MCV
        * (A_cv / A0_cv)
        * psi_sv
        * psi_av
        * psi_ecv
        * psi_ucrv
        * psi_hv
    )

    return V_dac


# ---------------- TEST VALUES ----------------

print("G-2.3.1 Vdas =",
      test_g_2_3_1(500, 400, 1.25), "N")

Mu = test_g_2_3_2_moment(10000, 100, 2.0)
print("G-2.3.2 Mu =", Mu, "N-mm")

Md0 = test_g_2_3_2_Md0(1000, 400)
print("G-2.3.2 Md0 =", Md0, "N-mm")

Mds = test_g_2_3_2_Mds(Md0, 5000, 20000)
print("G-2.3.2 Mds =", Mds, "N-mm")

V_das = test_g_2_3_2_shear(2.0, Mds, 100, 1.25)
print("G-2.3.2 Vdas =", V_das, "N")

print("G-2.3.3 Vdcp =",
      test_g_2_3_3(80, 10000), "N")

print("G-2.3.4 Vdac =",
      test_g_2_3_4(
          20, 100, 25, 100, 1.5,
          45000, 30000,
          1.0, 1.0, 1.0, 1.0, 1.0
      ), "N")