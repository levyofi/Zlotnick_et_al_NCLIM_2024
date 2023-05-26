These are codes for the modeling, analysis, and visualization of the study: 

# Code for Simulation Study

## Step 1 - calculating trunk temperatures
First, we calculate trunk temperature for each location on our domain. Using heat balance calculations, temperatures are calculated for each height above the ground under sunlit and shade conditions. The output is then saved in netcdf files. The code and more documentation for this step is in the `trunk_model` folder.

## Step 2 - simulating lizard performance with and without the ability to climb trees
Second, we calculate the operative temperature of lizards in the various microhabitats using biophysical model, and calculate lizard activity times, energy balance and performance under changing climatic conditions, with and without deforestation. The code includes options for senstivity analysis and deep model investigation that generates more output files. The code and more documentation for this step is in `lizard_model` folder.

## Step 3 - processing the raw output of the lizard simulation 
Third, we take the raw output from the lizard simulation model and calculate tables and netcdf files for model interpretation. The code and more documentation for this step in in `pre_analysis` folder.

## Step 4 - analyzing and plotting the results from the lizard simulation
Finally, using the calculated tables and netcdf files from the previous step, we caulculate statistics and generate figures. The code and more documentation for this step in in `final_analysis` folder.
