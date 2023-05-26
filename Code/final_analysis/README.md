## Final Analysis
Here are the code files needed for statistical analysis and plotting all of the figures in the paper and its supporting materials.
### Statistical analysis
To calculate the statistical description of the lizard simulation, we execute two R scripts:
- `important_statistics.R` :Generated the statistical analysis for the main simulation.
- `sensitivity_analysis.R` :Generated the results of our sensitivity analysis.

### Figures
To create the figures, the `main.R` should be executed. This file first executes the R scripts in the `data_editing` folder and then executes the figure creation R scripts located in the `figures` folder.

For a successful creaition of the figures, the input directory (`Codes/codes_for_plots/input`) should include the files in `Data/lizard_output_for_analysis`:

- `sums.csv` (file)
- `deep_data` (directory)
- `heat_pars` (directory)
- `results_for_locations` (directory)
- `geo_em.d01.nc` (file)
- `FVEG_monthly_past.nc` (file)
- `FVEG_monthly_future.nc` (file)

**Output:** All figures used in the paper and appendix, organised in the `Codes/codes_for_plots/results` directory.
