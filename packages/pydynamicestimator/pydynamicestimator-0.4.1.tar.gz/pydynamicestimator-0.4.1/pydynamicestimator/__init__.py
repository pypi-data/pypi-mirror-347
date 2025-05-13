from importlib.metadata import version

__version__ = version("pydynamicestimator")  # Must match the name in pyproject.toml


def help() -> None:
    """
    Prints an overview of the pydynamicestimator package and usage instructions.
    """
    print(
        r"""
    📦 pydynamicestimator — Recursive Dynamic State Estimation
    ----------------------------------------------------------
    This package implements algorithms from:

    Katanic, M., Lygeros, J., Hug, G. (2024). Recursive dynamic state estimation
    for power systems with an incomplete nonlinear DAE model.
    IET Gener. Transm. Distrib. 18, 3657–3668.
    DOI: https://doi.org/10.1049/gtd2.13308
    arXiv: https://arxiv.org/abs/2305.10065v2

    🔧 Key Modules:
    - run.py       : Simulation/estimation execution
    - system.py      : DAE system model


    🚀 Usage:
    >>> import pydynamicestimator
    >>> pydynamicestimator.help()

    🧾 License:
    GNU General Public License v3.0 (GPL-3.0)
    https://www.gnu.org/licenses/gpl-3.0.en.html

    ℹ️ More Info:
    GitLab: https://gitlab.nccr-automation.ch/mkatanic/powerdynamicestimator
    Contact: mkatanic@ethz.ch
    """
    )
