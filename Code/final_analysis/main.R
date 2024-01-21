library(ncdf4)
library(raster)
library(maptools)
library(plotrix)
library(gplots)
library(rasterVis)
library(maps)
library(RColorBrewer)
library(ggplot2)
library(dplyr)


### data editing ###

source("data_editing/data_slicing.R")
data_slicing()

source("data_editing/merging_tables.R")
merging_tables()



##### load model results that will be used for most (but not all) figures #####

data_df <- read.csv("../../Data/lizard_output_for_analysis/sums.csv", header = FALSE)
colnames(data_df) <- c("id", "lat", "lon", "time", "climbing", "mean_ta_year", "sd_ta_year", "mean_ta_summer", "sd_ta_summer", "mean_ta_winter", "sd_ta_winter", "energy_gain_per_year", "growth_rate_per_year", "annual_activity_hours", "annual_activity_days", "first_activity_day", "last_activity_day", "length_of_activity_season", "mean_height", "std_height", "mean_height_open", "mean_height_shaded", "percentage_to_warm", "percentage_to_cool", "percentage_mixed", "percentage_on_open_tree", "percentage_on_shaded_tree", "percentage_of_essential_from_open_tree", "percentage_of_essential_from_shaded_tree")


data_df <- data_df[,1:ncol(data_df)-1] %>%
  filter(id != 0)

data_df$time[data_df$time == 0] <- "past"
data_df$time[data_df$time == 1] <- "future"

data_df$climbing[data_df$climbing == 0] <- "not climbing"
data_df$climbing[data_df$climbing == 1] <- "climbing"

data_df$time <- factor(data_df$time)
data_df$climbing <- factor(data_df$climbing)


## create different mats

past_df <- data_df %>%
  filter(time == "past")

future_df <- data_df %>%
  filter(time == "future")

climbing_df <- data_df %>%
  filter(climbing == "climbing")

not_climbing_df <- data_df %>%
  filter(climbing == "not climbing")


past_c_df <- past_df %>%
  filter(climbing == "climbing")

past_nc_df <- past_df %>%
  filter(climbing == "not climbing")

future_c_df <- future_df %>%
  filter(climbing == "climbing")

future_nc_df <- future_df %>%
  filter(climbing == "not climbing")


# create directories
dir.create("results", showWarnings = FALSE)


########## figures ###########

##### main text #####

### figure 1 ###
source("figures/main/figure_1.R")
figure_1()


### figure 2 ###
source("figures/main/figure_2.R")
figure_2_facet_a(past_df)
figure_2_facet_b(past_df)
figure_2_facet_c(past_df)
figure_2_facet_d(past_df)


### figure 3 ###
source("figures/main/figure_3.R")
figure_3()


### figure 4 ###
source("figures/main/figure_4.R")
figure_4(data_df)


### figure 5 ###
source("figures/main/figure_5.R")
figure_5()



##### extended data #####

### figure E2 ###
source("figures/extended/figure_E2.R")
figure_E2()


### figure E3 ###
source("figures/extended/figure_E3.R")
figure_E3()


### figure E4 ###
source("figures/extended/figure_E4.R")
figure_E4(past_c_df)


### figure E5 ###
source("figures/extended/figure_E5.R")
figure_E5_facet_a()
figure_E5_facet_b()
figure_E5_facet_c()


### figure E6 ###
source("figures/extended/figure_E6.R")
figure_E6_facet_a()
figure_E6_facet_b()
figure_E6_facet_c()
figure_E6_facet_d(past_df)
figure_E6_facet_e(past_df)


### figure E7 ###
source("figures/extended/figure_E7.R")
figure_E7_facet_a(past_df)
figure_E7_facet_b(past_df)


### figure E8 ###
source("figures/extended/figure_E8.R")
figure_E8_facet_a()
figure_E8_facet_b()


### figure E9 ###
source("figures/extended/figure_E9.R")
figure_E9_facet_a()
figure_E9_facet_b(data_df)



##### supplementary information #####

### figure S1 ###
source("figures/supplementary/figure_S1.R")
figure_S1()


### figure S3 ###
source("figures/supplementary/figure_S3.R")
figure_S3_facet_a()
figure_S3_facet_b()


### figure S5 ###
source("figures/supplementary/figure_S5.R")
figure_S5_facet_a()
figure_S5_facet_b(climbing_df)


### figure S6 ###
source("figures/supplementary/figure_S6.R")
figure_S6()


### figure S7 ###
source("figures/supplementary/figure_S7.R")
figure_S7_facet_a()
figure_S7_facet_b(climbing_df)


### figure S8 ###
source("figures/supplementary/figure_S8.R")
figure_S8_facet_a()
figure_S8_facet_b()
figure_S8_facet_c()


### figure S9 ###
source("figures/supplementary/figure_S9.R")
figure_S9()


### figure S10 ###
source("figures/supplementary/figure_S10.R")
figure_S10()


