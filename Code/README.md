These are codes for the modeling, analysis, and visualization of the study: 

# Code for Simulation Study

## Step 1 - calculating trunk temperatures
First, we calculate trunk temperature for each location on our domain. Using heat balance calculations, temperatures are calculated for each height above the ground under sunlit and shade conditions. The output is then saved in netcdf files. The code and more documentation for this step is in the `trunk_model` folder.

## Step 2 - simulating lizard performance with and without the ability to climb trees
Second, we calculate the operative temperature of lizards in the various microhabitats using biophysical model, and calculate lizard activity times, energy balance and performance under changing climatic conditions, with and without deforestation. The code includes options for senstivity analysis and deep model investigation that generates more output files. The code and more documentation for this step is in `lizard_model` folder.

## Step 3 - processing the raw output of the lizard simulation 
Third, we take the raw output from the lizard simulation model and calculate tables and netcdf files for model interpretation. The code and more documentation for this step in in `pre_analysis` folder.

## Step 4 - analyzing and plotting the results from the lizard simulation (TO COMPLETE LATER)
Finally, using the calculated tables and netcdf files from the previous step, we caulculate statistics and generate figures. 
### Statistical analysis
`Comparison between lab and field body temperatures.R` :Statistical comparison of field body temperatures and laboratory preferred temperatures. Also includes code for figure S3.

`Calculate_climate_change_data.R` :Code for calculating the mean increase in summer and winter temperatures by 2100 using worldclim's published global circulation models.

### Figures and Tables
`Figure 1.R`, `Figure 2.R`, `Figure 3.R`, `Figure 4.R`, `Figure 5.R`, `Figure 6.R`
`Table 1.R`, `Table S2.R`

