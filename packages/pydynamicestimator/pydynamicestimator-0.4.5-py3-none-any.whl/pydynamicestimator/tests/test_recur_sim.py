# Created: 2024-12-01
# Last Modified: 2025-05-12
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


# from pydynamicestimator import run
import numpy as np
from pydynamicestimator.run import run
import os
from pydynamicestimator.configs.config_standard import config
import pickle


def test_run():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sim_loc = os.path.join(base_dir, "baselines/baseline_result_sim.pkl")

    with open(sim_loc, "rb") as file:
        sim_base = pickle.load(file)
    est, sim = run(config)

    # print("rounded error is:")
    # print(np.max(sim.x_full - sim_base.x_full))
    assert np.allclose(
        sim.x_full, sim_base.x_full, atol=1e-06
    ), "The simulated results did not match the baseline"
