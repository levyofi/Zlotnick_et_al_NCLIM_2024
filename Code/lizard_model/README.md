# Lizard Model

The lizard model is a biophysical model predicting lizard performance under changing climatic conditions with a resolution of 1 hour. Our model calculates the potential body temperature of the lizard in different micro-environments in the habitat, and predicts where the lizard will choose to be. The model also calculates the lizard energy balance, which can later be used to calculate the population growth rate.

The main model used for this study runs over 20 years of hourly climatic data for 10,303 locations in North-America. This model can be executed via the Python file: `Code/lizard_model/Main/__init__.py`.

As the model accepts arguments and uses MPI, it is recommended to execute this file via Linux terminal or Windows CMD, using the execution line:
```
mpiexec -np 36 python -m mpi4py __init__.py -a 0 -b 0
```
Arguments `a` and `b` are used for sensitivity analysis, where `a` accepts the parameter we want to change, and `b` the relative change / the new value for this parameter. For the basic use of the model, both arguments should be 0 (that way, all parameters hold their original values).

**Output:** A single CSV file named `sums.csv`. For creating the plots, this file needs to be copied to the directory `Code/codes_for_plots/input`. An example of this file can be found in `Data/lizard_raw_output`.

## Additional Simulation Modes

For further investigation of the model results, we also used two additional modes:

### Detailed locations' analysis 

In this version, we run the model on specific locations (default is 3 locations in Arizona, New-Jersey, and Colorado as described in the paper). This mode produces more information as output, enabling us to further explore the daily thermoregulation patterns of the lizard.

For executing the model in this mode, use the Python file: `Code/lizard_model/Main_by_locations/__init__.py` (not necessarily via terminal or cmd).

**Output:** 

1. A directory with multiple sub-directories leading to a CSV file for each possible scenario (location X time period X with / without trees availability). For creating the plots, this directory should be named `results_for_locations` and moved to the directory `Code/codes_for_plots/input`.

2. A detailed output of the different heat exchange components during a typical day. Some of the calculations were done manually and the output was saved in in the directory `Data/lizard_output_for_analysis/heat_pars`. For creating the plots, this directory should be moved to `Codes/codes_for_plots/input`.

### Deeper Output Generation 

In this version, we run the normal model but produce a lot more data as output. This version is very memory, time and storage consuming, and therefore should only be used if necessary.

To use this mode, uncomment the lines written under "## additional information - about climbing" at the end of the Python file: `Code/lizard_model/Summary/__init__.py`, and run the model as described above (in the normal version).

**Output:** 

In addition to the default `sums.csv` output file (as in the regular version), this mode generated a directory a CSV file for each location called `climbing_info_files`. To analyze these outputs, both the `sums.csv` file and the directory should be transferred to `Code/codes_for_plots/pre_analysis/input`, and the 3 Python files in `Code/pre_analysis` should be executed one after the other according to their prefixes.

The output of these python scripts is a directory named `deep_data`. To create some of the figures, this `deep_data` directory should be copied to `Code/codes_for_plots/input`.

