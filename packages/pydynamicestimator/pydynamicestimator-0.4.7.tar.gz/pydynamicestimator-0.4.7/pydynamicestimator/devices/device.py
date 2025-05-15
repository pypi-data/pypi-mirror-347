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
from typing import TYPE_CHECKING, Union, Any, Optional

if TYPE_CHECKING:
    from pydynamicestimator.system import Dae, Grid, DaeEst, DaeSim
import casadi as ca
import numpy as np
import logging


np.random.seed(30)
sin = np.sin
cos = np.cos
sqrt = np.sqrt


class Element:
    """Metaclass to be used for all elements to be added"""

    def __init__(self) -> None:
        self.n: int = 0  # number of devices
        self.u: list[bool] = []  # device status
        self.name: list[str] = []  # name of the device
        self._type: Optional[str] = None  # Device type
        self._name: Optional[str] = None  # Device name
        self.int: dict[
            str, Union[str, int]
        ] = (
            {}
        )  # Dictionary of unique identifiers for each device based on the variable "idx"
        self._data: dict[str, Any] = {"u": True}  # Default entries for lists
        self._params: dict[str, float] = {}  # Default entries for np.arrays params
        self._setpoints: dict[
            str, float
        ] = {}  # Default entries for np.arrays set points
        self._descr: dict[str, str] = {}  # Parameter and data explanation
        self._mand: list[str] = []  # mandatory attributes
        self.properties: dict[str, bool] = {
            "gcall": False,
            "fcall": False,
            "xinit": False,
            "fgcall": False,
            "qcall": False,
            "call": False,
            "xy_index": False,
            "finit": False,
            "save_data": False,
            "fplot": False,
        }

    def add(
        self, idx: Optional[str] = None, name: Optional[str] = None, **kwargs
    ) -> None:
        """
        Add an element device

        Args:
        idx (str, optional): Unique identifier for the device. Generated if not provided.
        name (str, optional): Name of the device. Generated if not provided.
        **kwargs: Custom parameters to overwrite defaults.
        """
        # Generate unique identifiers if not provided
        idx = idx or f"{self._type}_{self.n + 1}"
        name = name or f"{self._name}_{self.n + 1}"

        self.int[idx] = self.n
        self.name.append(name)

        # check whether mandatory parameters have been set up

        for key in self._mand:
            if key not in kwargs:
                raise Exception("Mandatory parameter <%s> has not been set up" % key)
        self.n += 1
        # Set default values
        for key, default in {**self._params, **self._setpoints}.items():
            if key not in self.__dict__:
                logging.warning(
                    f"Attribute {key} not found in element - initializing as an empty array."
                )
                self.__dict__[key] = np.array([], dtype=type(default))
            self.__dict__[key] = np.append(self.__dict__[key], default)

        for key, default in self._data.items():
            if key not in self.__dict__:
                logging.warning(
                    f"Attribute {key} not found in element - initializing as an empty list."
                )
                self.__dict__[key] = []
            self.__dict__[key].append(default)

        # Overwrite custom values

        for key, value in kwargs.items():

            if key not in self.__dict__:
                logging.warning(
                    "Element %s does not have parameter %s - ignoring"
                    % (self._name, key)
                )
                continue
            try:
                self.__dict__[key][-1] = value  # Attempt to update the last element
            except IndexError:
                raise IndexError(
                    f"Parameter/setpoint '{key}' not properly specified in the model definition. Check if it's properly listed and initialized when defining the class"
                )

        logging.info(f"Element {name} (ID: {idx}) added successfully.")


class BusInit(Element):
    def __init__(self) -> None:
        super().__init__()
        self._type = "Bus_init_or_unknwon"  # Element type
        self._name = "Bus_init_or_unknown"  # Element name
        self._data.update({"bus": None, "p": 0, "q": 0, "v": 1.0, "type": None})
        self.bus: list[Optional[str]] = []
        self.p: list[float] = []
        self.q: list[float] = []
        self.v: list[float] = []
        self.type: list[Optional[str]] = []


BusUnknown = BusInit  # Alias class name


class Disturbance(Element):
    def __init__(self) -> None:
        super().__init__()
        self._type = "Disturbance"  # Element type
        self._name = "Disturbance"  # Element name
        # Default parameter values
        self._params.update(
            {
                "bus_i": None,
                "bus_j": None,
                "time": None,
                "type": None,
                "y": 10,
                "bus": None,
                "p_delta": 0,
                "q_delta": 0,
            }
        )

        self.type = np.array([], dtype=str)
        self.time = np.array([], dtype=float)
        self.bus_i = np.array([], dtype=str)
        self.bus_j = np.array([], dtype=str)
        self.y: np.ndarray = np.array([], dtype=float)
        self.bus = np.array([], dtype=str)
        self.p_delta = np.array([], dtype=float)
        self.q_delta = np.array([], dtype=float)

    def sort_chrono(self):
        sorted_indices = np.argsort(self.time)

        for key in self._params:
            setattr(self, key, getattr(self, key)[sorted_indices])


class Line(Element):
    r"""
    Parameters
    ----------
    r : ndarray[float]
        Series resistance value in per unit (p.u.).
    x : ndarray[float]
        Series reactance value in per unit (p.u.).
    g : ndarray[float]
        Total shunt conductance value in per unit (p.u.).
    b : ndarray[float]
        Total shunt susceptance value in per unit (p.u.).
    trafo : ndarray[float]
        Off-nominal line transformer ratio.
    bus_i : ndarray[str]
        Name of the sending-end bus.
    bus_j : ndarray[str]
        Name of the receiving-end bus.
    """

    def __init__(self) -> None:
        super().__init__()

        self._type = "Transmission_line"  # Element type
        self._name = "Transmission_line"  # Element name
        self._params.update(
            {
                "r": 0.001,
                "x": 0.001,
                "g": 0,
                "b": 0,
                "bus_i": None,
                "bus_j": None,
                "trafo": 1,
            }
        )
        self.r = np.array([], dtype=float)
        self.x = np.array([], dtype=float)
        self.g = np.array([], dtype=float)
        self.b = np.array([], dtype=float)
        self.trafo = np.array([], dtype=float)
        self.bus_i = np.array([], dtype=object)
        self.bus_j = np.array([], dtype=object)


class DeviceRect(Element):
    """
    Dynamic or static device modeled in rectangular coordinates. Used as a parent class
    for all devices modeled in rectangular coordinates.

    Attributes:
        properties (dict[str, bool]): Flags for method calls (e.g., 'gcall', 'fcall').
        xf (dict[str, np.ndarray]): Final state results for simulation/estimation.
        xinit (dict[State, list[float]]): Initial state values for all devices of the instance.
        xmin (list[float]): Minimum limited state value.
        xmax (list[float]): Maximum limited state value.
        _params (dict[str, float]): Device parameters, such as rated voltage, power, and frequency and internal parameters.
        _data (dict[str, str]): Additional data which will be used in a list, one entry for each device of this object instance.
        bus (list[Optional[str]]): Buses where the device is connected. Each device has an entry in the list.
        states (list[States]): State variables.
        units (list[States]): Units of state variables.
        ns (float): Total number of states in the model.
        _states_noise (dict[States, float]): Noise for each state variable.
        _states_init_error (dict[States, float]): Initial error for each state variable.
        vre (list[float]): Order of the real voltage value for each device in the overall DAE model.
        vim (list[float]): Order of the real voltage value for each device in the overall DAE model.
        _algebs (list[str]): Algebraic variables ('vre', 'vim').
        _descr (dict[str, str]): Descriptions for key parameters.
    """

    def __init__(self) -> None:

        super().__init__()

        self.xf: dict[str, np.ndarray] = {}  # final state results or sim/est
        self.xinit: dict[str, list[float]] = {}
        self.xmin: list[float] = []
        self.xmax: list[float] = []

        self._params.update({"Vn": 220, "fn": 50.0, "Sn": 100})
        self.Vn = np.array([], dtype=float)
        self.fn = np.array([], dtype=float)
        self.Sn = np.array([], dtype=float)

        self._data.update({"bus": None})
        self.bus: list[Optional[str]] = []  # at which bus

        self.states: list[str] = []  # list of state variables
        self.units: list[str] = []  # List of states' units
        self.ns: int = 0  # number of states
        self._states_noise: dict[
            str, float
        ] = {}  # list of noises for every state variable (only for estimation)
        self._states_init_error: dict[
            str, float
        ] = {}  # list of initial errors for every state variable (only for estimation)
        self._algebs: list[str] = ["vre", "vim"]  # list of algebraic variables
        self.vre = np.array([], dtype=float)
        self.vim = np.array([], dtype=float)

        self._x0: dict[
            str, float
        ] = (
            {}
        )  # default initial states, will be used as initial guess for the simulation initialization
        self._mand.extend(["bus"])
        self._descr = {
            "Sn": "rated power",
            "Vn": "rated voltage",
            "u": "connection status",
            "fn": "nominal frequency",
        }

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Merge class-level _descrs if subclass adds its own
        full_descr = dict(getattr(cls, "_descr", {}))
        for base in cls.__bases__:
            full_descr.update(getattr(base, "_descr", {}))

        # Format as docstring section
        doc_lines = ["\nAttributes", "----------"]
        for key, val in full_descr.items():
            doc_lines.append(f"{key} : np.ndarray")
            doc_lines.append(f"    {val}")

        # Inject into class docstring
        cls.__doc__ = (cls.__doc__ or "") + "\n" + "\n".join(doc_lines)

    def _init_data(self) -> None:

        self.xinit = {state: [] for state in self.states}

    def xy_index(self, dae: Dae, grid: Grid) -> None:
        """Initializes indices for states, algebraic variables, unknown inputs, and switches.

        Args:
            dae (Dae): Object managing differential-algebraic equations.
            grid (Grid): Object managing the electrical grid and node indices.
        """

        zeros = [0] * self.n
        for item in self.states:
            self.__dict__[item] = zeros[:]
        for item in self._algebs:
            self.__dict__[item] = zeros[:]

        for var in range(self.n):

            for item in self.states:
                self.__dict__[item][var] = dae.nx
                # Init with current state init value
                dae.xinit.append(self.xinit[item][var])
                # Add the corresponding state to the DAE
                dae.states.append(f"{self._name}_at_{self.bus[var]}_{item}")
                dae.nx += 1
                # Retrieve min and max state limits
                item_min = getattr(self, item + "_min", None)
                item_max = getattr(self, item + "_max", None)
                self.xmin.append(item_min[var] if item_min is not None else -np.inf)
                self.xmax.append(item_max[var] if item_max is not None else np.inf)
                dae.xmin.append(item_min[var] if item_min is not None else -np.inf)
                dae.xmax.append(item_max[var] if item_max is not None else np.inf)
        if self.n:
            # assign indices to real and imaginary voltage algebraic variables; first real value
            self.__dict__["vre"] = grid.get_node_index(self.bus)[1]
            self.__dict__["vim"] = grid.get_node_index(self.bus)[2]

    def add(self, idx=None, name=None, **kwargs) -> None:

        super().add(idx, name, **kwargs)

        # initialize initial states with some default values
        for item in self.states:
            self.xinit[item].append(self._x0[item])

    def init_from_simulation(
        self, device_sim: DeviceRect, idx: str, dae: DaeEst, dae_sim: DaeSim
    ) -> None:
        """Initialize the device state estimation based on simulation results.

        Args:
            device_sim (DeviceRect): The device simulation object containing simulation results.
            idx (str): unique index of the device
            dae (DaeEst): The DAE object responsible for managing the estimation of the system.
            dae_sim (DaeSim): The simulation object providing timing information.
        """

        var_sim = device_sim.int.get(idx)
        var_est = self.int.get(idx)

        # Initial states of estimation as true states obtained through simulation
        for item in self.states:
            # Init with simulated value
            try:
                self.xinit[item][var_est] = device_sim.xf[item][
                    var_sim, round(dae.T_start / dae_sim.t)
                ]
            except KeyError:
                logging.error(
                    f"Failed to initialize state {item}. State not found in simulation model."
                )
                continue
            # Add noise for the init state
            noise = (
                self._states_init_error[item]
                * (np.random.uniform() - 0.5)
                * dae.init_error_diff
            )
            dae.xinit[self.__dict__[item][var_est]] = self.xinit[item][var_est] + noise

        # Set setpoint values based on simulation
        for item, value in self._setpoints.items():
            if item in device_sim.__dict__:
                self.__dict__[item][var_est] = device_sim.__dict__[item][var_sim]
            else:
                logging.warning(
                    f"Setpoint {item} not found in simulation test cases. Skipping. It will be ignored and the estimation will start from default initial value"
                )

    def save_data(self, dae: Dae) -> None:

        for item in self.states:
            self.xf[item] = np.zeros([self.n, dae.nts])
            self.xf[item][:, :] = dae.x_full[self.__dict__[item][:], :]

    def finit(self, dae: Dae) -> None:
        """Initialize the device by setting up setpoints, initial states based on the power flow solution.
        Args:
            dae (Dae): The DAE object used to simulate the system.
        """

        u = ca.SX.sym("", 0)
        u0 = []
        for item in self._setpoints:
            # Set the initial guess for the setpoint
            u0.append(self.__dict__[item])

            # Reset it to be a variable
            self.__dict__[item] = ca.SX.sym(item, self.n)
            # Stack the variable to a single vector
            u = ca.vertcat(u, self.__dict__[item])
        u0 = [item for sublist in u0 for item in sublist]  # flatten it

        # Now subtract the initial network currents from algebraic equations
        for alg in self._algebs:
            dae.g[self.__dict__[alg]] += dae.iinit[self.__dict__[alg]]

        # Algebraic variables are now not symbolic but their init values
        dae.y = dae.yinit.copy()
        dae.s = np.ones(dae.nx)
        self.fgcall(dae)
        # Find the indices of differential equations for this type of generator
        diff = [self.__dict__[arg] for arg in self.states]
        diff_index = [item for sublist in np.transpose(diff) for item in sublist]

        inputs = [ca.vertcat(dae.x[diff_index], u)]
        outputs = [
            ca.vertcat(
                dae.f[diff_index],
                dae.g[self.__dict__["vre"]],
                dae.g[self.__dict__["vim"]],
            )
        ]

        device_init = ca.Function("h", inputs, outputs)
        newton_init = ca.rootfinder("G", "newton", device_init)

        x0 = np.array(list(self._x0.values()) * self.n)

        solution = newton_init(ca.vertcat(x0, u0))
        solution = np.array(solution).flatten()

        # # Init only these states
        # for s in self.states:
        #     self.xinit[s] = list(solution[self.__dict__[s]])

        index = 0  # emma: rewrote 2 lines above so that more than just synchronous generators could be included in the simulation (otherwise the indexing is not done properly)
        for s in self.states:
            locat = []
            for n in range(self.n):
                locat.append(n * len(self.states) + index)
            self.xinit[s] = solution[locat]
            index += 1

        for idx, s in enumerate(self._setpoints):
            setpoint_range_start = (len(self.states) + idx) * self.n
            changed_setpoints = (
                u0[idx * self.n : (idx + 1) * self.n]
                != solution[setpoint_range_start : setpoint_range_start + self.n]
            )
            for i in range(self.n):
                if changed_setpoints[i]:
                    logging.warning(
                        f"Setpoint {s} updated in device {self._name} at node {self.bus[i]} from {u0[idx*self.n + i]} to {solution[setpoint_range_start+i]} to match the initial power flow!"
                    )
            self.__dict__[s] = solution[
                setpoint_range_start : setpoint_range_start + self.n
            ]

        # Now load the initial states into DAE class such that simulation/estimation actually starts from those values
        dae.xinit[diff_index] = solution[: len(self.states) * self.n]

        # Reset the algebraic equations such that they can be used "erneut" from scratch once the "fgcall" is called
        dae.g *= 0
        # Reset the voltages to being again symbolic variables
        dae.y = ca.SX.sym("y", dae.ny)
        dae.s = ca.SX.sym("s", dae.nx)

        2 == 2

    def fgcall(self, dae: Dae) -> None:
        """
        A method that executes the differential and algebraic equations of the model
        and adds them to the appropriate places in the Dae class

        :param dae: an instance of a class Dae

        :type dae:

        :return: None

        :rtype: None
        """
        pass

    def qcall(self, dae: DaeEst) -> None:
        for item in self.states:
            dae.q_proc_noise_diff_cov_matrix[
                self.__dict__[item], self.__dict__[item]
            ] = (self._states_noise[item]) ** 2
