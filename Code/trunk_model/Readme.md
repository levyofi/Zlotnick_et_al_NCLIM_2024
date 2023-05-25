# Trunk temperature model

Here, we publish the code for calculating the trunk temperatures. The different files are:
- `air_density.R` :Code to calculate air density
- `convective_heat_trans.R` :Code to calculate the convective heat transfer on the tree trunk.
- `create_ncdf_function.R` :Code to save the output of the model in netcdf format.
- `solar_partition.R` :Code to calculate the direct and diffuse solar radiations that reach the trunk. 
- `trunk_temperature_model_parallel.R` : Code to read the input files, run in parrallel (each location in a different CPU) and calculate the temperature of a sunlit and shaded tree trunk for each hour of the dataset and each height above the ground.

# Model input

The input files for the model should be located in a single folder. Here, we show files for 3 location in our simulation domain. The files are found in `Data/trunk_sample_input_data`. The folder should also include the `inputs.txt` file, listing the locations to run, and the `locations.txt` file, listing the coordinate and elevation of each location in our domain.

