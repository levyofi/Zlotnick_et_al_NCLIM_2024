## Final Analysis
Here are the code files needed for statistical analysis and plotting all the figures in the paper and its supporting materials.

### Statistical analysis
To calculate the statistical description of the lizard simulation, we execute two R scripts:
- `get_stats.R` :Generated the statistical analysis for the main simulation.
- `sensitivity_analysis.R` :Generated the results of our sensitivity analysis.

The statistical description for locations with at least 10% tree canopy cover is executed in 'get_stats_for_regions_with_trees.R'.

### Figures
To create the figures, the `main.R` should be executed. This file first executes the R scripts in the `data_editing` folder and then executes the figure creation R scripts in the `figures` folder.
The figures will be created in a directory named `results`.

For successful creation of the figures, the directory (`Data/lizard_output_for_analysis`) should include the following files and directories:

- `sums.csv` (file)
- `deep_data` (directory)
- `heat_pars` (directory)
- `results_for_locations` (directory)
- `sums_for_sensitivity_analysis` (directory)
- `canopy_analysis` (directory)
- `geo_em.d01.nc` (file)
- `FVEG_monthly_past.nc` (file)
- `FVEG_monthly_future.nc` (file)

**Output:** The final edited figures used in the paper and supporting materials can be found in the 'Code/final_analysis/final_figures' directory.
