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

source("data_editing\\data_slicing.R")
data_slicing()

source("data_editing\\merging_tables.R")
merging_tables()



data_df <- read.csv("..\\input\\sums.csv", header = FALSE)
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
dir.create("..\\results", showWarnings = FALSE)


###### figures #####

### figure 1 ###
source("figures\\figure_1.R")
figure_1()


### figure 2 ###
source("figures\\figure_2.R")
figure_2_facet_a(past_df)
figure_2_facet_b(past_df)
figure_2_facet_c(past_df)
figure_2_facet_d(past_df)


### figure 3 ###
source("figures\\figure_3.R")
figure_3()


### figure 4 ###
source("figures\\figure_4.R")
figure_4()


### figure 5 ###
source("figures\\figure_5.R")
figure_5_facet_a()
figure_5_facet_b()


### figure 6 ###
source("figures\\figure_6.R")
figure_6(data_df)


### figure 7 ###
source("figures\\figure_7.R")
figure_7()


### figure S2 ###
source("figures\\figure_S2.R")
figure_S2_facet_a()
figure_S2_facet_b()
figure_S2_facet_c()


### figure S3 ###
source("figures\\figure_S3.R")
figure_S3()


### figure S4 ###
source("figures\\figure_S4.R")
figure_S4()


### figure S5 ###
source("figures\\figure_S5.R")
figure_S5()


### figure S7 ###
source("figures\\figure_S7.R")
figure_S7(past_c_df)


### figure S8 ###
source("figures\\figure_S8.R")
figure_S8_facet_a()
figure_S8_facet_b()


### figure S10 ###
source("figures\\figure_S10.R")
figure_S10()


### figure S11 ###
source("figures\\figure_S11.R")
figure_S11_facet_a()
figure_S11_facet_b()
figure_S11_facet_c()
figure_S11_facet_d(past_df)
figure_S11_facet_e(past_df)


### figure S12 ###
source("figures\\figure_S12.R")
figure_S12_facet_a(past_df)
figure_S12_facet_b(past_df)


### figure S13 ###
source("figures\\figure_S13.R")
figure_S13_facet_a()
figure_S13_facet_b(climbing_df)


### figure S14 ###
source("figures\\figure_S14.R")
figure_S14_facet_a()
figure_S14_facet_b(climbing_df)


### figure S15 ###
source("figures\\figure_S15.R")
figure_S15_facet_a()
figure_S15_facet_b()
figure_S15_facet_c()

