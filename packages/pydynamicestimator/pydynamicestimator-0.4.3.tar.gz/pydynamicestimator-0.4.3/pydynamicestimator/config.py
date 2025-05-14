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

from typing import Any
from typing import Literal
import logging
from pydantic import BaseModel

IntegrationSchemaEst = Literal["backward", "trapezoidal", "forward"]
IntegrationSchemeSim = Literal["idas", "collocation"]

Frequency = Literal[50, 60]
Filter = Literal["iekf", "ekf"]
Levels = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Config(BaseModel):
    """
    Configuration class used to store all relevant attributes for the execution of
    simulation and estimation.
    """

    testsystemfile: str
    fn: Frequency  # 50 or 60
    Sb: int  # parameters in .txt table are assumed to be given for 100 MW
    # General input data
    ts: float  # Simulation time step
    te: float  # Estimation time step
    T_start: float  # It has to be 0.0
    T_end: float

    filter: Filter
    int_scheme: IntegrationSchemaEst
    int_scheme_sim: IntegrationSchemeSim

    init_error_diff: float  # 0.5 = 5%; 1.0 = 10% etc.
    init_error_alg: bool  # 1 = flat start; 0 = true values

    plot: bool
    plot_voltage: bool
    plot_diff: bool

    proc_noise_alg: float  # Base level of algebraic equations noise
    proc_noise_diff: float  # Base level of differential equations noise
    incl_lim: bool

    log_level: Levels

    def updated(self, **kwargs: Any) -> "Config":
        """
          All keyword arguments listed below are optional and can be used to customize the configuration.

        :param testsystemfile: The path to the system test case.
        :type testsystemfile: str

        :param fn: System frequency (currently only tested for 50 Hz).
        :type fn: float

        :param Sb: Base power of the grid in [MW]. Line parameters are assumed to be calculated using this base power.
        :type Sb: float

        :param ts: Simulation time step.
        :type ts: float

        :param te: Estimation time step. Must be greater than or equal to the simulation time step.
        :type te: float

        :param T_start: Estimation start time (must currently be 0).
        :type T_start: float

        :param T_end: End time of the simulation/estimation.
        :type T_end: float

        :param int_scheme: Integration scheme for the estimation. Must be `'trapezoidal'` or `'backward'`.
        :type int_scheme: str

        :param init_error_diff: Estimation initialization error for differential states. E.g., `1.0` corresponds to 10% error.
        :type init_error_diff: float

        :param init_error_alg: Whether to use a flat start (`True`) or true values (`False`) for initialization.
        :type init_error_alg: bool

        :param plot: Enable or disable plotting.
        :type plot: bool

        :param plot_voltage: Whether to plot voltage data.
        :type plot_voltage: bool

        :param plot_diff: Whether to plot differential state data.
        :type plot_diff: bool

        :param proc_noise_alg: Process noise for the algebraic equations. Default is `1e-3`.
        :type proc_noise_alg: float

        :param proc_noise_diff: Process noise for the differential equations. Default is `1e-4`.
        :type proc_noise_diff: float

        :param incl_lim: If state limiters should be included in the simulation and the estimation. If `False`, the simulation will be much faster.
        :type incl_lim: bool

        :returns: A new instance of the :class:`Config` class configured with the provided parameters.
        :rtype: Config
        """
        return self.model_copy(update=kwargs)

    def get_log_level(self):
        """Returns the log level."""
        valid_levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        return valid_levels[self.log_level]


config = Config(
    testsystemfile="IEEE39_bus",
    fn=50,
    Sb=100,  # parameters in .txt table are assumed to be given for 100 MW
    ts=0.005,  # Simulation time step
    te=0.02,  # Estimation time step
    T_start=0.0,  # It has to be 0.0
    T_end=15.0,
    int_scheme="backward",
    int_scheme_sim="idas",
    # ###initialize estimation##########
    init_error_diff=1,  # 0.5 = 5%; 1.0 = 10% etc.
    init_error_alg=True,  # 1 = flat start; 0 = true values
    # #########Plot###############
    plot=True,
    plot_voltage=True,
    plot_diff=True,
    proc_noise_alg=1e-3,
    proc_noise_diff=1e-4,
    filter="iekf",
    log_level="WARNING",
    incl_lim=False,
)
