# Zlotnick_et_al_2023
 
In this github repository, we present all codes used in our study, including:

1) an energy-balance model for calculation of tree trunks temperatures (Code/trunk_model)

2) biophysical model for prediction of lizard performance under changing climatic conditions (Code/lizard_model)

3) a list of codes used to produce the plots for the published paper, and to calculate important statistics (Code/codes_for_plots)

Instructions for using each of these models / codes is presented below.
For any questions or comments, please contact us via mail at omerzlotnick@gmail.com.


### Trunk model ###

Ofir - fill it up


### Lizard model ###

The lizard model is a biophysical model predicting lizard performance under changing climatic conditions in resolution of 1 hour.
Our model calculates the potential body temperature of the lizard in different micro-environments in the habitat, and predict where the lizard will choose to be.
The model also calculates the lizard energy balance, that can later be used to calculate the population growth rate.

The main model we used for this study run over 20 years of hourly climatic data for 10303 locations in north-america.
This model can be executed via the python file: Code/lizard_model/Main/__init__.py. 
As the model accepts arguments, and uses mpi, it is recommended to execute this file via linux terminal or windows cmd, using the executation line:

> mpiexec -np 36 python -m mpi4py __init__.py -a 0 -b 0

Arguments a and b are used for sensitivity analysis, when a eccepts the parameter we want to change, and b the relative change / the new value for this parameter.
For the basic use of the model, both arguments should be 0 (that way, all parameters hold their original values).

output: one csv file named sums.csv
for creating the plots, this fil needs to be copied to the directory Code/codes_for_plots/input


For further investigation of the model results, we also used 2 additional modes:

# specific locations #

In this version, we run the model on spcific locations (default is 3 locations ar Arizona, New-Jersey and Colorado).
This mode produces more information as output, enabling us to further explore the daily thermoregulation patterns of the lizard.
For executing the model in this mode, use the python file: Code/lizard_model/Main_by_locations/__init__.py (not necessarily via terminal or cmd).

output: a directory with multiple sub-directories leading to a csv file for each possible scenario (location X time period X with / without trees availability)
for creating the plots, this directory must be named "results_for_locations" in the directory Code/codes_for_plots/input

under this mode we also produced a deep analysis of the different heat exchange components during a typical day,
the results from this half-computed, half-manual analysis, were saved in the directory heat_pars, that should be moved to Codes/codes_for_plots/input.

# deep data exploration #

In this version, we run the normal model, but produce a lot more data as output.
This version is very memory, time and storage consuming, and therefor should only be used if necessary.
To use this mode, expose the comment written under "## additional information - about climbing" at the end of the python file:
Code/lizard_model/Summary/__init__.py, and run the model as described above (in the normal version)

output: one csv file named sums.csv (as in the regular version), and a directory with multiple csv files called "climbing_info_files.
Both the sums.csv file and the directory should be tranfered to Code/codes_for_plots/pre_analysis/input, then they could be analyzed using the 3 python files, 
executed one after the other according to their prefixes. 

The output of this pre-analysis, a directory named deep_data, should be later copied to Code/codes_for_plots/input, for creating some of the plots.


### codes for plots ###

All codes needed for plotting any of the plots appear in the paper and its supporting materials can be found in the directory Codes/codes_for_plots/R_files.
The R file Code/codes_for_plots/R_files/main.R calls different R files, each creates a different plot from the paper.

For all plots to be produced successflly, the input directory (Codes/codes_for_plots/input) should include:
- sums.csv (file)
- deep_data (directory)
- heat_pars (directory)
- results_for_locations (directory)
- geo_em.d01.nc (file)
- FVEG_monthly_past.nc (file)
- FVEG_monthly_future.nc (file)


output: all plots used in the paper and appendix, organised in the Codes/codes_for_plots/results directory.

Hope you'd benefit from our model, 
Omer Zlotnick and Ofr Levy


