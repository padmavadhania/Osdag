import math


# Table 2(i)
def test_table2_i(width, thickness, fy):
    epsilon = math.sqrt(250 / fy)
    ratio = width / thickness

    if ratio <= 8.7 * epsilon:
        section_class = "Plastic"
    elif ratio <= 9.7 * epsilon:
        section_class = "Compact"
    elif ratio <= 13.6 * epsilon:
        section_class = "Semi-Compact"
    else:
        section_class = "Slender"

    return section_class, ratio


# Table 2(ii)
def test_table2_ii(depth, thickness, fy):
    epsilon = math.sqrt(250 / fy)
    ratio = depth / thickness

    if ratio <= 32 * epsilon:
        section_class = "Plastic"
    elif ratio <= 36.8 * epsilon:
        section_class = "Compact"
    elif ratio <= 40.7 * epsilon:
        section_class = "Semi-Compact"
    else:
        section_class = "Slender"

    return section_class, ratio


# Table 2(iii)
def test_table2_iii(width, depth, thickness, fy):
    epsilon = math.sqrt(250 / fy)

    b_t = width / thickness
    d_t = depth / thickness

    if b_t <= 8.7 * epsilon and d_t <= 8.7 * epsilon:
        section_class = "Plastic"
    elif b_t <= 9.7 * epsilon and d_t <= 9.7 * epsilon:
        section_class = "Compact"
    elif b_t <= 14.5 * epsilon and d_t <= 14.5 * epsilon:
        section_class = "Semi-Compact"
    else:
        section_class = "Slender"

    return section_class, b_t, d_t


# Table 2(iv)
def test_table2_iv(width, depth, thickness, fy):
    epsilon = math.sqrt(250 / fy)

    b_t = width / thickness
    d_t = depth / thickness
    bd_t = (width + depth) / thickness

    if (
        b_t <= 14.5 * epsilon
        and d_t <= 14.5 * epsilon
        and bd_t <= 22.3 * epsilon
    ):
        section_class = "Semi-Compact"
    else:
        section_class = "Slender"

    return section_class, b_t, d_t, bd_t


# Table 2(v)
def test_table2_v(depth, thickness, fy):
    epsilon = math.sqrt(250 / fy)
    ratio = depth / thickness

    if ratio <= 8.7 * epsilon:
        section_class = "Plastic"
    elif ratio <= 9.7 * epsilon:
        section_class = "Compact"
    elif ratio <= 14.5 * epsilon:
        section_class = "Semi-Compact"
    else:
        section_class = "Slender"

    return section_class, ratio


# Table 2(vi)
def test_table2_vi(outer_diameter, thickness, fy):
    epsilon = math.sqrt(250 / fy)
    ratio = outer_diameter / thickness

    if ratio <= 86 * epsilon ** 2:
        section_class = "Semi-Compact"
    else:
        section_class = "Slender"

    return section_class


# ---------------- TEST VALUES ----------------

print("Table 2(i)  =", test_table2_i(50, 6, 250))
print("Table 2(ii) =", test_table2_ii(300, 10, 250))
print("Table 2(iii) =", test_table2_iii(50, 50, 6, 250))
print("Table 2(iv) =", test_table2_iv(50, 50, 6, 250))
print("Table 2(v)  =", test_table2_v(50, 6, 250))
print("Table 2(vi) =", test_table2_vi(500, 10, 250))


class IS800_2025(object):
    """Perform calculations on steel design as per Draft IS 800:2025.

    Note:
        This module is under development. Only provisions that have
        been studied and verified from the Draft IS 800:2025 are
        implemented.
    """

    # ======================================================================
    """    SECTION 1     GENERAL    """
    # ======================================================================

    # ======================================================================
    """    SECTION 15     MEMBER DESIGN - BENDING    """
    # ======================================================================
    # ----------------------------------------------------------------------
    @staticmethod
    def cl_15_2_2_unsupported_beam_bending_strength(
            beta_b, Zp, fbd):
        """
        Calculate design bending strength of a laterally unsupported
        beam as per Cl. 15.2.2 of Draft IS 800:2025.

        Args:
            beta_b: Section modulus factor
            Zp: Plastic section modulus
            fbd: Design bending compressive stress

        Returns:
            Design bending strength Md
        """
        return beta_b * Zp * fbd
    @staticmethod
    def cl_15_2_2_unsupported_beam_bending_compressive_stress(
            chi_lt, fy, gamma_m0):
        """
        Calculate design bending compressive stress as per
        Cl. 15.2.2 of Draft IS 800:2025.

        Args:
            chi_lt: Bending stress reduction factor
            fy: Yield stress
            gamma_m0: Partial safety factor

        Returns:
            Design bending compressive stress fbd
        """
        return chi_lt * fy / gamma_m0
    @staticmethod
    def cl_15_2_2_unsupported_beam_bending_phi_lt(
            fm, lambda_lt, lambda_y, alpha_lt):
        """
        Calculate phi_LT as per Cl. 15.2.2 of Draft IS 800:2025.
        """
        phi_lt = 0.5 * (
            1
            + fm * (lambda_lt / lambda_y) ** 2
            * (
                alpha_lt * (lambda_lt - 0.2)
                + lambda_lt ** 2
            )
        )

        return phi_lt
    @staticmethod
    def cl_15_2_2_unsupported_beam_bending_stress_reduction_factor(
            phi_lt, lambda_lt, fm):
        """
        Calculate chi_LT, the bending stress reduction factor,
        as per Cl. 15.2.2 of Draft IS 800:2025.

        Args:
            phi_lt: Lateral torsional buckling parameter
            lambda_lt: Non-dimensional lateral torsional slenderness
            fm: Moment gradient effect parameter

        Returns:
            chi_LT
        """
        chi_lt = fm / (
            phi_lt
            + math.sqrt(phi_lt ** 2 - fm * lambda_lt ** 2)
        )

        return min(chi_lt, 1.0)
    
    @staticmethod
    def cl_15_2_2_unsupported_beam_bending_non_dimensional_slenderness(
            beta_b, Zp, Zeff, fy, Mcr):
        """
        Calculate non-dimensional lateral torsional slenderness
        ratio as per Cl. 15.2.2 of Draft IS 800:2025.

        Args:
            beta_b: Section modulus factor
            Zp: Plastic section modulus
            Zeff: Effective section modulus
            fy: Yield stress
            Mcr: Elastic lateral torsional buckling moment

        Returns:
            lambda_LT
        """
        lambda_lt_1 = math.sqrt(
            beta_b * Zp * fy / Mcr
        )

        lambda_lt_2 = math.sqrt(
            1.2 * Zeff * fy / Mcr
        )

        return min(lambda_lt_1, lambda_lt_2)
    print("\n===== CLAUSE 15.2.2 TESTS =====")

Md = IS800_2025.cl_15_2_2_unsupported_beam_bending_strength(
    beta_b=1.0,
    Zp=500000,
    fbd=200
)
print("15.2.2 Design bending strength Md =", Md, "N-mm")


fbd = IS800_2025.cl_15_2_2_unsupported_beam_bending_compressive_stress(
    chi_lt=0.8,
    fy=250,
    gamma_m0=1.1
)
print("15.2.2 Design bending compressive stress fbd =", fbd, "MPa")


phi_lt = IS800_2025.cl_15_2_2_unsupported_beam_bending_phi_lt(
    fm=1.0,
    lambda_lt=1.2,
    lambda_y=0.8,
    alpha_lt=0.34
)
print("15.2.2 Phi_LT =", phi_lt)


chi_lt = IS800_2025.cl_15_2_2_unsupported_beam_bending_stress_reduction_factor(
    phi_lt=phi_lt,
    lambda_lt=1.2,
    fm=1.0
)
print("15.2.2 Chi_LT =", chi_lt)


lambda_lt = IS800_2025.cl_15_2_2_unsupported_beam_bending_non_dimensional_slenderness(
    beta_b=1.0,
    Zp=500000,
    Zeff=450000,
    fy=250,
    Mcr=200000000
)
print("15.2.2 Lambda_LT =", lambda_lt)
# ============================================================
# CLAUSE 22.4.1 — YIELD STRESS VARIATION WITH TEMPERATURE
# ============================================================

print("\n===== CLAUSE 22.4.1 TEST =====")

fy_20 = 250  # MPa

# At room temperature, 20°C
fy_20_result = IS800_2025.cl_22_4_1_yield_stress_temperature(
    f_y_20=fy_20,
    T=20
)

print(
    "22.4.1 Yield stress at 20°C =",
    fy_20_result,
    "MPa"
)

# At elevated temperature, 600°C
fy_600_result = IS800_2025.cl_22_4_1_yield_stress_temperature(
    f_y_20=fy_20,
    T=600
)

print(
    "22.4.1 Yield stress at 600°C =",
    fy_600_result,
    "MPa"
)