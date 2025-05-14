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

# The code is based on the publication: Katanic, M., Lygeros, J., Hug, G.: Recursive dynamic state estimation for power systems with an incomplete nonlinear DAE model.
# IET Gener. Transm. Distrib. 18, 3657–3668 (2024). https://doi.org/10.1049/gtd2.13308
# The full paper version is available at: https://arxiv.org/abs/2305.10065v2
# See full metadata at: README.md
# For inquiries, contact: mkatanic@ethz.ch


from matplotlib import cm
from tabulate import tabulate

from pydynamicestimator.utils import data_loader
from pydynamicestimator.config import Config
import matplotlib.pyplot as plt
import importlib
from pydynamicestimator import system
from pathlib import Path
import numpy as np
import logging
import sys
import pandas as pd
import os

# import matplotlib

# matplotlib.use("TkAgg")


def run(config: Config) -> tuple[system.DaeEst, system.DaeSim]:
    """Initialize function and run appropriate routines"""

    clear_module("pydynamicestimator.system")
    importlib.reload(system)

    # Set up logging
    logging.basicConfig(level=config.get_log_level())
    base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    simfile = base_dir / "testcases" / config.testsystemfile / "sim_param.txt"
    simdistfile = base_dir / "testcases" / config.testsystemfile / "sim_dist.txt"
    estfile = base_dir / "testcases" / config.testsystemfile / "est_param.txt"
    estdistfile = base_dir / "testcases" / config.testsystemfile / "est_dist.txt"

    with open(simfile, "rt") as fid:
        data_loader.read(fid, "sim")

    with open(simdistfile, "rt") as fid:
        data_loader.read(fid, "sim")

    with open(estfile, "rt") as fid:
        data_loader.read(fid, "est")

    with open(estdistfile, "rt") as fid:
        data_loader.read(fid, "est")

    system.grid_sim.add_lines(system.line_sim)
    system.grid_est.add_lines(system.line_est)
    # Simulation
    for item in system.device_list_sim:
        if item.properties["xy_index"]:
            item.xy_index(system.dae_sim, system.grid_sim)

    system.dae_sim.t = config.ts
    system.dae_sim.setup(**vars(config))

    system.grid_sim.setup(dae=system.dae_sim, bus_init=system.bus_init_sim)

    for item in system.device_list_sim:
        if item.properties["finit"]:
            item.finit(system.dae_sim)

    for item in system.device_list_sim:
        if item.properties["fgcall"]:
            item.fgcall(system.dae_sim)

    system.grid_sim.gcall(system.dae_sim)

    system.disturbance_sim.sort_chrono()

    system.dae_sim.simulate(system.disturbance_sim)

    system.grid_sim.save_data(system.dae_sim)
    for item in system.device_list_sim:
        if item.properties["save_data"]:
            item.save_data(system.dae_sim)

    # Estimation
    for item in system.device_list_est:
        if item.properties["xy_index"]:
            item.xy_index(system.dae_est, system.grid_est)

    system.grid_est.setup(system.dae_est, system.grid_sim)
    system.dae_est.t = config.te
    system.dae_est.setup(**vars(config))
    system.dae_est.unknown = system.bus_unknown_est.bus

    for device_est in system.device_list_est:
        if device_est.properties["finit"]:
            for idx_est in device_est.int.keys():
                device_sim = find_device_sim(idx_est)[0]
                if device_sim is not None:
                    device_est.init_from_simulation(
                        device_sim, idx_est, system.dae_est, system.dae_sim
                    )
                else:
                    logging.warning(
                        f"Estimation device index {idx_est} not found simulation data. It will be ignored and the estimation will start from default initial value"
                    )

    for item in system.device_list_est:
        if item.properties["fgcall"]:
            item.fgcall(system.dae_est)
        if item.properties["qcall"]:
            item.qcall(system.dae_est)

    system.grid_est.gcall(system.dae_est)

    system.disturbance_est.sort_chrono()

    system.dae_est.estimate(dist=system.disturbance_est)

    for item in system.device_list_est:
        if item.properties["save_data"]:
            item.save_data(system.dae_est)

    system.grid_est.save_data(system.dae_est)

    if config.plot:
        fplot(config)

    print(
        "======================================================================================================="
    )
    print("The statistics of the estimation:")
    print(
        "======================================================================================================="
    )
    print(f"Sampling time step: {(1000*system.dae_est.t)} [ms]")
    print(f"Filter: {system.dae_est.filter}")
    print(f"Discretization scheme: {system.dae_est.int_scheme}")
    print(
        f"Average computation time (per sampling step): {(1000*np.mean(system.dae_est.time_full)).round(2)} [ms]"
    )
    print(
        f"Maximal computation time (per sampling step): {(1000*np.max(system.dae_est.time_full)).round(2)} [ms]"
    )
    print(
        f"Average number of iterations (per sampling step): {np.mean(system.dae_est.iter_full).round(2)}"
    )
    print(
        f"Maximal number of iterations (over all sampling steps): {round(np.max(system.dae_est.iter_full))}"
    )

    print(
        "-------------------------------------------------------------------------------------------------------"
    )

    return system.dae_est, system.dae_sim


def fplot(config: Config):
    """Plot voltage and differential states based on configuration settings."""
    logging.basicConfig(level=logging.WARNING)  # Set logging level

    # Estimation time steps
    est_time = system.dae_est.time_steps
    # Simulation time steps
    sim_time = system.dae_sim.time_steps

    # Find closest simulation indices for each estimation time step
    closest_sim_indices = [np.argmin(np.abs(sim_time - t)) for t in est_time]

    # Plot voltage profiles if enabled
    if config.plot_voltage:

        viridis = cm.get_cmap("viridis", system.dae_est.grid.nn)
        for i, node in enumerate(system.dae_est.grid.buses):
            try:
                # Plot estimation data
                est_voltage = np.sqrt(
                    system.grid_est.yf[node][0, :] ** 2
                    + system.grid_est.yf[node][1, :] ** 2
                )
                plt.plot(
                    system.dae_est.time_steps,
                    est_voltage,
                    color=viridis(i),
                    linestyle=":",
                )
            except KeyError:
                logging.warning(f"Node {node} not estimated.")

            try:
                # Plot simulation data
                sim_voltage = np.sqrt(
                    system.grid_sim.yf[node][0, :] ** 2
                    + system.grid_sim.yf[node][1, :] ** 2
                )
                plt.plot(
                    system.dae_sim.time_steps,
                    sim_voltage,
                    color=viridis(i),
                    label=f"{node}",
                )
            except KeyError:
                logging.warning(f"Node {node} does not exist in simulation.")

        plt.legend()
        plt.title("Voltage Profiles")
        plt.xlabel("Time")
        plt.ylabel("Voltage Magnitude")
        # plt.savefig('voltage.png')

        # Dataframe for showing the error of algebraic state estimation
        error_summary = []

        for node in system.dae_est.grid.buses:
            try:

                # Estimation data
                est_real = system.grid_est.yf[node][0, :]
                est_imag = system.grid_est.yf[node][1, :]
                est_mag = np.sqrt(est_real**2 + est_imag**2)
                est_angle = np.arctan2(est_imag, est_real)

                # Simulation data at closest matching time steps
                sim_real = system.grid_sim.yf[node][0, closest_sim_indices]
                sim_imag = system.grid_sim.yf[node][1, closest_sim_indices]
                sim_mag = np.sqrt(sim_real**2 + sim_imag**2)
                sim_angle = np.arctan2(sim_imag, sim_real)

                # Errors
                mag_error = sim_mag - est_mag
                angle_error = np.unwrap(sim_angle - est_angle)

                # Metrics
                mse_mag = np.sqrt(np.mean(mag_error**2))
                mse_ang = np.sqrt(np.mean(angle_error**2))
                mae_mag = np.mean(np.abs(mag_error))
                mae_ang = np.mean(np.abs(angle_error))

                # Add to summary list
                error_summary.append(
                    {
                        "Node": node,
                        "RMSE magnitude": mse_mag,
                        "RMSE angle (rad)": mse_ang,
                        "MAE magnitude": mae_mag,
                        "MAE angle (rad)": mae_ang,
                    }
                )

            except KeyError:
                logging.warning(f"Node {node} missing in estimation or simulation.")

        # Create DataFrame from the error summary
        summary_df = pd.DataFrame(error_summary)
        summary_df.set_index("Node", inplace=True)
        summary_df = tabulate(summary_df, headers="keys")

        print(
            "======================================================================================================="
        )
        print("The errors of algebraic state estimation:")
        print(
            "======================================================================================================="
        )
        print(summary_df)
        print(
            "-------------------------------------------------------------------------------------------------------"
        )

    # Plot differential states if enabled
    if config.plot_diff:

        for device_est in system.device_list_est:
            if device_est.properties["fplot"]:

                # config.plot_machines.reverse()
                num_units = device_est.n
                num_states = device_est.ns

                # Create subplots with shared x-axis
                figure, axis = plt.subplots(
                    num_units,
                    num_states,
                    sharex=True,
                    figsize=(num_states * 5, num_units * 5),
                )
                axis = np.atleast_2d(axis)
                figure.supxlabel("Time (s)", fontsize=12)

                if "delta" in device_est.states:
                    # Align delta angles with the reference unit
                    n_est_ref = 0  # First device taken as reference angle
                    reference_est = device_est.xf["delta"][n_est_ref].copy()
                    device_sim, n_sim_ref = find_device_sim(next(iter(device_est.int)))
                    reference_sim = device_sim.xf["delta"][n_sim_ref].copy()

                for idx, n_est in device_est.int.items():
                    try:
                        device_sim, n_sim = find_device_sim(idx)

                    except ValueError as e:
                        logging.warning(
                            f"Machine {idx} not found in simulation or estimation: {e}"
                        )
                        continue
                    if "delta" in device_est.states:
                        device_sim.xf["delta"][n_sim] -= reference_sim
                        device_est.xf["delta"][n_est] -= reference_est
                    # Initialize the error summary list for states
                    state_error_summary = []
                    for col, state in enumerate(device_est.states):
                        unit = device_est.units[col]
                        t_sim = np.arange(
                            system.dae_sim.T_start,
                            system.dae_sim.T_end,
                            system.dae_sim.t,
                        )
                        t_est = np.arange(
                            system.dae_est.T_start,
                            system.dae_est.T_end,
                            system.dae_est.t,
                        )

                        try:
                            # Plot simulation data
                            axis[n_est, col].plot(
                                t_sim,
                                device_sim.xf[state][n_sim],
                            )
                            # Plot estimation data
                            axis[n_est, col].plot(
                                t_est, device_est.xf[state][n_est], linestyle=":"
                            )

                            # Label the y-axis only in the first column
                            if col == 0:
                                axis[n_est, col].set_ylabel(f"Device {idx}")

                            # Add a title to each column indicating the state
                            if n_est == 0:
                                axis[n_est, col].set_title(state)

                            # Now cfill the dataframe
                            # Matching the simulation data with the estimation time steps
                            sim_state = device_sim.xf[state][n_sim][closest_sim_indices]
                            est_state = device_est.xf[state][n_est]
                            # Compute errors: (difference between simulation and estimation)
                            state_error = sim_state - est_state

                            # Compute MSE and MAE for the state
                            mse_state = np.sqrt(np.mean(state_error**2))
                            mae_state = np.mean(np.abs(state_error))

                            # Add the results to the summary
                            state_error_summary.append(
                                {
                                    "State": state,
                                    "Unit": unit,
                                    "RMSE": mse_state,
                                    "MAE": mae_state,
                                }
                            )

                        except KeyError:
                            logging.warning(
                                f"State '{state}' not found for unit {device_est}."
                            )
                    state_error_df = pd.DataFrame(state_error_summary)
                    state_error_df.set_index("State", inplace=True)
                    state_error_df = tabulate(state_error_df, headers="keys")
                    # Display the DataFrame

                    print(
                        "======================================================================================================="
                    )
                    print(
                        f"The errors of differential states estimates of device {idx}:"
                    )
                    print(
                        "======================================================================================================="
                    )
                    print(state_error_df)
                    print(
                        "-------------------------------------------------------------------------------------------------------"
                    )

                # Adjust layout for clarity
                figure.suptitle(
                    f"Differential States of {device_est._name}", fontsize=14
                )
                plt.tight_layout(rect=[0, 0, 1, 0.95])
                # plt.savefig(f'{device_est._name}_diffstates.png')

    # Show all plots

    plt.show()


def clear_module(module_name):
    """Remove all attributes from a module, preparing it for a clean reload."""
    if module_name in sys.modules:
        module = sys.modules[module_name]
        module_dict = module.__dict__
        to_delete = [
            name
            for name in module_dict
            if not name.startswith("__")  # Avoid special and built-in attributes
        ]
        for name in to_delete:
            del module_dict[name]


def find_device_sim(idx_est):
    device_sim_found = next(
        (
            device_sim
            for device_sim in system.device_list_sim
            if any(idx_est == idx_sim for idx_sim in device_sim.int.keys())
        ),
        None,
    )
    n_sim = device_sim_found.int[idx_est] if device_sim_found else None
    return device_sim_found, n_sim
