# Created: 2024-12-01
# Last Modified: 2025-05-14
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
from scipy.linalg import cho_solve, cholesky, block_diag, null_space
from typing import Literal, Optional, Tuple
from pydynamicestimator.devices.device import Line, BusInit, Disturbance, BusUnknown
import casadi as ca
import numpy as np
import pandas as pd
from tabulate import tabulate
import logging
import math
import time

np.set_printoptions(threshold=np.inf)
np.random.seed(30)


class Grid:
    def __init__(self) -> None:

        self.y_adm_matrix: Optional[np.ndarray] = None  # Admittance matrix
        self.z_imp_matrix: Optional[np.ndarray] = None  # Impedance matrix
        self.incident_matrix: Optional[np.ndarray] = None
        self.Bsum: Optional[np.ndarray] = None  # sum of shunt susceptance at each node
        self.Gsum: Optional[np.ndarray] = None  # sum of shunt conductance at each node
        self.nb: int = 0  # Number of branches
        self.nn: int = 0  # Number of nodes
        self.buses: list = []  # list of all system buses

        self.Sb: float = 100
        # Indices corresponding to branches
        self.idx_i: list = []
        self.idx_j: list = []
        self.idx_i_re: list = []
        self.idx_j_re: list = []
        self.idx_i_im: list = []
        self.idx_j_im: list = []

        self.yinit: dict = {}  # Init voltages
        self.yf: dict = {}  # Output voltages
        self.sf: dict = {}  # Output power

        self.line: Optional[Line] = None
        self.line_is_faulted: list[bool] = []
        self.line_is_open: list[bool] = []
        self.line_fault_adm: list[float] = []
        self.bus_is_faulted: list[bool] = []
        self.bus_fault_adm: list[float] = []
        # Dictionary indices for fast look up
        self.idx_branch: dict[Tuple[str, str], int] = {}
        self.idx_bus: dict[str, int] = {}
        self.idx_bus_re: dict[str, int] = {}
        self.idx_bus_im: dict[str, int] = {}
        # Matrices to calculate all branch currents
        self.C_branches_forward: Optional[np.ndarray] = None
        self.C_branches_reverse: Optional[np.ndarray] = None
        self.C_branches: Optional[np.ndarray] = None  # stacked together

    def save_data(self, dae: Dae) -> None:

        for idx, bus in enumerate(self.buses):
            self.yf[str(bus)] = dae.y_full[2 * idx : 2 * idx + 2, :]

        # for idx, bus in enumerate(self.buses):
        #     self.sf[bus] = np.zeros([2, dae.nts])
        #
        #     for t in range(dae.nts):
        #         u_power = stack_volt_power(
        #             dae.y_full[2 * idx, t], dae.y_full[2 * idx + 1, t]
        #         )
        #         self.sf[bus][:, t] = u_power.dot(
        #             self.y_adm_matrix[2 * idx : 2 * idx + 2, :]
        #         ).dot(dae.y_full[:, t])

    def init_symbolic(self, dae: Dae) -> None:
        dae.ny = self.nn * 2
        dae.y = ca.SX.sym("y", dae.ny)
        dae.g = ca.SX(np.zeros(dae.ny))
        dae.grid = self

    def gcall(self, dae: Dae) -> None:
        dae.g += self.y_adm_matrix @ dae.y

    def guncall(self, dae: Dae) -> None:
        dae.g -= self.y_adm_matrix @ dae.y

    def add_lines(self, line: Line) -> None:
        self.line = line
        for bus_i, bus_j in zip(line.bus_i, line.bus_j):
            self.add_bus(bus_i, self.idx_i, self.idx_i_re, self.idx_i_im)
            self.add_bus(bus_j, self.idx_j, self.idx_j_re, self.idx_j_im)
            self.idx_branch[(bus_i, bus_j)] = self.nb
            self.nb += 1
        self.line_is_faulted = [False] * self.nb
        self.line_fault_adm = [0.0] * self.nb
        self.line_is_open = [False] * self.nb
        self.bus_is_faulted = [False] * self.nn
        self.bus_fault_adm = [0.0] * self.nn

    def add_bus(self, bus: str, idx: list, idx_re: list, idx_im: list) -> None:

        if bus not in self.buses:
            self.buses.append(bus)
            idx.append(self.nn)
            idx_re.append(2 * self.nn)
            idx_im.append(2 * self.nn + 1)
            self.idx_bus[bus] = self.nn
            self.nn += 1
        else:
            idx.append(self.buses.index(bus))
            idx_re.append(2 * self.buses.index(bus))
            idx_im.append(1 + 2 * self.buses.index(bus))

    def build_y(self) -> None:
        self.y_adm_matrix = np.zeros([2 * self.nn, 2 * self.nn])
        self.C_branches_forward = np.zeros([2 * self.nb, 2 * self.nn])
        self.C_branches_reverse = np.zeros([2 * self.nb, 2 * self.nn])

        r = self.line.r.copy()
        x = self.line.x.copy()
        g = self.line.g.copy()
        b = self.line.b.copy()
        trafo = self.line.trafo.copy()

        for faulted_line, faulted in enumerate(self.line_is_faulted):
            if faulted:
                rtemp = complex(r[faulted_line])
                xtemp = complex(x[faulted_line])
                gtemp = complex(g[faulted_line])
                btemp = complex(b[faulted_line])
                zt = complex(rtemp, xtemp)
                yt = self.line_fault_adm[faulted_line]
                zp = zt * (1 + zt * yt / 4)
                yp = zt * yt / zp + complex(gtemp, btemp)
                r[faulted_line] = zp.real
                x[faulted_line] = zp.imag
                g[faulted_line] = yp.real
                b[faulted_line] = yp.imag
        for open_line, opened in enumerate(self.line_is_open):
            if opened:
                r[open_line] = 1e308
                x[open_line] = 1e308
                g[open_line] = 0
                b[open_line] = 0
        for bus_id, faulted in enumerate(self.bus_is_faulted):
            if faulted:
                np.add.at(
                    self.y_adm_matrix,
                    (2 * bus_id, 2 * bus_id),
                    self.bus_fault_adm[bus_id],
                )
                np.add.at(
                    self.y_adm_matrix,
                    (2 * bus_id + 1, 2 * bus_id + 1),
                    self.bus_fault_adm[bus_id],
                )

        # Calculate Y matrix values
        z_inv = 1 / (r**2 + x**2)
        y_off_diag_real = -r * z_inv / trafo
        y_off_diag_imag = -x * z_inv / trafo
        y_diag_real = (g / 2 + r * z_inv) / trafo**2
        y_diag_imag = (-b / 2 + x * z_inv) / trafo**2

        # Update Y matrix with vectorized operations
        np.add.at(self.y_adm_matrix, (self.idx_i_re, self.idx_j_re), y_off_diag_real)
        np.add.at(self.y_adm_matrix, (self.idx_i_re, self.idx_j_im), y_off_diag_imag)
        np.add.at(self.y_adm_matrix, (self.idx_i_im, self.idx_j_re), -y_off_diag_imag)
        np.add.at(self.y_adm_matrix, (self.idx_i_im, self.idx_j_im), y_off_diag_real)

        np.add.at(self.y_adm_matrix, (self.idx_j_re, self.idx_i_re), y_off_diag_real)
        np.add.at(self.y_adm_matrix, (self.idx_j_re, self.idx_i_im), y_off_diag_imag)
        np.add.at(self.y_adm_matrix, (self.idx_j_im, self.idx_i_re), -y_off_diag_imag)
        np.add.at(self.y_adm_matrix, (self.idx_j_im, self.idx_i_im), y_off_diag_real)

        # Update diagonal elements
        np.add.at(self.y_adm_matrix, (self.idx_i_re, self.idx_i_re), y_diag_real)
        np.add.at(self.y_adm_matrix, (self.idx_i_re, self.idx_i_im), y_diag_imag)
        np.add.at(self.y_adm_matrix, (self.idx_i_im, self.idx_i_re), -y_diag_imag)
        np.add.at(self.y_adm_matrix, (self.idx_i_im, self.idx_i_im), y_diag_real)

        np.add.at(self.y_adm_matrix, (self.idx_j_re, self.idx_j_re), g / 2 + r * z_inv)
        np.add.at(self.y_adm_matrix, (self.idx_j_re, self.idx_j_im), -b / 2 + x * z_inv)
        np.add.at(self.y_adm_matrix, (self.idx_j_im, self.idx_j_re), b / 2 - x * z_inv)
        np.add.at(self.y_adm_matrix, (self.idx_j_im, self.idx_j_im), g / 2 + r * z_inv)

        even_rows = np.arange(0, 2 * self.nb, 2)
        odd_rows = np.arange(1, 2 * self.nb, 2)
        # Create a branch impedance matrix to calculate branch currents
        np.add.at(
            self.C_branches_forward,
            (even_rows, self.idx_i_re),
            -y_off_diag_real / trafo + g / 2 / trafo**2,
        )
        np.add.at(
            self.C_branches_forward,
            (even_rows, self.idx_i_im),
            -y_off_diag_imag / trafo - b / 2 / trafo**2,
        )
        np.add.at(
            self.C_branches_forward,
            (odd_rows, self.idx_i_re),
            y_off_diag_imag / trafo + b / 2 / trafo**2,
        )
        np.add.at(
            self.C_branches_forward,
            (odd_rows, self.idx_i_im),
            -y_off_diag_real / trafo + g / 2 / trafo**2,
        )

        np.add.at(self.C_branches_forward, (even_rows, self.idx_j_re), y_off_diag_real)
        np.add.at(self.C_branches_forward, (even_rows, self.idx_j_im), y_off_diag_imag)
        np.add.at(self.C_branches_forward, (odd_rows, self.idx_j_re), -y_off_diag_imag)
        np.add.at(self.C_branches_forward, (odd_rows, self.idx_j_im), y_off_diag_real)

        np.add.at(
            self.C_branches_reverse,
            (even_rows, self.idx_j_re),
            -y_off_diag_real * trafo + g / 2,
        )
        np.add.at(
            self.C_branches_reverse,
            (even_rows, self.idx_j_im),
            -y_off_diag_imag * trafo - b / 2,
        )
        np.add.at(
            self.C_branches_reverse,
            (odd_rows, self.idx_j_re),
            y_off_diag_imag * trafo + b / 2,
        )
        np.add.at(
            self.C_branches_reverse,
            (odd_rows, self.idx_j_im),
            -y_off_diag_real * trafo + g / 2,
        )

        np.add.at(self.C_branches_reverse, (even_rows, self.idx_i_re), y_off_diag_real)
        np.add.at(self.C_branches_reverse, (even_rows, self.idx_i_im), y_off_diag_imag)
        np.add.at(self.C_branches_reverse, (odd_rows, self.idx_i_re), -y_off_diag_imag)
        np.add.at(self.C_branches_reverse, (odd_rows, self.idx_i_im), y_off_diag_real)

        self.C_branches = np.vstack((self.C_branches_forward, self.C_branches_reverse))
        self.z_imp_matrix = np.linalg.inv(self.y_adm_matrix)

    def get_branch_index(
        self, node1: list[str], node2: list[str]
    ) -> tuple[np.ndarray, np.ndarray]:
        """

        Args:
            node1 (): List of starting nodes
            node2 (): List of receiving nodes

        Returns: The order of the given branch and the order of the opposite direction branch

        """
        # Sort the node pair and look it up in the dictionary
        # the first one sequence doesn't matter
        # the second one matters
        ids1 = []
        ids2 = []
        if isinstance(node1, str):
            node1 = [node1]
        if isinstance(node2, str):
            node2 = [node2]

        for n1, n2 in zip(node1, node2):
            key = (n1, n2)
            key_r = (n2, n1)

            if key in self.idx_branch:
                idx = self.idx_branch[key]
                ids1.append(idx)
                ids2.append(idx)
            elif key_r in self.idx_branch:
                idx = self.idx_branch[key_r]
                ids1.append(idx)
                ids2.append(idx + self.nb)
            else:
                ids1.append(None)
                ids2.append(None)

        return np.array(ids1), np.array(ids2)

    def get_node_index(self, buses: list) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        # Calculate the real and imaginary indices in one step
        if not buses:
            return (
                np.array([]),
                np.array([]),
                np.array([]),
            )  # Return empty arrays safely, if list of buses empty
        var_indices = [
            (self.idx_bus[bus], 2 * self.idx_bus[bus], 2 * self.idx_bus[bus] + 1)
            for bus in buses
        ]
        idx, idx_re, idx_im = zip(*var_indices)
        return np.array(idx), np.array(idx_re), np.array(idx_im)


class GridSim(Grid):
    def init_from_power_flow(self, dae: DaeSim, static: BusInit) -> None:

        y = ca.SX.sym("y", self.nn * 2)
        y_init = []
        g = ca.SX(np.zeros(self.nn * 2))

        for idx, bus in enumerate(self.buses):
            y_init.extend([1, 0])
            static_idx = static.bus.index(bus)
            y_real = y[2 * idx]
            y_imag = y[2 * idx + 1]

            if static.type[static_idx] == "PQ":
                u_power = ca.horzcat(
                    ca.vertcat(y_real, y_imag), ca.vertcat(+y_imag, -y_real)
                )
                g[2 * idx : 2 * idx + 2] = (
                    u_power @ self.y_adm_matrix[2 * idx : 2 * idx + 2, :] @ y
                    + np.array([static.p[static_idx], static.q[static_idx]]) / self.Sb
                )

            elif static.type[static_idx] == "PV":
                u_power = ca.horzcat(y_real, +y_imag)
                g[2 * idx] = (
                    u_power @ self.y_adm_matrix[2 * idx : 2 * idx + 2, :] @ y
                    + static.p[static_idx] / self.Sb
                )
                g[2 * idx + 1] = (
                    np.sqrt(y[2 * idx] ** 2 + y[2 * idx + 1] ** 2)
                    - static.v[static_idx]
                )

            elif static.type[static_idx] == "slack":
                g[2 * idx] = np.sqrt(y_real**2 + y_imag**2) - static.v[static_idx]
                g[2 * idx + 1] = y_imag

        z = ca.Function("z", [y], [g])
        G = ca.rootfinder("G", "newton", z)
        try:
            solution = G(y_init)
        except Exception as e:
            logging.error(f"An exception occurred: {e}")
            logging.error("Init power flow failed.")
            raise Exception(
                "Power flow cannot be solved. Check if the grid parameters (pu) and initial power consumptions (MW and MVar) are realistic. Generated power should be negative. Only one bus can be slack."
            )
        if (solution == y_init).is_one():
            logging.error(
                "Init power flow aborted. Error unknown. Try different operating point"
            )
            raise Exception("Power flow not solved")
        # save the initial data into yinit dictionary

        for idx, bus in enumerate(self.buses):
            self.yinit[str(bus)] = np.array(solution[2 * idx : 2 * idx + 2].T)[0]

        dae.yinit = np.array(list(self.yinit.values())).reshape(self.nn * 2)
        dae.iinit = self.y_adm_matrix @ dae.yinit

        self.print_init_power_flow(dae)

    def print_init_power_flow(self, dae: DaeSim) -> None:
        # Print results of initialization
        print("\nPower flow for initialization successfully solved")

        # ---- BUS RESULTS ----
        idx_bus_re = [i for i in range(2 * self.nn) if i % 2 == 0]
        idx_bus_im = [i for i in range(2 * self.nn) if i % 2 != 0]

        vinit_re = np.array(dae.yinit)[idx_bus_re]
        vinit_im = np.array(dae.yinit)[idx_bus_im]

        vinit_mag = np.sqrt(vinit_re**2 + vinit_im**2)  # p.u.
        vinit_phase = np.arctan2(vinit_im, vinit_re)  # radians

        iinit_re = np.array(dae.iinit)[idx_bus_re]
        iinit_im = np.array(dae.iinit)[idx_bus_im]

        Pinit = (vinit_re * iinit_re + vinit_im * iinit_im) * self.Sb
        Qinit = (vinit_im * iinit_re - vinit_re * iinit_im) * self.Sb

        # calculate power (P & Q) loss due to shunts
        self.build_Gsum()
        self.build_Bsum()
        iinit_shunt_re = self.Gsum * vinit_re - self.Bsum * vinit_im
        iinit_shunt_im = self.Bsum * vinit_re + self.Gsum * vinit_im

        Ploss_shunt = (vinit_re * iinit_shunt_re + vinit_im * iinit_shunt_im) * self.Sb
        Qloss_shunt = (vinit_im * iinit_shunt_re - vinit_re * iinit_shunt_im) * self.Sb

        power_flow_bus_table = pd.DataFrame(
            {
                "Bus": pd.Series(np.array(self.buses), dtype="string"),
                "V Magnitude": pd.Series(vinit_mag, dtype=float),
                "V Phase (deg)": pd.Series(vinit_phase * 180 / np.pi, dtype=float),
                "P Gen (kW)": pd.Series(Pinit, dtype=float),
                "Q Gen (kVAr)": pd.Series(Qinit, dtype=float),
                "P Shunt (kW)": pd.Series(Ploss_shunt, dtype=float),
                "Q Shunt (kVAr)": pd.Series(Qloss_shunt, dtype=float),
            }
        )

        power_flow_bus_table = tabulate(power_flow_bus_table, headers="keys")

        # ---- BRANCH RESULTS ----
        # calculate the voltage across each branch (v_from - v_to)
        self.build_incident_matrix()
        V_branch = self.incident_matrix @ dae.yinit

        # find the admittance at each branch
        y_adm_branch = np.zeros((2 * self.nb, 2 * self.nb))
        y_adm_re = -self.y_adm_matrix[self.idx_i_re, self.idx_j_re]
        y_adm_im = -self.y_adm_matrix[self.idx_i_im, self.idx_j_re]
        for k in range(self.nb):
            y_adm_branch[2 * k, 2 * k] = y_adm_re[k]
            y_adm_branch[2 * k, 2 * k + 1] = -y_adm_im[k]
            y_adm_branch[2 * k + 1, 2 * k] = y_adm_im[k]
            y_adm_branch[2 * k + 1, 2 * k + 1] = y_adm_re[k]

        # calculate the initial line currents through each branch
        ilinit = y_adm_branch @ V_branch

        idx_branch_re = [i for i in range(2 * self.nb) if i % 2 == 0]
        idx_branch_im = [i for i in range(2 * self.nb) if i % 2 != 0]

        # calculate the from_bus power injection
        Pinit_ij = (
            dae.yinit[self.idx_i_re] * ilinit[idx_branch_re]
            + dae.yinit[self.idx_i_im] * ilinit[idx_branch_im]
        ) * self.Sb
        Qinit_ij = (
            dae.yinit[self.idx_i_im] * ilinit[idx_branch_re]
            - dae.yinit[self.idx_i_re] * ilinit[idx_branch_im]
        ) * self.Sb

        # calculate the to_bus power injection
        Pinit_ji = (
            -(
                dae.yinit[self.idx_j_re] * ilinit[idx_branch_re]
                + dae.yinit[self.idx_j_im] * ilinit[idx_branch_im]
            )
            * self.Sb
        )
        Qinit_ji = (
            -(
                dae.yinit[self.idx_j_im] * ilinit[idx_branch_re]
                - dae.yinit[self.idx_j_re] * ilinit[idx_branch_im]
            )
            * self.Sb
        )

        Ploss = Pinit_ij + Pinit_ji
        Qloss = Qinit_ij + Qinit_ji

        power_flow_branch_table = pd.DataFrame(
            {
                "From Bus": [self.buses[i] for i in self.idx_i],
                "To Bus": [self.buses[j] for j in self.idx_j],
                "From Bus P (kW)": Pinit_ij,
                "From Bus Q (kVAr)": Qinit_ij,
                "To Bus P (kW)": Pinit_ji,
                "To Bus Q (kVAr)": Qinit_ji,
                "P Loss (kW)": Ploss,
                "Q Loss (kVAr)": Qloss,
            }
        )

        power_flow_branch_table = tabulate(power_flow_branch_table, headers="keys")

        print(
            "======================================================================================================="
        )
        print("Power Flow: Bus Results")
        print(
            "======================================================================================================="
        )
        print(power_flow_bus_table)
        print(
            "-------------------------------------------------------------------------------------------------------"
        )
        print(f"Total P Generation: {np.sum(Pinit)} kW")
        print(f"Total Q Generation: {np.sum(Qinit)} kVAr")
        print(f"\nTotal P Loss from shunts: {np.sum(Ploss_shunt)} kW")
        print(f"Total Q Loss from shunts: {np.sum(Qloss_shunt)} kVAr")
        print(
            "======================================================================================================="
        )
        print("Power Flow: Branch Results")
        print(
            "======================================================================================================="
        )
        print(power_flow_branch_table)
        print(
            "-------------------------------------------------------------------------------------------------------"
        )
        print(f"Total P Loss from line impedances: {np.sum(Ploss)} kW")
        print(f"Total Q Loss from line impedances: {np.sum(Qloss)} kVAr")
        print(
            "-------------------------------------------------------------------------------------------------------"
        )

    def build_Gsum(self) -> None:
        # finds the sum of the shunt conductances (g) at each node due to line parameters
        g = self.line.g

        self.Gsum = np.zeros(self.nn)
        np.add.at(self.Gsum, self.idx_i, g / 2)
        np.add.at(self.Gsum, self.idx_j, g / 2)

    def build_Bsum(self) -> None:
        # finds the sum of the shunt susceptances (b) at each node due to line parameters
        b = self.line.b

        self.Bsum = np.zeros(self.nn)
        np.add.at(self.Bsum, self.idx_i, b / 2)
        np.add.at(self.Bsum, self.idx_j, b / 2)

    def build_incident_matrix(self) -> None:
        # build incident matrix for network (+1 indicates start node; -1 indicates end node)
        self.incident_matrix = np.zeros([self.nb * 2, self.nn * 2])

        for k in range(self.nb):
            self.incident_matrix[2 * k, self.idx_i_re[k]] = 1
            self.incident_matrix[2 * k + 1, self.idx_i_im[k]] = 1
            self.incident_matrix[2 * k, self.idx_j_re[k]] = -1
            self.incident_matrix[2 * k + 1, self.idx_j_im[k]] = -1

    def setup(self, dae: DaeSim, bus_init: BusInit) -> None:

        self.build_y()
        self.init_from_power_flow(dae, bus_init)
        self.init_symbolic(dae)


class GridEst(Grid):
    def __init__(self) -> None:
        Grid.__init__(self)
        self.y_simulation = (
            []
        )  # Store voltage results from the simulation in their full time resolution

    def _init_from_simulation(self, other: GridSim, dae: Dae) -> None:

        for node in self.buses:
            self.yinit[str(node)] = other.yf[str(node)][:, round(dae.T_start / dae.t)]
        dae.yinit = np.array(list(self.yinit.values())).reshape(self.nn * 2)
        dae.iinit = self.y_adm_matrix @ dae.yinit

    def _get_results(self, other: GridSim) -> None:
        y_simulation_list = []
        for bus in self.buses:
            y_simulation_list.append(other.yf[bus])
        self.y_simulation = np.vstack(y_simulation_list)

    def setup(self, dae: DaeEst, other: GridSim) -> None:

        self.build_y()
        self._init_from_simulation(other, dae)
        self._get_results(other)
        self.init_symbolic(dae)

    def init_symbolic(self, dae: DaeEst) -> None:

        super().init_symbolic(dae)
        # Prepare measurement matrices/vectors dimensions such that real measurements can be added below
        dae.y = ca.SX.sym("y", dae.ny)
        dae.cy_meas_alg_matrix = np.empty((0, dae.ny))


class Dae:
    def __init__(self) -> None:

        # Counters
        self.nx: int = 0  # Number of differential states
        self.ny: int = 0  # Number of algebraic states
        self.ng: int = 0  # Number of algebraic equations
        self.np: int = 0  # Number of parameters/inputs (not used)
        self.nts: int = 0  # Number of time steps

        # Symbolic variables
        self.x: Optional[ca.SX] = None  # Symbolic differential states
        self.y: Optional[ca.SX] = None  # Symbolic algebraic states (voltages)
        self.f: Optional[ca.SX] = None  # Symbolic first derivatives
        self.g: Optional[ca.SX] = None  # Symbolic algebraic equations (current balance)
        self.p: Optional[ca.SX] = None  # Will be used for parameters/inputs
        self.p0: Optional[ca.SX] = None  # Will be used for parameters/inputs
        self.s: Optional[ca.SX] = None  # Switches

        # Simulation/estimation outputs
        self.x_full: Optional[np.ndarray] = None  # Differential states output
        self.y_full: Optional[np.ndarray] = None  # Algebraic states output
        self.i_full: Optional[np.ndarray] = None  # Branch currents output

        # Simulation/estimation parameters
        self.T_start: float = 0.0
        self.T_end: float = 10.0
        self.time_steps: Optional[np.ndarray] = None  # Time steps of the est/sim
        self.states: list[str] = []  # List of all states used in the model
        self.Sb: float = 100
        self.fn: Literal[50, 60] = 50
        self.t: float = 0.02

        # Initial values
        self.xinit: list = []
        self.yinit: list = []
        self.iinit: list = []
        self.sinit = np.ndarray([], dtype=float)
        self.xmin: list = []  # minimal state limiter values
        self.xmax: list = []  # maximal state limiter values
        # Store the grid as an attribute of the class
        self.grid: Optional[Grid] = None
        self.incl_lim: bool  # Include state limiters or not

        self.FG: Optional[ca.Function] = None  # Casadi function for the DAE model

    def __reduce__(self):
        # Filter the attributes based on their types
        picklable_attrs = {}
        for key, value in self.__dict__.items():
            if isinstance(value, (float, int, list, np.ndarray)):
                # Only serialize float, int, list, or numpy arrays
                picklable_attrs[key] = value

        # Return the class constructor and the picklable attributes as a tuple
        return (self.__class__, (), picklable_attrs)

    def __setstate__(self, state):
        # Restore the state from the pickled attributes
        self.__dict__.update(state)

    def setup(self, **kwargs) -> None:
        # Overwrite default values
        self.__dict__.update(kwargs)
        # Number of time steps
        self.nts = round((self.T_end - self.T_start) / self.t)
        self.time_steps = np.arange(self.T_start, self.T_end, self.t)
        self.init_symbolic()
        self.xinit = np.array(self.xinit)
        self.xmin = np.array(self.xmin)
        self.xmax = np.array(self.xmax)

    def fgcall(self) -> None:
        pass

    def init_symbolic(self) -> None:
        pass

    def dist_load(self, p: float, q: float, bus: list) -> None:
        idx_re = self.grid.get_node_index(bus)[1][0]
        idx_im = self.grid.get_node_index(bus)[2][0]
        self.g[idx_re] += (
            p / self.Sb * self.y[idx_re] + q / self.Sb * self.y[idx_im]
        ) / (self.y[idx_re] ** 2 + self.y[idx_im] ** 2)
        self.g[idx_im] += (
            p / self.Sb * self.y[idx_im] - q / self.Sb * self.y[idx_re]
        ) / (self.y[idx_re] ** 2 + self.y[idx_im] ** 2)
        self.fgcall()

    def check_disturbance(self, dist: Disturbance, iter_forward: int) -> None:
        active = dist.time <= iter_forward * self.t
        if active.any():
            for idx, state in enumerate(active):
                if state:
                    match dist.type[0]:
                        case "FAULT_LINE":
                            short_index = self.grid.get_branch_index(
                                dist.bus_i[0], dist.bus_j[0]
                            )[0][0]
                            self.grid.line_is_faulted[short_index] = True
                            self.grid.line_fault_adm[short_index] += dist.y[0]
                        case "CLEAR_FAULT_LINE":
                            short_index = self.grid.get_branch_index(
                                dist.bus_i[0], dist.bus_j[0]
                            )[0][0]
                            self.grid.line_is_faulted[short_index] = False
                        case "OPEN_LINE":
                            short_index = self.grid.get_branch_index(
                                dist.bus_i[0], dist.bus_j[0]
                            )[0][0]
                            self.grid.line_is_open[short_index] = True

                        case "LOAD":
                            self.dist_load(
                                p=dist.p_delta[0],
                                q=dist.q_delta[0],
                                bus=[dist.bus[0]],
                            )
                        case "FAULT_BUS":
                            short_index = self.grid.get_node_index([dist.bus[0]])[0][0]
                            self.grid.bus_is_faulted[short_index] = True
                            self.grid.bus_fault_adm[short_index] += dist.y[0]
                        case "CLEAR_FAULT_BUS":
                            short_index = self.grid.get_node_index([dist.bus[0]])[0][0]
                            self.grid.bus_is_faulted[short_index] = False
                        case _:
                            logging.ERROR(
                                f"Disturbance type {dist.type[0]} not found - skipped."
                            )
                            for key, value in dist._params.items():
                                dist.__dict__[key] = np.array(dist.__dict__[key][1:])
                            break
                    self.exec_dist()
                    logging.info(
                        f"Disturbance {dist.type[0]} at {dist.time[0]} successfully executed!"
                    )
                    #  Remove the executed disturbance
                    for key, value in dist._params.items():
                        dist.__dict__[key] = np.array(dist.__dict__[key][1:])

    def exec_dist(self):
        self.grid.guncall(self)
        self.grid.build_y()
        self.grid.gcall(self)
        self.fgcall()


class DaeSim(Dae):
    def __init__(self) -> None:
        super().__init__()
        self.int_scheme_sim = None
        self.eigenvalues = None
        self.t0: float  # Start of the next DAE call
        self.tf: float  # End of the next DAE call

    def init_symbolic(self) -> None:

        self.x = ca.SX.sym("x", self.nx)
        self.f = ca.SX.sym("f", self.nx)
        self.s = ca.SX.sym("s", self.nx)
        self.p = ca.SX.sym("p", self.np)
        self.p0 = np.ones(self.np)
        self.sinit = np.ones(self.nx)  # Initial values for limiters (nothing limited)

    def fgcall(self) -> None:
        dae_dict = {"x": self.x, "z": self.y, "p": self.s, "ode": self.f, "alg": self.g}
        # options = {'tf': self.t, 'print_stats': 1, 'collocation_scheme': 'radau', 'interpolation_order': 2}
        self.FG = ca.integrator("FG", self.int_scheme_sim, dae_dict, self.t0, self.tf)

    def simulate(self, dist: Disturbance) -> None:

        # Prepare for successive calls
        self.t0 = self.T_start
        self.tf = self.t
        self.fgcall()

        iter_forward = 0
        self.x_full = np.zeros([self.nx, self.nts])
        self.y_full = np.zeros([self.ny, self.nts])
        self.i_full = np.zeros([4 * self.grid.nb, self.nts])
        # set initial values
        x0 = self.xinit
        y0 = self.yinit
        s0 = self.sinit
        self.x_full[:, iter_forward] = x0
        self.y_full[:, iter_forward] = y0
        previous_value = None
        self.eigenvalue_analysis()
        if self.incl_lim:
            for time_step in range(self.nts - 1):
                iter_forward += 1
                try:
                    res = self.FG(x0=x0, z0=y0, p=s0)
                except RuntimeError:
                    logging.critical(
                        f"Simulation failed numerically at or before {iter_forward*self.t} [s]. "
                        f"Check the log to see if the system was stable at the initial point. "
                        f"Try reducing the disturbance, changing the operating point (reduce the loading), "
                        f"reducing the time step, changing the simulation solver, tuning model parameters, "
                        f"decrease the constant power loads... Good luck!"
                    )
                    raise

                x0 = res["xf"].T
                x0 = np.clip(x0, self.xmin, self.xmax)
                y0 = res["zf"].T

                self.x_full[:, iter_forward] = x0
                self.y_full[:, iter_forward] = y0
                current_value = round(iter_forward * self.t, 0)

                # Log only when the first digit after the decimal changes
                (
                    logging.info(f"Simulation time is {current_value} [s]")
                    if previous_value != current_value
                    else None
                )

                previous_value = current_value

                self.check_disturbance(dist, iter_forward)

                self.i_full[:, iter_forward] = (self.grid.C_branches @ y0.T).T

        else:

            self.x_full = x0
            self.y_full = y0
            self.x_full = self.x_full.reshape(-1, 1)
            self.y_full = self.y_full.reshape(-1, 1)

            for i in range(len(dist.time)):
                if not dist.time.any():
                    break
                tf = dist.time[0]  # Take the next disturbance event
                if tf > self.T_end:
                    continue
                self.tf = np.arange(self.t0 + self.t, tf + self.t - 1e-10, self.t)
                self.fgcall()

                try:
                    res_grid = self.FG(x0=x0, z0=y0, p=s0)
                except RuntimeError:
                    logging.critical(
                        f"Simulation failed numerically at or before time {tf}. Check the log for details. "
                        "Try reducing the disturbance, changing the operating point, "
                        "reducing the time step, or tuning model parameters."
                    )
                    raise
                logging.info(f"Simulation time is {tf} [s]")
                iter_forward = math.ceil(tf / self.t)
                xf = res_grid["xf"].full()
                yf = res_grid["zf"].full()

                self.x_full = np.hstack((self.x_full, xf))
                self.y_full = np.hstack((self.y_full, yf))
                self.check_disturbance(dist, iter_forward)

                self.t0 = self.tf[
                    -1
                ]  # set the beginning of the next interval as the end of the current interval
                x0 = xf[:, -1]  # initial value for the next interval
                y0 = yf[:, -1]  # initial value for the next interval
            # Now do the last interval
            self.tf = np.arange(self.t0 + self.t, self.T_end - 1e-10, self.t)
            self.fgcall()
            try:
                res_grid = self.FG(x0=x0, z0=y0, p=s0)
            except RuntimeError:
                logging.critical(
                    f"Simulation failed numerically at or before time {self.T_end}. Check the log for details. "
                    "Try reducing the disturbance, changing the operating point, "
                    "reducing the time step, or tuning model parameters."
                )
                raise
            xf = res_grid["xf"].full()
            yf = res_grid["zf"].full()

            self.x_full = np.hstack((self.x_full, xf))
            self.y_full = np.hstack((self.y_full, yf))
            self.i_full = self.grid.C_branches @ self.y_full

    def eigenvalue_analysis(self) -> None:

        J = ca.jacobian(ca.vertcat(self.f, self.g), ca.vertcat(self.x, self.y))
        jacobian_func = ca.Function("jacobian_func", [self.x, self.y, self.s], [J])
        Ac = jacobian_func(self.xinit, self.yinit, self.sinit)

        fx = Ac[: self.nx, : self.nx]
        fy = Ac[: self.nx, self.nx :]
        gx = Ac[self.nx :, : self.nx]
        gy = Ac[self.nx :, self.nx :]

        As = fx - fy @ ca.inv(gy) @ gx
        As = np.array(As)  # convert As casadi matrix into numpy array

        # eigenvalues = np.linalg.eigvals(As)
        # Compute eigenvalues and eigenvectors
        self.eigenvalues, right_eigenvectors = np.linalg.eig(As)
        # Compute the left eigenvectors (pseudo-inverse of right eigenvectors)
        left_eigenvectors = np.linalg.inv(right_eigenvectors).T
        # Compute participation factors
        participation_factors = np.abs(right_eigenvectors * np.conj(left_eigenvectors))

        unstable_modes = [e for e in self.eigenvalues if np.real(e) > 1e-4]
        unstable_modes_indices = [
            np.where(self.eigenvalues == mode)[0][0] for mode in unstable_modes
        ]

        unstable_modes_PFs = {}
        for i in unstable_modes_indices:
            # PF = participation_factors[:,i]
            PF = pd.DataFrame(participation_factors[i])
            PF.sort_values(0, ascending=False, inplace=True)
            unstable_modes_PFs[self.eigenvalues[i]] = {
                "state_index": PF.index.to_list(),
                "participation_factor": PF[0].to_list(),
            }
        if unstable_modes_PFs:
            logging.error(
                f"The operating point seems unstable. It has unstable modes: {unstable_modes}. "
                f"The simulation will potentially fail. Known causes: too much fix power loads, model parameter issues..."
            )


class DaeEst(Dae):
    err_msg_est = (
        "Estimation failed \n"
        "Possible reasons: \n"
        " - Not enough measurements specified \n"
        " - Initialization point very bad \n"
        " - Estimator diverged from true state \n"
        " - Check if the disturbance rendered system unestimable \n"
        "Possible solutions: \n"
        "More measurements, less noise, different disturbance, better initialization..."
    )

    def __init__(self) -> None:

        Dae.__init__(self)
        self.nm: int = 0  # Number of measurements
        # Integration scheme
        self._schemes = {
            "trapezoidal": {"kf": 0.5, "kb": 0.5},
            "forward": {"kf": 1.0, "kb": 0.0},
            "backward": {"kf": 0.0, "kb": 1.0},
        }
        # Set backward Euler as default
        self.int_scheme: str = "backward"
        self.kf: float = 0.0
        self.kb: float = 1.0

        self.filter = None
        self.unknown = None
        self.proc_noise_alg: float = 0.0001  # default value
        self.proc_noise_diff: float = 0.0001  # default value
        self.init_error_diff: float = 1.0  # default value
        self.init_error_alg: bool = False  # default value
        self.unknown_indices: list = []
        self.known_indices: list = []
        self.err_init: float = 0.001  # initial covariance matrix - default value

        # Matrices needed for calculation
        self.r_meas_noise_cov_matrix: Optional[
            np.ndarray
        ] = None  # Measurement noise covariance matrix
        self.r_meas_noise__inv_cov_matrix: Optional[
            np.ndarray
        ] = None  # Measurement noise covariance matrix
        self.q_proc_noise_diff_cov_matrix: Optional[
            np.ndarray
        ] = None  # Process noise covariance matrix
        self.q_proc_noise_alg_cov_matrix: Optional[np.ndarray] = None
        self.q_proc_noise_cov_matrix: Optional[np.ndarray] = None
        self.c_meas_matrix: Optional[np.ndarray] = None
        self.z_meas_points_matrix: Optional[np.ndarray] = None
        self.p_est_init_cov_matrix: Optional[np.ndarray] = None

        self.x0: Optional[
            np.ndarray
        ] = None  # actual initial vector of differential states
        self.y0: Optional[
            np.ndarray
        ] = None  # actual vector of initial algebraic states
        self.s0: Optional[np.ndarray] = None  # actual vector of initial switch states

        self.f_func: Optional[
            ca.Function
        ] = None  # ca.Function of differential equations
        self.g_func: Optional[ca.Function] = None  # ca.Function of algebraic equations
        self.df_dxy_jac: Optional[
            ca.Function
        ] = None  # Jacobian of differential equations
        self.dg_dxy_jac: Optional[ca.Function] = None  # Jacobian of algebraic equations

        self.inner_tol: float = (
            1e-6  # default value for the inner estimation loop tolerance
        )
        self.cov_tol: float = 1e-10  # minimal covariance matrix
        self.iter_ful: Optional[np.ndarray] = None  # Number of internal iterations
        self.time_full: Optional[np.ndarray] = None  # Time for each iteration

    @property
    def te(self):
        return self._te

    @te.setter
    def te(self, value):
        self._te = value
        self.t = value

    def find_unknown_indices(self, grid: Grid) -> None:
        # This is to remove the equations at unknown nodes
        self.unknown_indices = []
        self.unknown_indices.extend(grid.get_node_index(dae_est.unknown)[1])
        self.unknown_indices.extend(grid.get_node_index(dae_est.unknown)[2])

        self.known_indices = [i for i in range(self.ny)]
        for i in range(len(self.unknown)):
            self.known_indices.remove(grid.buses.index(dae_est.unknown[i]) * 2)
            self.known_indices.remove(grid.buses.index(dae_est.unknown[i]) * 2 + 1)

    def init_symbolic(self) -> None:

        self.x = ca.SX.sym("x", self.nx)
        self.f = ca.SX.sym("f", self.nx)
        self.s = ca.SX.sym("s", self.nx)

        self.q_proc_noise_diff_cov_matrix = np.zeros([self.nx, self.nx])
        self.r_meas_noise_cov_matrix = np.zeros([self.nm, self.nm])
        self.z_meas_points_matrix = np.zeros([self.nm, self.nts])
        self.c_meas_matrix = np.zeros([self.nm, self.nx + self.ny])
        self.sinit = np.ones(self.nx)  # Initial values for limiters (nothing limited)

    def fgcall(self) -> None:
        for dev in device_list_est:
            if dev.properties["call"]:
                dev.call(dae_est, dae_sim)
        # branch_voltage_p_m_u_est.call(dae_est, dae_sim)
        # branch_current_p_m_u_est.call(dae_est, dae_sim)
        dae_est.r_meas_noise__inv_cov_matrix = np.linalg.inv(
            dae_est.r_meas_noise_cov_matrix
        )
        self.f_func = ca.Function("f", [self.x, self.y, self.s], [self.f])
        self.df_dxy_jac = self.f_func.jacobian()
        self.g_func = ca.Function(
            "g", [self.x, self.y, self.s], [self.g[self.known_indices]]
        )
        self.dg_dxy_jac = self.g_func.jacobian()

    def _init_estimate(self) -> None:

        self.p_est_init_cov_matrix = np.eye(self.nx + self.ny) * self.err_init ** (-1)

        # set initial values
        #         err = lambda: (np.random.uniform() - 0.5) * 0.2 * config.init_error_diff
        self.x0 = self.xinit
        self.y0 = self.yinit
        self.s0 = self.sinit

        self.x_full = np.zeros([self.nx, self.nts])
        self.y_full = np.zeros([self.ny, self.nts])
        self.i_full = np.zeros([4 * self.grid.nb, self.nts])
        self.iter_full = np.zeros(
            [self.nts - 1]
        )  # 0-th state estimate is assumed known
        self.time_full = np.zeros([self.nts - 1])

        if self.init_error_alg:
            self.y0 = [1, 0] * round(self.ny / 2)

        A_jac = self.df_dxy_jac(self.x0, self.y0, self.s0, 0)
        A12x = np.array(A_jac[0])
        A12y = np.array(A_jac[1])
        A12 = np.hstack((A12x, A12y))
        ones = np.eye(self.nx, self.nx + self.ny)
        A34_jac = self.dg_dxy_jac(self.x0, self.y0, self.s0, 0)
        A34 = np.hstack((A34_jac[0], A34_jac[1]))
        obs = np.vstack((A12 + ones, A34, self.c_meas_matrix))
        if np.linalg.matrix_rank(obs) < self.nx + self.ny:
            logging.error(
                "It seems that the system is un-estimable. Check input data! Try placing more measurements!"
            )
            null = null_space(obs)  # nullspace
            un_est_nodes = self.grid.buses.copy()
            for node_idx, node in enumerate(self.grid.buses):
                if np.allclose(null[self.nx + 2 * node_idx], 0):
                    un_est_nodes.remove(node)
            logging.error(f"Un-estimable nodes are: {un_est_nodes}")
            logging.warning(
                "A good idea would be to place some PMUs around these nodes."
            )

    def estimate(self, dist: Disturbance, **kwargs) -> None:

        self.find_unknown_indices(self.grid)
        self.q_proc_noise_alg_cov_matrix = np.eye(self.grid.nn * 2) * (
            max(self.proc_noise_alg**2, self.cov_tol)
        )  # Noise for the algebraic equations
        self.q_proc_noise_diff_cov_matrix *= max(
            self.proc_noise_diff**2, self.cov_tol
        )

        self.q_proc_noise_alg_cov_matrix = np.delete(
            self.q_proc_noise_alg_cov_matrix, self.unknown_indices, 0
        )
        self.q_proc_noise_alg_cov_matrix = np.delete(
            self.q_proc_noise_alg_cov_matrix, self.unknown_indices, 1
        )
        self.q_proc_noise_cov_matrix = block_diag(
            self.q_proc_noise_diff_cov_matrix, self.q_proc_noise_alg_cov_matrix
        )
        self.ng = self.ny - 2 * (len(self.unknown))  # number of algebraic equations
        self.fgcall()
        self._init_estimate()

        self.kf = self._schemes[self.int_scheme]["kf"]
        self.kb = self._schemes[self.int_scheme]["kb"]
        x0 = self.x0
        y0 = self.y0
        s0 = self.s0
        self.x_full[:, 0] = x0
        self.y_full[:, 0] = y0
        #  Create shorter variable names
        P_cov_inv = self.p_est_init_cov_matrix
        C = self.c_meas_matrix
        Rinv = self.r_meas_noise__inv_cov_matrix
        Q = self.q_proc_noise_cov_matrix
        CRC = C.T.dot(Rinv).dot(C)
        CR = C.T.dot(Rinv)
        A34 = np.zeros([self.ng, self.nx + self.ny])
        ones = np.eye(self.nx, self.nx + self.ny)
        iter_forward = 0
        previous_value = None
        for time_step in range(self.nts - 1):
            start = time.time()
            iter_forward += 1

            x1 = x0
            y1 = y0
            s1 = s0
            A_jac = self.df_dxy_jac(x0, y0, s0, 0)
            A12x = np.array(A_jac[0] * self.t * self.kf)
            A12y = np.array(A_jac[1] * self.t * self.kf)
            A12 = np.hstack((A12x, A12y))
            A = np.vstack((A12 + ones, A34))
            Cov_L = cholesky(
                Q + A.dot(cho_solve((P_cov_inv, True), A.T, check_finite=False)),
                check_finite=False,
                lower=True,
            )
            f_d = np.zeros(self.nx)
            f_d_0 = np.zeros(self.nx)

            if self.kf != 0:  # for forward Euler and trapezoidal
                f_d_0 = np.array(self.f_func(x0, y0, s0) * self.t * self.kf)[:, 0]
            if self.kb == 0:  # for forward Euler
                E12 = np.zeros([self.nx, self.nx + self.ny])
                f_d = f_d_0

            y = self.z_meas_points_matrix[:, iter_forward]

            current_value = round(iter_forward * self.t, 0)

            # Log only when the first digit after the decimal changes
            (
                logging.info(f"Estimation time is {current_value} [s]")
                if previous_value != current_value
                else None
            )

            previous_value = current_value

            # if the value is zero, add no noise
            p_nd = (
                np.sqrt(self.q_proc_noise_diff_cov_matrix) @ np.random.randn(self.nx)
            ) * (self.proc_noise_diff != 0)
            p_na = (
                np.sqrt(self.q_proc_noise_alg_cov_matrix) @ np.random.randn(self.ng)
            ) * (self.proc_noise_alg != 0)
            p_n = np.hstack((p_nd, p_na))
            if self.filter == "iekf" or self.filter == "IEKF":
                max_inner_iter = 5
            else:
                max_inner_iter = 1
            for iter_kf in range(max_inner_iter):

                if self.kb != 0:  # for trapezoidal and backward Euler
                    E12_jac = self.df_dxy_jac(x1, y1, s1, 0)
                    E12 = np.hstack((E12_jac[0], E12_jac[1])) * self.t * self.kb

                    f_d = (
                        f_d_0
                        + np.array(self.f_func(x1, y1, s1) * self.t * self.kb)[:, 0]
                    )

                E34_jac = self.dg_dxy_jac(x1, y1, s1, 0)
                E34 = np.hstack((E34_jac[0], E34_jac[1]))

                g_d = np.array(self.g_func(x1, y1, s1))[:, 0]
                E = np.vstack((E12 - ones, E34))
                xy1 = np.hstack((x1, y1))

                Big_ = E.T.dot(cho_solve((Cov_L, True), E, check_finite=False)) + CRC

                delta_k = np.hstack((E12.dot(xy1) - x0 - f_d, E34.dot(xy1) - g_d)) + p_n

                small_ = E.T.dot(
                    cho_solve((Cov_L, True), delta_k, check_finite=False)
                ) + CR.dot(y)

                try:
                    Big_chol = cholesky(Big_, lower=True)
                except np.linalg.LinAlgError:
                    raise Exception(DaeEst.err_msg_est)

                xy1_new = cho_solve((Big_chol, True), small_, check_finite=False)
                x1_raw = xy1_new[: self.nx]
                y1 = xy1_new[self.nx : self.nx + self.ny]

                if self.incl_lim:
                    x1 = np.clip(x1_raw, self.xmin, self.xmax)
                    s1 = (x1 == x1_raw).astype(int)
                else:
                    x1 = x1_raw

                if np.max(np.abs(xy1_new - xy1)) < self.inner_tol:
                    break

            self.x_full[:, iter_forward], self.y_full[:, iter_forward] = x0, y0 = x1, y1

            P_cov_inv = Big_chol

            self.check_disturbance(dist, iter_forward)
            end = time.time()
            self.time_full[iter_forward - 1] = end - start
            self.iter_full[iter_forward - 1] = iter_kf + 1


# create the estimation grid
grid_est = GridEst()
# create the simulation grid
grid_sim = GridSim()
# initialize the DAE classes
dae_est = DaeEst()
dae_sim = DaeSim()

bus_init_sim = BusInit()
bus_unknown_est = BusUnknown()

line_sim = Line()
line_est = Line()

disturbance_sim = Disturbance()
disturbance_est = Disturbance()

device_list_sim = []
device_list_est = []


def stack_volt_power(vre, vim) -> np.ndarray:
    u_power = np.hstack((np.vstack((vre, vim)), np.vstack((vim, -vre))))
    return u_power
