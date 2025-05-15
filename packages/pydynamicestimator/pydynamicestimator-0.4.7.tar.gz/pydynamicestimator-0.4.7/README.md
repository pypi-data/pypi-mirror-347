<div align="center">

# PowerDynamicEstimator

*a Dynamic State Estimator for Power Systems*

</div>

<div align="center">

  <!-- Button to GitLab Pages Documentation -->
   [![View Documentation](https://img.shields.io/badge/View%20Documentation-Docs-blue?logo=gitlab)](https://powerdynamicestimator-34b372.pages.nccr-automation.ch/index.html)  <!-- Button to Paper DOI -->
  [![View Paper](https://img.shields.io/badge/View%20Paper-DOI-green?logo=doi)](https://doi.org/10.1049/gtd2.13308)

</div>

---
## About

`PowerDynamicEstimator` is a dynamic state estimation (DSE) tool for power systems modeled by nonlinear Differential-Algebraic Equations (DAEs). 
It is based on the Iterated Extended Kalman Filter (IEKF) and combines dynamic evolution equations, algebraic network equations, and phasor measurements to recursively estimate dynamic and algebraic states. It is especially suitable for centralized power systems DSE, when some component models are missing or unknown.

## Features

- Simultaneous dynamic and algebraic (nodal voltage) states estimation
- Supports nonlinear DAE power system models
- Works with missing or unknown component models (unknown injectors)
- Supports bounds (limits) on differential states
- Supports explicit (forward Euler) and implicit (backward Euler and trapezoidal rule) integration schemes
- Supports 50 Hz and 60 Hz systems
- Configurable as Extended Kalman Filter (EKF) for fast execution or Iterated Extended Kalman Filter (IEKF) for more accurate estimation
- Possible to simulate any power system topology
- Easy to configure Kalman filter settings
- User-defined dynamic and static models can be integrated.



## Installation

To get started with `PowerDynamicEstimator`, follow these steps:
### Option 1: Install from Source (with `venv`)

1. **Clone the repository**:
```bash
git clone https://gitlab.nccr-automation.ch/mkatanic/powerdynamicestimator
cd PowerDynamicEstimator
```
2. **Create and activate a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate 
```

3. **Install Dependencies**:
```bash
pip install -r requirements.txt
```
### Option 2: Install from Source (with `conda`)

1. **Clone the repository**:
```bash
git clone https://gitlab.nccr-automation.ch/mkatanic/powerdynamicestimator
cd PowerDynamicEstimator
```

2. **Create the** `conda` **environment**:

```bash
conda env create -f environment.yaml
conda activate pydynamicestimator
```

### Option 3: Install from PyPI

```bash
pip install pydynamicestimator
```

## Documentation

Full documentation is available online at:

👉 https://powerdynamicestimator-34b372.pages.nccr-automation.ch/

Alternatively, the documentation following the Sphinx standard and can be found locally by opening `./docs/build/html/index.html` from the root folder:

### Windows:
```bash
start docs/build/html/index.html
```
### Linux:
```bash
xdg-open docs/build/html/index.html
```
### macOS:
```bash
open docs/build/html/index.html
```


## Usage

### Running the Estimator

1. **Navigate to the root directory**:
```bash
cd pydynamicestimator
```

2. **Run the main script**:
```bash
python -m main
```
## Examples 

You can check out the available examples in `./examples` directory and get started with the estimator. See the docu for more details about the test cases.

### Basic Usage

An interactive demo showcasing how to use the `PowerDynamicEstimator` package is available on **Google Colab**:

[![Colab](https://img.shields.io/badge/Open%20in-Colab-blue?logo=googlecolab)](https://colab.research.google.com/drive/1u-m-o1VAeVyGNhuiSxBSsSqbA4nnHNC2?usp=sharing)



### IEEE 39 bus with renewables

The test case includes grid-forming and grid-following converters.


[![Colab](https://img.shields.io/badge/Open%20in-Colab-blue?logo=googlecolab)](https://colab.research.google.com/drive/1sUQwF4o5_yPRAlJi-WzXZf6YywnOhCW-?usp=sharing)


## Important Notes

- **Injector Limitation**: Currently, the system supports only one injector per node due to initialization ambiguity. To handle multiple injectors per node, you can create a new node connected via a branch with very small impedance to simulate this behavior.

### Parameters

System dynamic and static parameters, including the topology, are specified in the `./data` subfolder. You can define the loads, generators, and their characteristics at specific nodes in the power system. Refer to the documentation for additional details.

Phasor Measurement Units (PMUs) used for estimation and their associated characteristics are defined in the file: `./data/.../est_param.txt`.

### Kalman Filter Settings

Adjust parameters related to the recursive state estimation process (e.g., noise covariance, initial error) in the `./config.py` file. Refer to the documentation for additional details.

## Acknowledgments
`PowerDynamicEstimator` was developed at [Power Systems Laboratory](https://psl.ee.ethz.ch/) at [ETH Zurich](https://ethz.ch/en.html). This work was supported as a part of [NCCR Automation](https://nccr-automation.ch/), a National Centre of Competence in Research, funded by the Swiss National Science Foundation (grant number 51NF40_225155).

If you use `PowerDynamicEstimator` in your research, please cite the following paper:
- **Katanic, Milos, Lygeros, John, Hug, Gabriela**. "Recursive dynamic state estimation for power systems with an incomplete nonlinear DAE model." *IET Generation, Transmission & Distribution*, 18(22), 3657-3668, 2024.  
  DOI: [https://doi.org/10.1049/gtd2.13308](https://doi.org/10.1049/gtd2.13308)
```bibtex
@article{powerdynamicestimator,
  author = {Katanic, Milos and Lygeros, John and Hug, Gabriela},
  title = {Recursive dynamic state estimation for power systems with an incomplete nonlinear DAE model},
  journal = {IET Generation, Transmission \& Distribution},
  volume = {18},
  number = {22},
  pages = {3657-3668},
  keywords = {differential algebraic equations, Kalman filters, state estimation},
  doi = {https://doi.org/10.1049/gtd2.13308}, 
  url = {https://ietresearch.onlinelibrary.wiley.com/doi/abs/10.1049/gtd2.13308},
  eprint = {https://ietresearch.onlinelibrary.wiley.com/doi/pdf/10.1049/gtd2.13308},
  year = {2024}
}
```
Some proofs were omitted due to page limitation. Full version of the paper is available on [ArXiv](https://arxiv.org/abs/2305.10065v2).


## Version

**Version 0.4.7** released on 14.05.2025  
[DOI: 10.5905/ethz-1007-842](https://doi.org/10.5905/ethz-1007-842)

## License

This software is licensed under the [GNU General Public License v3.0 (GPL-3.0)](https://www.gnu.org/licenses/gpl-3.0.html).


## Contact
For any questions or if you desired to contribute to this project, please contact me at mkatanic@ethz.ch.
