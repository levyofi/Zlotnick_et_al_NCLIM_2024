## Final Analysis

Below are the code files necessary for statistical analysis and creating all the figures for the paper and its supporting materials.

### Statistical Analysis

To calculate the statistical description of the lizard simulation, we run two R scripts:
- `get_stats.R`: Generates the statistical analysis for the main simulation.
- `sensitivity_analysis.R`: Produces the results of our sensitivity analysis.

The statistical description for locations with at least 10% tree canopy cover is conducted using `get_stats_for_regions_with_trees.R`.

### Figures

To create the figures, run `main.R`. This script first executes the R scripts in the `data_editing` folder, followed by the figure creation R scripts in the `figures` folder. The figures will be saved in a directory named `results`.

For successful figure creation, ensure that the directory (`Data/lizard_output_for_analysis`) contains the following files and directories:

- `sums.csv` (file)
- `deep_data` (directory)
- `heat_pars` (directory)
- `results_for_locations` (directory)
- `sums_for_sensitivity_analysis` (directory)
- `canopy_analysis` (directory)
- `geo_em.d01.nc` (file)
- `FVEG_monthly_past.nc` (file)
- `FVEG_monthly_future.nc` (file)

**Output:** The final edited figures used in the paper and supporting materials are located in the `Code/final_analysis/final_figures` directory.
