# Lizard Model

The Lizard Model is a biophysical model that predicts lizard performance under changing climatic conditions with an hourly resolution. Our model calculates the potential body temperature of lizards in various micro-environments within their habitat and predicts their preferred locations. Additionally, the model computes the energy balance of lizards, which can be used to estimate population growth rates.

The primary model used for this study processes 20 years of hourly climatic data across 10,303 locations in North America. This model can be run using the Python file: `Code/lizard_model/Main/__init__.py`.

Since the model accepts arguments and utilizes MPI, it is recommended to run this file through a Linux terminal or Windows CMD, using the following command:
```
mpiexec -np 36 python -m mpi4py __init__.py -a 0 -b 0
```
Arguments `a` and `b` are for sensitivity analysis, where `a` represents the parameter to be altered, and `b` indicates the relative change or the new value of this parameter. For basic usage of the model, set both arguments to 0 to retain original parameter values.

**Output:** The model generates a single CSV file named `sums.csv`. To create plots, this file should be copied to `Code/codes_for_plots/input`. An example of this file is available in `Data/lizard_raw_output`.

## Additional Simulation Modes

We have also utilized two additional modes for in-depth analysis of the model results:

### Detailed Locations' Analysis 

In this mode, the model is executed for specific locations (default settings include 3 locations in Arizona, New Jersey, and Colorado, as described in the paper). This mode yields more detailed output, enabling further exploration of daily thermoregulation patterns in lizards.

To run the model in this mode, use the Python file: `Code/lizard_model/Main_by_locations/__init__.py` (not necessarily via terminal or cmd).

**Output:** 

1. A directory containing multiple subdirectories, each leading to a CSV file for every scenario (location X time period X tree availability). For plot creation, rename this directory to `results_for_locations` and move it to `Code/codes_for_plots/input`.

2. Detailed outputs of various heat exchange components during a typical day. Some calculations are performed manually, and their outputs are stored in `Data/lizard_output_for_analysis/heat_pars`. For plot creation, move this directory to `Codes/codes_for_plots/input`.

### Deeper Output Generation 

This mode runs the standard model but generates significantly more data. Due to its high demands on memory, time, and storage, it should only be used when necessary.

To activate this mode, uncomment the lines under "## additional information - about climbing" at the end of `Code/lizard_model/Summary/__init__.py`, and run the model as previously described.

**Output:** 

In addition to the standard `sums.csv` file, this mode produces a directory with a CSV file for each location, named `climbing_info_files`. To analyze these outputs, transfer both the `sums.csv` file and the directory to `Code/codes_for_plots/pre_analysis/input`, then execute the three Python files in `Code/pre_analysis` sequentially as per their prefixes.

The output from these scripts is a directory named `deep_data`. To generate certain figures, copy this `deep_data` directory to `Code/codes_for_plots/input`.
