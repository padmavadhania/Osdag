"""Module for Draft Indian Standard, IS 800 : 2025

This module contains steel design provisions implemented
from the Draft IS 800:2025.

The implementation is developed with reference to the
existing IS 800:2007 implementation in Osdag.
"""

import math
from ...Common import *


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
    @staticmethod
    def cl_10_7_2_table2_i(
            width, thickness, f_y,
            stress_type='Uniform compression',
            r1=None):
        """
        Calculate the section class for an outstanding element
        as per Table 2(i) of Draft IS 800:2025.

        Args:
            width: Width of the outstanding element in mm.
            thickness: Thickness of the element in mm.
            f_y: Yield stress of the material in MPa.
            stress_type: Type of stress distribution:
                         'Uniform compression',
                         'Tip in compression',
                         'Tip in tension'.
            r1: Stress ratio parameter for non-uniform stress.

        Returns:
            [section_class, ratio]
        """

        epsilon = math.sqrt(250 / f_y)
        ratio = width / thickness

        if stress_type == 'Uniform compression':

            if ratio <= 8.7 * epsilon:
                section_class = KEY_Plastic
            elif ratio <= 9.7 * epsilon:
                section_class = KEY_Compact
            elif ratio <= 13.6 * epsilon:
                section_class = KEY_SemiCompact
            else:
                section_class = 'Slender'

        elif stress_type == 'Tip in compression':

            if r1 is None:
                raise ValueError(
                    "r1 is required for non-uniform stress."
                )

            if ratio <= (8.7 * epsilon / r1):
                section_class = KEY_Plastic
            elif ratio <= (9.7 * epsilon / r1):
                section_class = KEY_Compact
            else:
                section_class = 'Slender'

        elif stress_type == 'Tip in tension':

            if r1 is None:
                raise ValueError(
                    "r1 is required for non-uniform stress."
                )

            limit_class_1 = (
                8.7 * epsilon
                / (r1 * math.sqrt(r1))
            )

            limit_class_2 = (
                9.7 * epsilon
                / (r1 * math.sqrt(r1))
            )

            if ratio <= limit_class_1:
                section_class = KEY_Plastic
            elif ratio <= limit_class_2:
                section_class = KEY_Compact
            else:
                section_class = 'Slender'

        else:
            raise ValueError(
                "Invalid stress_type."
            )

        return [section_class, ratio]
    

    @staticmethod
    def cl_10_7_2_table2_ii(depth, thickness, f_y,
                            classification_type='Axial compression',
                            r1=None, r2=None):
        """
        Section classification for web of I, Channel, H or box section
        as per Table 2(ii), Draft IS 800:2025.
        """

        epsilon = math.sqrt(250 / f_y)
        ratio = depth / thickness

        if classification_type == 'Axial compression':

            if ratio <= 32 * epsilon:
                section_class = KEY_Plastic
            elif ratio <= 36.8 * epsilon:
                section_class = KEY_Compact
            elif ratio <= 40.7 * epsilon:
                section_class = KEY_SemiCompact
            else:
                section_class = 'Slender'

        elif classification_type == 'Neutral axis at mid-depth':

            if ratio <= 70 * epsilon:
                section_class = KEY_Plastic
            elif ratio <= 80 * epsilon:
                section_class = KEY_Compact
            elif ratio <= 120 * epsilon:
                section_class = KEY_SemiCompact
            else:
                section_class = 'Slender'

        else:
            raise ValueError(
                "Non-uniform web classification requires "
                "verification of the complete 2025 Table 2 formula."
            )

        return [section_class, ratio]


    @staticmethod
    def cl_10_7_2_table2_iii(width, depth, thickness, f_y):
        """
        Section classification for angle subjected to compression
        due to bending as per Table 2(iii), Draft IS 800:2025.

        Both b/t and d/t criteria must be satisfied.
        """

        epsilon = math.sqrt(250 / f_y)

        b_t = width / thickness
        d_t = depth / thickness

        if b_t <= 8.7 * epsilon and d_t <= 8.7 * epsilon:
            section_class = KEY_Plastic

        elif b_t <= 9.7 * epsilon and d_t <= 9.7 * epsilon:
            section_class = KEY_Compact

        elif b_t <= 14.5 * epsilon and d_t <= 14.5 * epsilon:
            section_class = KEY_SemiCompact

        else:
            section_class = 'Slender'

        return [section_class, b_t, d_t]


    @staticmethod
    def cl_10_7_2_table2_iv(width, depth, thickness, f_y):
        """
        Section classification for single angle or double angles
        with components separated under axial compression
        as per Table 2(iv), Draft IS 800:2025.

        All three criteria must be satisfied.
        """

        epsilon = math.sqrt(250 / f_y)

        b_t = width / thickness
        d_t = depth / thickness
        bd_t = (width + depth) / thickness

        if (
            b_t <= 14.5 * epsilon
            and d_t <= 14.5 * epsilon
            and bd_t <= 22.3 * epsilon
        ):
            section_class = KEY_SemiCompact
        else:
            section_class = 'Slender'

        return [section_class, b_t, d_t, bd_t]


    @staticmethod
    def cl_10_7_2_table2_v(depth, thickness, f_y):
        """
        Section classification for outstanding leg of an angle
        as per Table 2(v), Draft IS 800:2025.
        """

        epsilon = math.sqrt(250 / f_y)
        ratio = depth / thickness

        if ratio <= 8.7 * epsilon:
            section_class = KEY_Plastic
        elif ratio <= 9.7 * epsilon:
            section_class = KEY_Compact
        elif ratio <= 14.5 * epsilon:
            section_class = KEY_SemiCompact
        else:
            section_class = 'Slender'

        return [section_class, ratio]


    @staticmethod
    def cl_10_7_2_table2_vi(outer_diameter, tube_thickness, f_y,
                            load_type='axial compression'):
        """
        Section classification for circular hollow tube,
        including welded tube, as per Table 2(vi),
        Draft IS 800:2025.
        """

        epsilon = math.sqrt(250 / f_y)
        ratio = outer_diameter / tube_thickness

        if load_type == 'axial compression':

            if ratio <= 86 * epsilon ** 2:
                section_class = KEY_SemiCompact
            else:
                section_class = 'Slender'

        elif load_type == 'moment':

            if ratio <= 47 * epsilon ** 2:
                section_class = KEY_Plastic

            elif ratio <= 66 * epsilon ** 2:
                section_class = KEY_Compact

            elif ratio <= 85 * epsilon ** 2:
                section_class = KEY_SemiCompact

            else:
                section_class = 'Slender'

        else:
            raise ValueError(
                "Invalid load_type. Use 'moment' "
                "or 'axial compression'."
            )

        return section_class
    @staticmethod
    def cl_22_4_1_yield_stress_temperature(f_y_20, T):
        """
        Calculate yield stress of steel at temperature T
        as per Clause 22.4.1 of Draft IS 800:2025.

        Args:
            f_y_20: Yield stress at 20°C (MPa)
            T: Temperature of steel (°C)

        Returns:
            Yield stress at temperature T (MPa)
        """

        reduction_factor = (905 - T) / 690
        reduction_factor = min(reduction_factor, 1.0)

        f_y_T = reduction_factor * f_y_20

        return f_y_T
    # ======================================================================
    """    ANNEX G     ANCHOR BOLTS    """
    # ======================================================================

    # ----------------------------------------------------------------------
    @staticmethod
    def annex_g_2_3_2_anchor_shear_bending_moment(
            Vu, lever_arm, alpha_M):
        """
        Calculate the ultimate bending moment in an anchor bolt
        subjected to shear and bending as per Annex G, Clause G-2.3.2
        of Draft IS 800:2025.

        Args:
            Vu: Shear force acting on the anchor bolt
            lever_arm: Lever arm of the anchor bolt
            alpha_M: Fixture rotational restraint factor
                     2.0 for fully restrained
                     1.0 for not restrained

        Returns:
            Mu: Ultimate bending moment in the anchor bolt
        """

        Mu = Vu * lever_arm / alpha_M

        return Mu

    # ----------------------------------------------------------------------
    @staticmethod
    def annex_g_2_3_1_anchor_shear_resistance(
            A_sn, f_usa, gamma_MSV, low_ductility=False):
        """
        Calculate design shear resistance of an anchor due to
        steel failure without bending as per G-2.3.1 of
        Draft IS 800:2025.

        Args:
            A_sn: Net shear area of the anchor in mm^2
            f_usa: Ultimate tensile strength of anchor steel in MPa
            gamma_MSV: Partial safety factor for shear
            low_ductility: True for anchor group with lower ductility
                           (epsilon_u <= 8 percent)

        Returns:
            V_das: Design shear resistance of the anchor in N
        """

        V_das = (0.5 * A_sn * f_usa) / gamma_MSV

        if low_ductility:
            V_das *= 0.8

        return V_das
    # ----------------------------------------------------------------------
    @staticmethod
    def annex_g_2_3_2_anchor_reference_bending_resistance(
            Z_ea, f_usa):
        """
        Calculate reference bending resistance of an anchor
        as per G-2.3.2 of Draft IS 800:2025.

        Args:
            Z_ea: Elastic section modulus of the anchor in mm^3
            f_usa: Ultimate tensile strength of anchor steel in MPa

        Returns:
            Md0: Reference bending resistance of the anchor in N-mm
        """

        Md0 = 1.2 * Z_ea * f_usa

        return Md0
    # ----------------------------------------------------------------------
    @staticmethod
    def annex_g_2_3_2_anchor_design_bending_resistance(
            Md0, Tu, Tdsa):
        """
        Calculate design bending resistance of an anchor subjected
        to shear and bending as per G-2.3.2 of Draft IS 800:2025.

        Args:
            Md0: Reference bending resistance of the anchor in N-mm
            Tu: Tensile force in the anchor in N
            Tdsa: Design tensile resistance of the anchor in N

        Returns:
            Mds: Design bending resistance of the anchor in N-mm
        """

        Mds = Md0 * (1 - Tu / Tdsa)

        return Mds
        # ----------------------------------------------------------------------
    @staticmethod
    def annex_g_2_3_2_anchor_shear_resistance_with_bending(
            alpha_M, Mds, lever_arm, gamma_MSV):
        """
        Calculate design shear resistance of an anchor governed by
        steel failure with shear and bending as per G-2.3.2 of
        Draft IS 800:2025.

        Args:
            alpha_M: Fixture rotational restraint factor
            Mds: Design bending resistance of the anchor in N-mm
            lever_arm: Lever arm of the anchor in mm
            gamma_MSV: Partial safety factor for shear

        Returns:
            V_das: Design shear resistance of the anchor in N
        """

        V_das = (alpha_M * Mds) / (lever_arm * gamma_MSV)

        return V_das
    # ----------------------------------------------------------------------
    @staticmethod
    def annex_g_2_3_3_concrete_pryout_resistance(
            hef, Tdca):
        """
        Calculate design shear resistance governed by concrete
        pry-out failure as per G-2.3.3 of Draft IS 800:2025.

        Args:
            hef: Effective embedment depth of anchor in mm
            Tdca: Design tension resistance of anchor governed by
                  concrete pyramid failure in N

        Returns:
            V_dcp: Design shear resistance governed by concrete
                   pry-out failure in N
        """

        if hef < 60:
            k = 1
        else:
            k = 2

        V_dcp = k * Tdca

        return V_dcp
    # ----------------------------------------------------------------------
    @staticmethod
    def annex_g_2_3_4_concrete_edge_failure_resistance(
            da, hef, fck, c1, gamma_MCV,
            A_cv, A0_cv,
            psi_sv, psi_av, psi_ecv, psi_ucrv, psi_hv):
        """
        Calculate design shear resistance of an anchor governed by
        concrete edge failure as per G-2.3.4 of Draft IS 800:2025.

        Args:
            da: Nominal diameter of anchor in mm
            hef: Effective embedment depth of anchor in mm
            fck: Characteristic compressive strength of concrete in MPa
            c1: Edge distance in direction of shear in mm
            gamma_MCV: Partial safety factor for concrete shear
            A_cv: Actual area of concrete cone considering group
                  and edge effects in mm^2
            A0_cv: Area of concrete cone of an individual anchor in mm^2
            psi_sv: Modification factor
            psi_av: Modification factor
            psi_ecv: Modification factor
            psi_ucrv: Modification factor
            psi_hv: Modification factor

        Returns:
            V_dac: Design shear resistance due to concrete edge
                   failure in N
        """

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
    