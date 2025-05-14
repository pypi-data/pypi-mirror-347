# Created: 2024-12-01
# Last Modified: 2025-05-13
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
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from system import Dae
from pydynamicestimator.devices.device import DeviceRect
import numpy as np
import casadi as ca


class StaticLoadPower(DeviceRect):  # Not finished
    def __init__(self) -> None:
        super().__init__()
        self._type = "Static_load_power"
        self._name = "Static_load_power"
        self._setpoints.update({"p": 0.0, "q": 0.0})
        self.p = np.array([], dtype=float)
        self.q = np.array([], dtype=float)
        self.properties.update(
            {
                "fgcall": True,
                "finit": True,
                "init_data": True,
                "xy_index": True,
                "save_data": False,
            }
        )

    def gcall(self, dae: Dae) -> None:

        dae.g[self.vre] += (
            self.p / dae.Sb * dae.y[self.vre] + self.q / dae.Sb * dae.y[self.vim]
        ) / (dae.y[self.vre] ** 2 + dae.y[self.vim] ** 2)
        dae.g[self.vim] += (
            self.p / dae.Sb * dae.y[self.vim] - self.q / dae.Sb * dae.y[self.vre]
        ) / (dae.y[self.vre] ** 2 + dae.y[self.vim] ** 2)

    def fgcall(self, dae: Dae) -> None:
        self.gcall(dae)


class StaticLoadImpedance(DeviceRect):
    def __init__(self) -> None:
        super().__init__()
        self._type = "Static_load_impedance"
        self._name = "Static_load_impedance"
        self._setpoints.update({"g": 1.0, "b": 1.0})
        self.g = np.array([], dtype=float)
        self.b = np.array([], dtype=float)
        self.properties.update(
            {
                "fgcall": True,
                "finit": True,
                "init_data": True,
                "xy_index": True,
                "save_data": False,
            }
        )

    def gcall(self, dae: Dae):

        dae.g[self.vre] += self.g * dae.y[self.vre] - self.b * dae.y[self.vim]
        dae.g[self.vim] += self.b * dae.y[self.vre] + self.g * dae.y[self.vim]

    def fgcall(self, dae: Dae) -> None:
        self.gcall(dae)

    def finit(self, dae: Dae) -> None:
        super().finit(dae)
        2 == 2


class StaticInfiniteBus(DeviceRect):
    r"""
    This model implements the infinite bus with current balance equations. Resistance
    and reactance need to be set and the voltage values get calculated during
    initialization.

    Attributes:
        r (np.ndarray): Resistance value
        x (np.ndarray): Reactance value
        vre_int (np.ndarray): Internal voltage value
        vim_int (np.ndarray): Internal voltage value

    .. math::
       :nowrap:

       \begin{aligned}
       i_{re} &= \frac{1}{r^2 + x^2} \left( (v_{re} - v_{re}^{\text{int}}) r + (v_{im} - v_{im}^{\text{int}}) x \right) \\
       i_{im} &= \frac{1}{r^2 + x^2} \left( -\left(v_{re} - v_{re}^{\text{int}}\right) x + \left(v_{im} - v_{im}^{\text{int}}\right) r \right)
       \end{aligned}
    """

    def __init__(self) -> None:
        super().__init__()
        self._type = "Infinite_bus"
        self._name = "Infinite_bus"
        self._setpoints.update({"vre_int": 1.0, "vim_int": 0.0})
        self.vre_int = np.array([], dtype=float)
        self.vim_int = np.array([], dtype=float)
        self._params.update({"r": 0.001, "x": 0.001})
        self.r = np.array([], dtype=float)  # internal resistance
        self.x = np.array([], dtype=float)  # internal reactance
        self.properties.update(
            {
                "fgcall": True,
                "finit": True,
                "init_data": True,
                "xy_index": True,
                "save_data": False,
            }
        )

    def gcall(self, dae: Dae):

        dae.g[self.vre] += (
            1
            / (self.r**2 + self.x**2)
            * (
                (dae.y[self.vre] - self.vre_int) * self.r
                + (dae.y[self.vim] - self.vim_int) * self.x
            )
        )
        dae.g[self.vim] += (
            1
            / (self.r**2 + self.x**2)
            * (
                (dae.y[self.vre] - self.vre_int) * -self.x
                + (dae.y[self.vim] - self.vim_int) * self.r
            )
        )

    def fgcall(self, dae: Dae) -> None:
        self.gcall(dae)


class StaticZIP(DeviceRect):
    r"""
    ZIP static load. The shares of Z, I, and P (z_share, i_share, p_share) in the overall load need to be specified,
    and then the inner  parameters of the load will be set during the initialization
    to satisfy the initial power flow and the share of contributions of each load tape. The shares need to sum up to one for the
    initialization to work perfectly. Positive reactive current i_q means consumption.



    .. math::
      :nowrap:

      \begin{aligned}
      i_{re} &= \left(\frac{{p}v_{re} + {q} v_{im}}{v_{re}^2 + v_{im}^2}\right) + (g v_{re} - b v_{im}) + (\cos{\theta} i_d + \sin{\theta} i_q)\\
      i_{re} &=\left(\frac{{p}v_{im} - {q} v_{re}}{v_{re}^2 + v_{im}^2} \right)+ (b v_{re} + g v_{im}) + (\sin{\theta} i_q - \sin{\theta} i_d)
      \end{aligned}

    Attributes:
        g (np.ndarray:  Conductance value
        b (np.ndarray):  Susceptance value
        p (np.ndarray):  Active power value
        q (np.ndarray):  Reactive power value
        id (np.ndarray):  Active current value
        iq (np.ndarray):  Reactive current value
        p_share (np.ndarray):  Share of power load (default: 0.0)
        i_share (np.ndarray):  Share of current load (default: 0.0)
        z_share (np.ndarray):  Share of impedance load (default: 1.0)

    """

    def __init__(self) -> None:
        super().__init__()
        self._type = "Static_load_ZIP"
        self._name = "Static_load_ZIP"
        self._setpoints_z = {"g": 1.0, "b": 1.0}
        self._setpoints_i = {"id": 1.0, "iq": 1.0}
        self._setpoints_p = {"p": 1.0, "q": 1.0}
        self._setpoints.update(
            {"g": 1.0, "b": 1.0, "p": 1.0, "q": 1.0, "id": 1.0, "iq": 1.0}
        )
        self._params.update({"p_share": 0.0, "i_share": 0.0, "z_share": 1.0})
        self.g = np.array([], dtype=float)
        self.b = np.array([], dtype=float)
        self.p = np.array([], dtype=float)
        self.q = np.array([], dtype=float)
        self.id = np.array([], dtype=float)
        self.iq = np.array([], dtype=float)
        self.p_share = np.array([], dtype=float)
        self.i_share = np.array([], dtype=float)
        self.z_share = np.array([], dtype=float)
        self.properties.update(
            {
                "fgcall": True,
                "finit": True,
                "init_data": True,
                "xy_index": True,
                "save_data": False,
            }
        )

    def gcall_i(self, dae: Dae):
        theta = np.arctan2(dae.y[self.vim], dae.y[self.vre])
        i_re = np.cos(theta) * self.id + np.sin(theta) * self.iq
        i_im = np.sin(theta) * self.id - np.cos(theta) * self.iq
        dae.g[self.vre] += i_re
        dae.g[self.vim] += i_im

    def gcall_p(self, dae: Dae):

        dae.g[self.vre] += (self.p * dae.y[self.vre] + self.q * dae.y[self.vim]) / (
            dae.y[self.vre] ** 2 + dae.y[self.vim] ** 2
        )
        dae.g[self.vim] += (self.p * dae.y[self.vim] - self.q * dae.y[self.vre]) / (
            dae.y[self.vre] ** 2 + dae.y[self.vim] ** 2
        )

    def gcall_z(self, dae: Dae):

        dae.g[self.vre] += self.g * dae.y[self.vre] - self.b * dae.y[self.vim]
        dae.g[self.vim] += self.b * dae.y[self.vre] + self.g * dae.y[self.vim]

    def fgcall(self, dae: Dae) -> None:
        self.gcall_i(dae)
        self.gcall_z(dae)
        self.gcall_p(dae)

    def finit_sub(self, dae: Dae, sub: str) -> None:
        _setpoints = self.__getattribute__(f"_setpoints_{sub}")
        share = self.__getattribute__(f"{sub}_share")
        u = ca.SX.sym("", 0)
        u0 = []
        for item in _setpoints:
            # Set the initial guess for the setpoint
            u0.append(self.__dict__[item])
            # Reset it to be a variable
            self.__dict__[item] = ca.SX.sym(item, self.n)
            # Stack the variable to a single vector
            u = ca.vertcat(u, self.__dict__[item])
        u0 = [item for sublist in u0 for item in sublist]

        # Now subtract the initial network currents from algebraic equations
        for alg in self._algebs:
            dae.g[self.__dict__[alg]] += dae.iinit[self.__dict__[alg]] * share

        # Algebraic variables are now not symbolic but their init values
        dae.y = dae.yinit.copy()
        dae.s = np.ones(dae.nx)
        dae.s = np.ones(dae.nx)
        gcall = self.__getattribute__(f"gcall_{sub}")
        gcall(dae)
        # self.fgcall(dae)

        inputs = [ca.vertcat(u)]
        outputs = [
            ca.vertcat(
                dae.g[self.__dict__["vre"]],
                dae.g[self.__dict__["vim"]],
            )
        ]

        power_flow_init = ca.Function("h", inputs, outputs)
        newton_init = ca.rootfinder("G", "newton", power_flow_init)

        solution = newton_init(ca.vertcat(u0))
        solution = np.array(solution).flatten()

        for idx, s in enumerate(_setpoints):
            setpoint_range_start = (len(self.states) + idx) * self.n
            self.__dict__[s] = solution[
                setpoint_range_start : setpoint_range_start + self.n
            ]

        # Reset the algebraic equations such that they can be used "erneut" from scratch once the "fgcall" is called
        dae.g *= 0
        # Reset the voltages to being again symbolic variables
        dae.y = ca.SX.sym("y", dae.ny)
        dae.s = ca.SX.sym("s", dae.nx)

    def finit(self, dae: Dae) -> None:

        self.finit_sub(dae, "p")
        self.finit_sub(dae, "z")
        self.finit_sub(dae, "i")
        2 == 2
