# Created: 2024-12-01
# Last Modified: 2025-04-16
# (c) Copyright 2024 ETH Zurich, Milos Katanic
# https://doi.org/10.5905/ethz-1007-842
#
# Licensed under the GNU General Public License v3.0;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     https://www.gnu.org/licenses/gpl-3.0.en.html
#
# This software is distributed "AS IS", WITHOUT WARRANTY OF ANY KIND,
# express or implied. See the License for specific language governing
# permissions and limitations under the License.
#

# The code is based on the publication: Katanic, M., Lygeros, J., Hug, G.: Recursive
# dynamic state estimation for power systems with an incomplete nonlinear DAE model.
# IET Gener. Transm. Distrib. 18, 3657–3668 (2024). https://doi.org/10.1049/gtd2.13308
# The full paper version is available at: https://arxiv.org/abs/2305.10065v2
# See full metadata at: README.md
# For inquiries, contact: mkatanic@ethz.ch


from __future__ import annotations  # Postponed type evaluation
from typing import TYPE_CHECKING, Tuple

from pydynamicestimator.devices.device import DeviceRect, sin, cos, sqrt


if TYPE_CHECKING:
    from pydynamicestimator.system import Dae
import casadi as ca
import numpy as np


class Synchronous(DeviceRect):
    """Metaclass for SG in rectangular coordinates with TGOV1 governor and IEEEDC1 exciter"""

    def __init__(self):
        super().__init__()
        self._params.update(
            {
                "fn": 50,
                "H": 30,
                "R_s": 0.0,
                "x_q": 0.2,
                "x_d": 0.2,
                "D": 0.0,
                "Rd": 0.05,
                "Tch": 0.05,
                "Tsv": 1.5,
                "KA": 200.0,
                "TA": 0.015,
                "KF": 1.0,
                "TF": 0.1,
                "KE": 1.0,
                "TE": 0.04,
                "f": 0.01,
                "Vr_max": 5.0,
                "Vr_min": 0.0,
                "psv_min": -10,
                "psv_max": 10,
            }
        )

        self._descr.update(
            {
                "H": "inertia constant",
                "D": "rotor damping",
                "fn": "rated frequency",
                "bus": "bus id",
                "gen": "static generator id",
                "R_s": "stator resistance",
                "x_d": "reactance in d axis",
                "x_q": "reactance in q axis",
                "f": "rotor friction coefficient",
                "Tch": "steam chest time constant",
                "Tsv": "steam valve time constant",
                "Rd": "droop constant",
                "KA": "voltage regulator gain",
                "TA": "voltage regulator time constant",
                "KF": "stabilizer gain",
                "TF": "stabilizer time constant",
                "KE": "exciter field constant without saturation",
                "TE": "exciter time constant",
                "delta": "mechanical rotor angle with respect to fictitious synchronous frame",
                "omega": "per unit mechanical speed deviation from synchronous",
                "psv": "steam valve position",
                "pm": "mechanical rotor toque",
                "Efd": "internal field voltage",
                "Rf": "feedback rate",
                "Vr": "pilot exciter voltage",
                "Pref": "generator mechanical power set point",
                "Vf_ref": "exciter set point voltage",
                "Vr_min": "Exciter minimal voltage",
                "Vr_max": "Exciter maximal voltage",
                "psv_min": "Governor minimal set point",
                "psv_max": "Governor maximal set point",
            }
        )
        # params
        # SG
        self.fn = np.array([], dtype=float)
        self.H = np.array([], dtype=float)
        self.R_s = np.array([], dtype=float)
        self.x_d = np.array([], dtype=float)
        self.x_q = np.array([], dtype=float)
        self.D = np.array([], dtype=float)
        self.f = np.array([], dtype=float)
        # Governor
        self.Rd = np.array([], dtype=float)
        self.Tch = np.array([], dtype=float)
        self.Tsv = np.array([], dtype=float)
        # Exciter
        self.KA = np.array([], dtype=float)
        self.TA = np.array([], dtype=float)
        self.KF = np.array([], dtype=float)
        self.TF = np.array([], dtype=float)
        self.KE = np.array([], dtype=float)
        self.TE = np.array([], dtype=float)
        self.Vr_max = np.array([], dtype=float)
        self.Vr_min = np.array([], dtype=float)
        self.psv_max = np.array([], dtype=float)
        self.psv_min = np.array([], dtype=float)

        # States
        self.ns = 7
        self.states.extend(["delta", "omega", "psv", "pm", "Efd", "Rf", "Vr"])
        self.units.extend(["rad", "p.u.", "p.u.", "p.u.", "p.u.", "p.u.", "p.u."])
        self.delta = np.array([], dtype=float)
        self.omega = np.array([], dtype=float)
        self.psv = np.array([], dtype=float)  # steam valve position
        self.pm = np.array([], dtype=float)
        self.Efd = np.array([], dtype=float)
        self.Rf = np.array([], dtype=float)
        self.Vr = np.array([], dtype=float)

        self._states_noise.update(
            {
                "delta": 1e-2,
                "omega": 1e-2,
                "psv": 1,
                "pm": 1,
                "Efd": 1,
                "Rf": 1,
                "Vr": 1,
            }
        )
        self._states_init_error.update(
            {
                "delta": 0.1,
                "omega": 0.001,
                "psv": 0.1,
                "pm": 0.1,
                "Efd": 0.1,
                "Rf": 0.1,
                "Vr": 0.1,
            }
        )
        self._x0.update(
            {
                "delta": 0.5,
                "omega": 0.0,
                "psv": 0.5,
                "pm": 0.5,
                "Efd": 1.5,
                "Rf": 0.2,
                "Vr": 1.5,
            }
        )

        # Set points
        self._setpoints.update({"Pref": 0.1, "Vf_ref": 2.0})
        self.Vf_ref = np.array([], dtype=float)
        self.Pref = np.array([], dtype=float)
        self.properties.update({"fplot": True})

    def gcall(self, dae: Dae, i_d: ca.SX, i_q: ca.SX) -> None:
        # algebraic equations (current balance in rectangular coordinates) + scale the current back to the grid reference power
        dae.g[self.vre] -= (
            self.Sn
            / dae.Sb
            * (i_d * sin(dae.x[self.delta]) + i_q * cos(dae.x[self.delta]))
        )
        dae.g[self.vim] -= (
            self.Sn
            / dae.Sb
            * (i_d * -cos(dae.x[self.delta]) + i_q * sin(dae.x[self.delta]))
        )

    def tgov1(self, dae: Dae) -> None:
        """
        TGOV1 governor model as presented in Power System Dynamics and Stability by P.W. Sauer and M.A. Pai, 2006. (page 100)

        Parameters
        ----------
        dae : DAE
        """

        dae.f[self.pm] = 1 / self.Tch * (dae.x[self.psv] - dae.x[self.pm])
        dae.f[self.psv] = (
            dae.s[self.psv]
            * 1
            / self.Tsv
            * (-dae.x[self.omega] / self.Rd - dae.x[self.psv] + self.Pref)
        )

    def ieeedc1a(self, dae: Dae) -> None:
        """
        IEEEDC1 exciter and AVR model as presented in Power System Dynamics and Stability by P.W. Sauer and M.A. Pai, 2006. (page 100)

        Parameters
        ----------
        dae : differential-algebraic model class
        """
        dae.f[self.Efd] = 1 / self.TE * (-(self.KE) * dae.x[self.Efd] + dae.x[self.Vr])
        dae.f[self.Rf] = (
            1 / self.TF * (-dae.x[self.Rf] + self.KF / self.TF * (dae.x[self.Efd]))
        )
        dae.f[self.Vr] = (
            dae.s[self.Vr]
            * 1
            / self.TA
            * (
                -dae.x[self.Vr]
                + self.KA * dae.x[self.Rf]
                - self.KA * self.KF / self.TF * dae.x[self.Efd]
                + self.KA
                * (self.Vf_ref - sqrt((dae.y[self.vre]) ** 2 + (dae.y[self.vim]) ** 2))
            )
        )


class SynchronousTransient(Synchronous):
    r"""
    Transient two-axis SG with TGOV1 governor and IEEEDC1A AVR

    **Rotor Dynamics**


    .. math::

        \dot{\delta} &= 2 \pi f_n \Delta \omega \\
        \Delta \dot{\omega} &= \frac{1}{2 H} \left( P_m - E_d I_d - E_q I_q + (X_q' - X_d') I_d I_q - D \Delta \omega - f (\Delta \omega + 1) \right)

    **Electromagnetic Equations**


    .. math::

        \dot{E}_q &= \frac{1}{T_{d'}} \left( -E_q + E_f + (X_d - X_d') I_d \right)\\
        \dot{E}_d &= \frac{1}{T_{q'}} \left( -E_d - (X_q - X_q') I_q \right)

    **Excitation System Equations**


    .. math::

         \dot{E}_{\textup{fd}} &= \frac{1}{T_{E}} \left( -K_{E,i}E_{\textup{fd},i} + V_{R,i}\right)\\
        \dot{R}_{f} &= \frac{1}{T_{F} } \left(- R_{f} + \frac{K_{F}}{T_{F}}E_{\textup{fd}} \right)\\
        \dot{V}_{R} &= \frac{1}{T_{A}} \left(-V_{R} + K_{A}R_{f} - \frac{K_{A}K_{F}}{T_{F}}E_{\textup{fd}} + K_{A}(v_{\textup{ref}} - v_i) \right)

    **Turbine-Governor System Equations**


    .. math::

        \dot{p}_{\textup{m}} &= \frac{1}{T_{ch}} \left( p_{\textup{sv}}- p_{\textup{m}} \right)\\
         \dot{p}_{sv} &= \frac{1}{T_{sv}} \left( - \frac{\Delta \omega}{R_d} - p_{\textup{sv}} + p_{\textup{ref}} \right)




    """

    def __init__(self) -> None:
        super().__init__()

        self._type = "Synchronous_machine"
        self._name = "Synchronous_machine_transient_model"

        # States
        self.ns += 2
        self.states.extend(["e_dprim", "e_qprim"])
        self.units.extend(["p.u.", "p.u."])
        self.e_dprim = np.array([], dtype=float)
        self.e_qprim = np.array([], dtype=float)

        self._states_noise.update(
            {
                "e_dprim": 1,
                "e_qprim": 1,
            }
        )
        self._states_init_error.update({"e_dprim": 0.1, "e_qprim": 0.1})
        self._x0.update(
            {
                "delta": 0.0,
                "omega": 0.0,
                "e_dprim": -0.4,
                "e_qprim": 1,
                "psv": 0.5,
                "pm": 0.5,
                "Efd": 2.5,
                "Rf": 0.0,
                "Vr": 2.5,
            }
        )

        # Params
        self._params.update(
            {"x_dprim": 0.05, "x_qprim": 0.1, "T_dprim": 8.0, "T_qprim": 0.8}
        )
        self._descr.update(
            {
                "T_dprim": "d-axis transient time constant",
                "T_qprim": "q-axis transient time constant",
                "e_dprim": "d-axis voltage behind transient reactance",
                "e_qprim": "q-axis voltage behind transient reactance",
                "x_dprim": "d-axis transient reactance",
                "x_qprim": "q-axis transient reactance",
            }
        )

        # Parameters
        self.x_dprim = np.array([], dtype=float)
        self.x_qprim = np.array([], dtype=float)
        self.T_dprim = np.array([], dtype=float)
        self.T_qprim = np.array([], dtype=float)

        self.properties.update(
            {
                "fgcall": True,
                "finit": True,
                "init_data": True,
                "xy_index": True,
                "save_data": True,
                "qcall": True,
                "gcall": True,
            }
        )

        self._init_data()

    def input_current(self, dae: Dae) -> Tuple[ca.SX, ca.SX]:
        # differential equations
        i_d = ca.SX.sym("id", self.n)
        i_q = ca.SX.sym("iq", self.n)
        for i in range(self.n):
            adq = ca.SX(
                [[self.R_s[i], -self.x_qprim[i]], [self.x_dprim[i], self.R_s[i]]]
            )
            vd = dae.y[self.vre[i]] * np.sin(dae.x[self.delta[i]]) + dae.y[
                self.vim[i]
            ] * -np.cos(dae.x[self.delta[i]])
            vq = dae.y[self.vre[i]] * np.cos(dae.x[self.delta[i]]) + dae.y[
                self.vim[i]
            ] * np.sin(dae.x[self.delta[i]])
            b1 = -vd + dae.x[self.e_dprim[i]]
            b2 = -vq + dae.x[self.e_qprim[i]]
            b = ca.vertcat(b1, b2)
            i_dq = (
                ca.solve(adq, b) * dae.Sb / self.Sn[i]
            )  # scale the current for the base power inside the machine
            i_d[i] = i_dq[0]
            i_q[i] = i_dq[1]
        return i_d, i_q

    def two_axis(self, dae, i_d: ca.SX, i_q: ca.SX) -> None:
        """
        Mechanical and electrical equations for the two-axis model.

        :param dae: Dae

        :type dae:

        :param i_d: Stator d-current

        :type i_d: casadi.SX

        :param i_q: Stator q-current

        :type i_q: casadi.SX

        :return: None

        :rtype: None
        """
        dae.f[self.delta] = 2 * np.pi * dae.fn * dae.x[self.omega]
        dae.f[self.omega] = (
            1
            / (2 * self.H)
            * (
                dae.x[self.pm]
                - dae.x[self.e_dprim] * i_d
                - dae.x[self.e_qprim] * i_q
                - (self.x_qprim - self.x_dprim) * i_d * i_q
                - self.D * dae.x[self.omega]
                - self.f * (dae.x[self.omega] + 1)
            )
        )  # omega
        dae.f[self.e_qprim] = (
            1
            / self.T_dprim
            * (-dae.x[self.e_qprim] + dae.x[self.Efd] - (self.x_d - self.x_dprim) * i_d)
        )  # Eq
        dae.f[self.e_dprim] = (
            1 / self.T_qprim * (-dae.x[self.e_dprim] + (self.x_q - self.x_qprim) * i_q)
        )  # Ed

    def fgcall(self, dae: Dae) -> None:
        """
        A method that executes the differential and algebraic equations of the model
        and adds them to the appropriate places in the Dae class

        :param dae: an instance of a class Dae

        :type dae:

        :return: None

        :rtype: None
        """
        i_d, i_q = self.input_current(dae)

        self.two_axis(dae, i_d, i_q)

        self.tgov1(dae)

        self.ieeedc1a(dae)

        self.gcall(dae, i_d, i_q)


class SynchronousSubtransient(Synchronous):
    r"""Subtransient Anderson Fouad SG with TGOV1 governor and IEEEDC1A AVR
    The subtransient behavior of the synchronous generator is described by the following differential equations:


    **Rotor Dynamics**


    .. math::

        \dot{\delta} &= 2 \pi f_n \Delta \omega \\
        \Delta \dot{\omega} &= \frac{1}{2 H} \Big( P_m - E_{d}^{\prime\prime} I_d - E_{q}^{\prime\prime} I_q + (X_q^{\prime\prime} - X_d^{\prime\prime}) I_d I_q - D \Delta \omega - f (\Delta \omega + 1) \Big) \\

    **Electromagnetic Equations**


    .. math::

        \dot{E}_q^{\prime} &= \frac{1}{T_{d}^{\prime}} \Big( -E_q + E_f + (X_d - X_d^{\prime}) I_d \Big) \\
        \dot{E}_d^{\prime} &= \frac{1}{T_{q}^{\prime}} \Big( -E_d - (X_q - X_q^{\prime}) I_q \Big) \\
        \dot{E}_{q}^{\prime\prime} &= \frac{1}{T_{d}^{\prime\prime}} \Big( E_q - E_{q}^{\prime\prime} + (X_d^{\prime} - X_d^{\prime\prime}) I_d \Big) \\
        \dot{E}_{d}^{\prime\prime} &= \frac{1}{T_{q}^{\prime\prime}} \Big( E_d - E_{d}^{\prime\prime} - (X_q^{\prime} - X_q^{\prime\prime}) I_q \Big) \\

    **Excitation System Equations**


    .. math::

         \dot{E}_{\textup{fd}} &= \frac{1}{T_{E}} \left( -K_{E,i}E_{\textup{fd},i} + V_{R,i}\right)\\
        \dot{R}_{f} &= \frac{1}{T_{F} } \left(- R_{f} + \frac{K_{F}}{T_{F}}E_{\textup{fd}} \right)\\
        \dot{V}_{R} &= \frac{1}{T_{A}} \left(-V_{R} + K_{A}R_{f} - \frac{K_{A}K_{F}}{T_{F}}E_{\textup{fd}} + K_{A}(v_{\textup{ref}} - v_i) \right)

    **Turbine-Governor System Equations**


    .. math::

        \dot{p}_{\textup{m}} &= \frac{1}{T_{ch}} \left( p_{\textup{sv}}- p_{\textup{m}} \right)\\
         \dot{p}_{sv} &= \frac{1}{T_{sv}} \left( - \frac{\Delta \omega}{R_d} - p_{\textup{sv}} + p_{\textup{ref}} \right)
    """

    def __init__(self) -> None:
        super().__init__()

        # private data
        self._type = "Synchronous_machine"
        self._name = "Synchronous_machine_subtransient_model"

        # States
        self.ns += 4
        self.states.extend(["e_dprim", "e_qprim", "e_dsec", "e_qsec"])
        self.units.extend(["p.u.", "p.u.", "p.u.", "p.u."])
        self.e_dprim = np.array([], dtype=float)
        self.e_qprim = np.array([], dtype=float)
        self.e_dsec = np.array([], dtype=float)
        self.e_qsec = np.array([], dtype=float)
        self._states_noise.update(
            {"e_dprim": 1, "e_qprim": 1, "e_dsec": 1, "e_qsec": 1}
        )
        self._states_init_error.update(
            {"e_dprim": 0.1, "e_qprim": 0.1, "e_dsec": 0.1, "e_qsec": 0.1}
        )

        self._x0.update(
            {
                "delta": 0.0,
                "omega": 0.0,
                "e_dprim": 0.0,
                "e_qprim": 1.0,
                "psv": 0.5,
                "pm": 0.5,
                "Efd": 2.3,
                "Rf": 0.0,
                "Vr": 2.3,
                "e_dsec": 0.0,
                "e_qsec": 1.0,
            }
        )

        # Params
        self._params.update(
            {
                "x_dprim": 0.05,
                "x_qprim": 0.1,
                "T_dprim": 8.0,
                "T_qprim": 0.8,
                "x_dsec": 0.01,
                "x_qsec": 0.01,
                "T_dsec": 0.001,
                "T_qsec": 0.001,
            }
        )

        self._descr.update(
            {
                "T_dprim": "d-axis transient time constant",
                "T_qprim": "q-axis transient time constant",
                "x_dprim": "d-axis transient reactance",
                "x_qprim": "q-axis transient reactance",
                "e_dprim": "d-axis voltage behind transient reactance",
                "e_qprim": "q-axis voltage behind transient reactance",
                "e_dsec": "d-axis voltage behind subtransient reactance",
                "e_qsec": "q-axis voltage behind subtransient reactance",
                "T_dsec": "d-axis subtransient time constant",
                "T_qsec": "q-axis subtransient time constant",
                "x_dsec": "d-axis subtransient reactance",
                "x_qsec": "q-axis subtransient reactance",
            }
        )

        # Parameters
        self.x_dprim = np.array([], dtype=float)
        self.x_qprim = np.array([], dtype=float)
        self.T_dprim = np.array([], dtype=float)
        self.T_qprim = np.array([], dtype=float)
        self.x_dsec = np.array([], dtype=float)
        self.x_qsec = np.array([], dtype=float)
        self.T_dsec = np.array([], dtype=float)
        self.T_qsec = np.array([], dtype=float)

        self.properties.update(
            {
                "fgcall": True,
                "finit": True,
                "init_data": True,
                "xy_index": True,
                "save_data": True,
                "qcall": True,
            }
        )

        self._init_data()

    def input_current(self, dae: Dae) -> Tuple[ca.SX, ca.SX]:
        # differential equations
        i_d = ca.SX.sym("Id", self.n)
        i_q = ca.SX.sym("Iq", self.n)
        for i in range(self.n):
            adq = ca.SX([[self.R_s[i], -self.x_qsec[i]], [self.x_dsec[i], self.R_s[i]]])
            vd = dae.y[self.vre[i]] * np.sin(dae.x[self.delta[i]]) + dae.y[
                self.vim[i]
            ] * -np.cos(dae.x[self.delta[i]])
            vq = dae.y[self.vre[i]] * np.cos(dae.x[self.delta[i]]) + dae.y[
                self.vim[i]
            ] * np.sin(dae.x[self.delta[i]])
            b1 = -vd + dae.x[self.e_dsec[i]]
            b2 = -vq + dae.x[self.e_qsec[i]]
            b = ca.vertcat(b1, b2)
            i_dq = (
                ca.solve(adq, b) * dae.Sb / self.Sn[i]
            )  # scale the current for the base power inside the machine
            i_d[i] = i_dq[0]
            i_q[i] = i_dq[1]
        return i_d, i_q

    def anderson_fouad(self, dae: Dae, i_d: ca.SX, i_q: ca.SX):
        """

        :param dae:
        :type dae:
        :param i_d:
        :type i_d:
        :param i_q:
        :type i_q:
        :return:
        :rtype:
        """
        dae.f[self.delta] = 2 * np.pi * dae.fn * dae.x[self.omega]
        dae.f[self.omega] = (
            1
            / (2 * self.H)
            * (
                dae.x[self.pm]
                - dae.x[self.e_dsec] * i_d
                - dae.x[self.e_qsec] * i_q
                - (self.x_qsec - self.x_dsec) * i_d * i_q
                - self.D * dae.x[self.omega]
                - self.f * (dae.x[self.omega] + 1)
            )
        )  # omega
        dae.f[self.e_qprim] = (
            1
            / self.T_dprim
            * (-dae.x[self.e_qprim] + dae.x[self.Efd] - (self.x_d - self.x_dprim) * i_d)
        )  # Eq
        dae.f[self.e_dprim] = (
            1 / self.T_qprim * (-dae.x[self.e_dprim] + (self.x_q - self.x_qprim) * i_q)
        )  # Ed
        dae.f[self.e_qsec] = (
            1
            / self.T_dsec
            * (
                dae.x[self.e_qprim]
                - dae.x[self.e_qsec]
                - (self.x_dprim - self.x_dsec) * i_d
            )
        )
        dae.f[self.e_dsec] = (
            1
            / self.T_qsec
            * (
                dae.x[self.e_dprim]
                - dae.x[self.e_dsec]
                + (self.x_qprim - self.x_qsec) * i_q
            )
        )

    def fgcall(self, dae: Dae) -> None:
        i_d, i_q = self.input_current(dae)

        self.anderson_fouad(dae, i_d, i_q)

        self.tgov1(dae)

        self.ieeedc1a(dae)

        self.gcall(dae, i_d, i_q)


class SynchronousSubtransientSP(Synchronous):
    r"""Subtransient Sauer and Pai SG model with stator dynamics
    with TGOV1 governor and IEEEDC1A AVR


    The model includes the following equations for rotor dynamics, stator dynamics, and the excitation system:



    **Rotor Dynamics**


    .. math::

        \dot{\delta} &= 2 \pi f_n \Delta \omega \\
        \Delta \dot{\omega} &= \frac{1}{2 H} \Big( P_m - (\psi_d I_q - \psi_q I_d) - D \Delta \omega - f (\Delta \omega + 1) \Big)

    **Electromagnetic Equations**


    The stator dynamics include the following equations for the flux linkages in the d and q axes:

    .. math::

        \dot{E}_d' &= \frac{1}{T_q'} \Big( -E_d' + (X_q - X_q') (i_q - g_{q2} \Psi_{q2} - (1 - g_{q1}) i_q - g_{q2} E_d') \Big) \\
        \dot{E}_q' &= \frac{1}{T_d'} \Big( -E_q' - (X_d - X_d') (i_d - g_{d2} \Psi_{d2} - (1 - g_{d1}) i_d + g_{d2} E_q') + E_f \Big)\\
        \dot{\Psi}_{d2} &= \frac{1}{T_{d2}} \Big( -\Psi_{d2} + E_q' - (X_d' - X_l) i_d \Big) \\
        \dot{\Psi}_{q2} &= \frac{1}{T_{q2}} \Big( -\Psi_{q2} - E_d' - (X_q' - X_l) i_q \Big)



    **Flux Linkage Dynamics**


    The following equations describe the stator flux linkage dynamics in the d and q axes:

    .. math::

        \dot{\Psi}_d &= 2 \pi f_n (R_s i_d + (1 + \Delta \omega) \Psi_q + v_d) \\
        \dot{\Psi}_q &= 2 \pi f_n (R_s i_q - (1 + \Delta \omega) \Psi_d + v_q)

    **Algebraic Equations**

    The following algebraic equations govern the system:

    .. math::

        i_d &= \frac{1}{x_d''} \Big( -\psi_d + g_{d1} e_q' + (1 - g_{d1}) \psi_{d2} \Big)\\
        i_q &= \frac{1}{x_q''} \Big( -\psi_q - g_{q1} e_d' + (1 - g_{q1}) \psi_{q2} \Big)\\
        g_{d1} &= \frac{x_d'' - x_l}{x_d' - x_l}\\
        g_{q1} &= \frac{x_q'' - x_l}{x_q' - x_l}\\
        g_{d2} &= \frac{1 - g_{d1}}{x_d' - x_l}\\
        g_{q2} &= \frac{1 - g_{q1}}{x_q' - x_l}
    """

    def __init__(self) -> None:
        super().__init__()

        # private data
        self._type = "Synchronous_machine"
        self._name = "Synchronous_machine_subtransient_model_Sauer_Pai"

        # States
        self.ns += 6
        self.states.extend(["e_dprim", "e_qprim", "psid", "psiq", "psid2", "psiq2"])
        self.units.extend(["p.u.", "p.u.", "p.u.", "p.u.", "p.u.", "p.u."])
        self.e_dprim = np.array([], dtype=float)
        self.e_qprim = np.array([], dtype=float)
        self.psid = np.array([], dtype=float)
        self.psiq = np.array([], dtype=float)
        self.psid2 = np.array([], dtype=float)
        self.psiq2 = np.array([], dtype=float)
        self._states_noise.update(
            {
                "e_dprim": 1.0,
                "e_qprim": 1.0,
                "psid": 1.0,
                "psiq": 1.0,
                "psid2": 1.0,
                "psiq2": 1.0,
            }
        )
        self._states_init_error.update(
            {
                "e_dprim": 0.1,
                "e_qprim": 0.1,
                "psid": 0.1,
                "psiq": 0.1,
                "psid2": 0.1,
                "psiq2": 0.1,
            }
        )

        self._x0.update(
            {
                "delta": 0.5,
                "omega": 0.0,
                "e_dprim": 0.2,
                "e_qprim": 1.0,
                "psid": 1.0,
                "psiq": -0.5,
                "psid2": 1.0,
                "psiq2": -0.5,
                "psv": 0.5,
                "pm": 0.5,
                "Efd": 2.3,
                "Rf": 0.0,
                "Vr": 2.3,
            }
        )

        # Params
        self._params.update(
            {
                "gd1": 1.0,
                "gq1": 1.0,
                "gd2": 1.0,
                "gq2": 1.0,
                "x_l": 0.1,
                "x_dprim": 0.05,
                "x_qprim": 0.1,
                "T_dprim": 8.0,
                "T_qprim": 0.8,
                "x_dsec": 0.01,
                "x_qsec": 0.01,
                "T_dsec": 0.001,
                "T_qsec": 0.001,
            }
        )

        self._descr.update(
            {
                "T_dprim": "d-axis transient time constant",
                "T_qprim": "q-axis transient time constant",
                "x_dprim": "d-axis transient reactance",
                "x_qprim": "q-axis transient reactance",
                "e_dprim": "d-axis voltage behind transient reactance",
                "e_qprim": "q-axis voltage behind transient reactance",
                "T_dsec": "d-axis subtransient time constant",
                "T_qsec": "q-axis subtransient time constant",
                "x_dsec": "d-axis subtransient reactance",
                "x_qsec": "q-axis subtransient reactance",
                "x_l": "leakage reactance",
                "psid": "stator flux in d axis",
                "psiq": "stator flux in q axis",
                "psiq2": "subtransient stator flux in q axis",
                "psid2": "subtransient stator flux in d axis",
            }
        )

        # Parameters
        self.x_l = np.array([], dtype=float)
        self.gd1 = np.array([], dtype=float)
        self.gq1 = np.array([], dtype=float)
        self.gd2 = np.array([], dtype=float)
        self.gq2 = np.array([], dtype=float)
        self.x_dprim = np.array([], dtype=float)
        self.x_qprim = np.array([], dtype=float)
        self.T_dprim = np.array([], dtype=float)
        self.T_qprim = np.array([], dtype=float)
        self.x_dsec = np.array([], dtype=float)
        self.x_qsec = np.array([], dtype=float)
        self.T_dsec = np.array([], dtype=float)
        self.T_qsec = np.array([], dtype=float)

        self.properties.update(
            {
                "fgcall": True,
                "finit": True,
                "init_data": True,
                "xy_index": True,
                "save_data": True,
                "qcall": True,
            }
        )

        self._init_data()

    def sauer_pai(self, dae: Dae, i_d: ca.SX, i_q: ca.SX):
        """
        Sauer and Pai model.
        Parameters
        ----------
        dae : DAE

        i_d : casadi.SX

        i_q : casadi.SX

        Returns
        -------

        """
        vd = dae.y[self.vre] * np.sin(dae.x[self.delta]) + dae.y[self.vim] * -np.cos(
            dae.x[self.delta]
        )
        vq = dae.y[self.vre] * np.cos(dae.x[self.delta]) + dae.y[self.vim] * np.sin(
            dae.x[self.delta]
        )

        dae.f[self.delta] = 2 * np.pi * dae.fn * dae.x[self.omega]
        dae.f[self.omega] = (
            1
            / (2 * self.H)
            * (
                dae.x[self.pm]
                - (dae.x[self.psid] * i_q - dae.x[self.psiq] * i_d)
                - self.D * dae.x[self.omega]
                - self.f * (dae.x[self.omega] + 1)
            )
        )  # omega

        dae.f[self.e_dprim] = (
            1
            / self.T_qprim
            * (
                -dae.x[self.e_dprim]
                + (self.x_q - self.x_qprim)
                * (
                    i_q
                    - self.gq2 * dae.x[self.psiq2]
                    - (1 - self.gq1) * i_q
                    - self.gq2 * dae.x[self.e_dprim]
                )
            )
        )
        dae.f[self.e_qprim] = (
            1
            / self.T_dprim
            * (
                -dae.x[self.e_qprim]
                - (self.x_d - self.x_dprim)
                * (
                    i_d
                    - self.gd2 * dae.x[self.psid2]
                    - (1 - self.gd1) * i_d
                    + self.gd2 * dae.x[self.e_qprim]
                )
                + dae.x[self.Efd]
            )
        )
        dae.f[self.psid2] = (
            1
            / self.T_dsec
            * (
                -dae.x[self.psid2]
                + dae.x[self.e_qprim]
                - (self.x_dprim - self.x_l) * i_d
            )
        )
        dae.f[self.psiq2] = (
            1
            / self.T_qsec
            * (
                -dae.x[self.psiq2]
                - dae.x[self.e_dprim]
                - (self.x_qprim - self.x_l) * i_q
            )
        )
        dae.f[self.psid] = (
            2
            * np.pi
            * dae.fn
            * (self.R_s * i_d + (1 + dae.x[self.omega]) * dae.x[self.psiq] + vd)
        )
        dae.f[self.psiq] = (
            2
            * np.pi
            * dae.fn
            * (self.R_s * i_q - (1 + dae.x[self.omega]) * dae.x[self.psid] + vq)
        )

    def fgcall(self, dae: Dae) -> None:
        self.gd1 = (self.x_dsec - self.x_l) / (self.x_dprim - self.x_l)
        self.gq1 = (self.x_qsec - self.x_l) / (self.x_qprim - self.x_l)
        self.gd2 = (1 - self.gd1) / (self.x_dprim - self.x_l)
        self.gq2 = (1 - self.gq1) / (self.x_qprim - self.x_l)

        i_d = (
            1
            / self.x_dsec
            * (
                -dae.x[self.psid]
                + self.gd1 * dae.x[self.e_qprim]
                + (1 - self.gd1) * dae.x[self.psid2]
            )
        )
        i_q = (
            1
            / self.x_qsec
            * (
                -dae.x[self.psiq]
                - self.gq1 * dae.x[self.e_dprim]
                + (1 - self.gq1) * dae.x[self.psiq2]
            )
        )

        self.sauer_pai(dae, i_d, i_q)

        self.tgov1(dae)

        self.ieeedc1a(dae)

        self.gcall(dae, i_d, i_q)


class SynchronousSubtransientSP6(Synchronous):
    r"""Subtransient Sauer and Pai SG 6th order model with neglected stator dynamics
    (stator modeled with algebraic equations) and included TGOV1 governor and
    IEEEDC1A AVR

    The model includes the following equations:



    **Rotor Dynamics**


    .. math::

        \dot{\delta} &= 2 \pi f_n \Delta \omega \\
        \Delta \dot{\omega} &= \frac{1}{2 H} \Big( P_m - (\psi_d I_q - \psi_q I_d) - D \Delta \omega - f (\Delta \omega + 1) \Big)

    **Electromagnetic Equations**


    The stator dynamics include the following equations for the flux linkages in the d and q axes:

    .. math::

        \dot{E}_d' &= \frac{1}{T_q'} \Big( -E_d' + (X_q - X_q') (i_q - g_{q2} \Psi_{q2} - (1 - g_{q1}) i_q - g_{q2} E_d') \Big) \\
        \dot{E}_q' &= \frac{1}{T_d'} \Big( -E_q' - (X_d - X_d') (i_d - g_{d2} \Psi_{d2} - (1 - g_{d1}) i_d + g_{d2} E_q') + E_f \Big)\\
        \dot{\Psi}_{d2} &= \frac{1}{T_{d2}} \Big( -\Psi_{d2} + E_q' - (X_d' - X_l) i_d \Big) \\
        \dot{\Psi}_{q2} &= \frac{1}{T_{q2}} \Big( -\Psi_{q2} - E_d' - (X_q' - X_l) i_q \Big)



    **Flux Linkage Dynamics**


    The following equations describe the stator flux linkage dynamics in the d and q axes:



    **Algebraic Equations**

    The following algebraic equations govern the system:

    .. math::

        0 &=-i_d +\frac{1}{x_d''} \Big( -\psi_d + g_{d1} e_q' + (1 - g_{d1}) \psi_{d2} \Big)\\
        0&=-i_q +\frac{1}{x_q''} \Big( -\psi_q - g_{q1} e_d' + (1 - g_{q1}) \psi_{q2} \Big)\\
        0&= R_s i_d + (1 + \Delta \omega) \Psi_q + v_d \\
        0&= R_s i_q - (1 + \Delta \omega) \Psi_d + v_q \\
        g_{d1} &= \frac{x_d'' - x_l}{x_d' - x_l}\\
        g_{q1} &= \frac{x_q'' - x_l}{x_q' - x_l}\\
        g_{d2} &= \frac{1 - g_{d1}}{x_d' - x_l}\\
        g_{q2} &= \frac{1 - g_{q1}}{x_q' - x_l}
    """

    def __init__(self) -> None:
        super().__init__()

        # private data
        self._type = "Synchronous_machine"
        self._name = "Synchronous_machine_subtransient_model_Sauer_Pai_6th_order"

        # States
        self.ns += 4
        self.states.extend(["e_dprim", "e_qprim", "psid2", "psiq2"])
        self.units.extend(["p.u.", "p.u.", "p.u.", "p.u."])
        self.e_dprim = np.array([], dtype=float)
        self.e_qprim = np.array([], dtype=float)
        self.psid2 = np.array([], dtype=float)
        self.psiq2 = np.array([], dtype=float)

        self._states_noise.update(
            {
                "e_dprim": 1.0,
                "e_qprim": 1.0,
                "psid2": 1.0,
                "psiq2": 1.0,
            }
        )
        self._states_init_error.update(
            {
                "e_dprim": 0.1,
                "e_qprim": 0.1,
                "psid2": 0.1,
                "psiq2": 0.1,
            }
        )

        self._x0.update(
            {
                "delta": 0.5,
                "omega": 0.0,
                "e_dprim": 0.2,
                "e_qprim": 1.0,
                "psid2": 1.0,
                "psiq2": -0.5,
                "psv": 0.5,
                "pm": 0.5,
                "Efd": 2.3,
                "Rf": 0.0,
                "Vr": 2.3,
            }
        )

        # Params
        self._params.update(
            {
                "gd1": 1.0,
                "gq1": 1.0,
                "gd2": 1.0,
                "gq2": 1.0,
                "x_l": 0.1,
                "x_dprim": 0.05,
                "x_qprim": 0.1,
                "T_dprim": 8.0,
                "T_qprim": 0.8,
                "x_dsec": 0.01,
                "x_qsec": 0.01,
                "T_dsec": 0.001,
                "T_qsec": 0.001,
            }
        )

        self._descr.update(
            {
                "T_dprim": "d-axis transient time constant",
                "T_qprim": "q-axis transient time constant",
                "x_dprim": "d-axis transient reactance",
                "x_qprim": "q-axis transient reactance",
                "e_dprim": "d-axis voltage behind transient reactance",
                "e_qprim": "q-axis voltage behind transient reactance",
                "T_dsec": "d-axis subtransient time constant",
                "T_qsec": "q-axis subtransient time constant",
                "x_dsec": "d-axis subtransient reactance",
                "x_qsec": "q-axis subtransient reactance",
                "x_l": "leakage reactance",
                "psid2": "subtransient flux in d axis",
                "psiq2": "subtransient flux in q axis",
            }
        )

        # Parameters
        self.x_l = np.array([], dtype=float)
        self.gd1 = np.array([], dtype=float)
        self.gq1 = np.array([], dtype=float)
        self.gd2 = np.array([], dtype=float)
        self.gq2 = np.array([], dtype=float)
        self.x_dprim = np.array([], dtype=float)
        self.x_qprim = np.array([], dtype=float)
        self.T_dprim = np.array([], dtype=float)
        self.T_qprim = np.array([], dtype=float)
        self.x_dsec = np.array([], dtype=float)
        self.x_qsec = np.array([], dtype=float)
        self.T_dsec = np.array([], dtype=float)
        self.T_qsec = np.array([], dtype=float)

        self.properties.update(
            {
                "fgcall": True,
                "finit": True,
                "init_data": True,
                "xy_index": True,
                "save_data": True,
                "qcall": True,
            }
        )

        self._init_data()

    def sauer_pai_6(self, dae: Dae, i_d: ca.SX, i_q: ca.SX, psid: ca.SX, psiq: ca.SX):
        r"""
        Sauer and Pai model.
        Parameters
        ----------
        dae : DAE

        i_d : casadi.SX

        i_q : casadi.SX

        psid : casadi.SX

        psiq : casadi.SX

        Returns
        -------

        Args:
            psid ():
            psiq ():

        """

        dae.f[self.delta] = 2 * np.pi * dae.fn * dae.x[self.omega]
        dae.f[self.omega] = (
            1
            / (2 * self.H)
            * (
                dae.x[self.pm]
                - (psid * i_q - psiq * i_d)
                - self.D * dae.x[self.omega]
                - self.f * (dae.x[self.omega] + 1)
            )
        )  # omega

        dae.f[self.e_dprim] = (
            1
            / self.T_qprim
            * (
                -dae.x[self.e_dprim]
                + (self.x_q - self.x_qprim)
                * (
                    i_q
                    - self.gq2 * dae.x[self.psiq2]
                    - (1 - self.gq1) * i_q
                    - self.gq2 * dae.x[self.e_dprim]
                )
            )
        )
        dae.f[self.e_qprim] = (
            1
            / self.T_dprim
            * (
                -dae.x[self.e_qprim]
                - (self.x_d - self.x_dprim)
                * (
                    i_d
                    - self.gd2 * dae.x[self.psid2]
                    - (1 - self.gd1) * i_d
                    + self.gd2 * dae.x[self.e_qprim]
                )
                + dae.x[self.Efd]
            )
        )
        dae.f[self.psid2] = (
            1
            / self.T_dsec
            * (
                -dae.x[self.psid2]
                + dae.x[self.e_qprim]
                - (self.x_dprim - self.x_l) * i_d
            )
        )
        dae.f[self.psiq2] = (
            1
            / self.T_qsec
            * (
                -dae.x[self.psiq2]
                - dae.x[self.e_dprim]
                - (self.x_qprim - self.x_l) * i_q
            )
        )

    def fgcall(self, dae: Dae) -> None:
        self.gd1 = (self.x_dsec - self.x_l) / (self.x_dprim - self.x_l)
        self.gq1 = (self.x_qsec - self.x_l) / (self.x_qprim - self.x_l)
        self.gd2 = (1 - self.gd1) / (self.x_dprim - self.x_l)
        self.gq2 = (1 - self.gq1) / (self.x_qprim - self.x_l)
        i_d = ca.SX.sym("i_d", self.n)
        i_q = ca.SX.sym("i_q", self.n)
        psid = ca.SX.sym("psid", self.n)
        psiq = ca.SX.sym("psiq", self.n)

        for i in range(self.n):
            # Symbolic variables for unknowns
            algs = ca.SX.sym("algs", 4)  # symbolic unknowns

            # Define vd and vq in terms of symbolic variables (using symbolic dae.x and dae.y)
            vd = dae.y[self.vre][i] * ca.sin(dae.x[self.delta][i]) + dae.y[self.vim][
                i
            ] * -ca.cos(dae.x[self.delta][i])
            vq = dae.y[self.vre][i] * ca.cos(dae.x[self.delta][i]) + dae.y[self.vim][
                i
            ] * ca.sin(dae.x[self.delta][i])

            # Define g as a symbolic vector in terms of algs, dae.x, and dae.y
            g = ca.SX(4, 1)
            g[0] = -algs[0] + (1 / self.x_dsec[i]) * (
                -algs[2]
                + self.gd1[i] * dae.x[self.e_qprim][i]
                + (1 - self.gd1[i]) * dae.x[self.psid2][i]
            )
            g[1] = -algs[1] + (1 / self.x_qsec[i]) * (
                -algs[3]
                - self.gq1[i] * dae.x[self.e_dprim][i]
                + (1 - self.gq1[i]) * dae.x[self.psiq2][i]
            )
            g[2] = (
                2
                * ca.pi
                * dae.fn
                * (self.R_s[i] * algs[0] + (1 + dae.x[self.omega][i]) * algs[3] + vd)
            )
            g[3] = (
                2
                * ca.pi
                * dae.fn
                * (self.R_s[i] * algs[1] - (1 + dae.x[self.omega][i]) * algs[2] + vq)
            )

            # Calculate the Jacobian of g with respect to algs
            J = ca.jacobian(g, algs)

            g_eval = ca.substitute(g, algs, ca.DM.zeros(4))

            # Solve J * x = -g symbolically
            sol = ca.solve(J, -g_eval)

            # Assign solutions to variables
            i_d[i] = sol[0]
            i_q[i] = sol[1]
            psid[i] = sol[2]
            psiq[i] = sol[3]

        self.sauer_pai_6(dae, i_d, i_q, psid, psiq)

        self.tgov1(dae)

        self.ieeedc1a(dae)

        self.gcall(dae, i_d, i_q)
