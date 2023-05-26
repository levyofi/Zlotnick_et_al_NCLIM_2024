library(dplyr)
library(ggplot2)
library(tidyverse)

data_slicing <- function() {
  
  data <- read.csv("..\\input\\sums.csv", header = FALSE)
  
  data_df <- as.data.frame(data)
  colnames(data_df) <- c("id", "lat", "lon", "time", "climbing", "mean_ta_year", "sd_ta_year", "mean_ta_summer", "sd_ta_summer", "mean_ta_winter", "sd_ta_winter", "energy_gain_per_year", "growth_rate_per_year", "annual_activity_hours", "annual_activity_days", "first_activity_day", "last_activity_day", "length_of_activity_season", "mean_height", "std_height", "mean_height_open", "mean_height_shaded", "percentage_to_warm", "percentage_to_cool", "percentage_mixed", "percentage_on_open_tree", "percentage_on_shaded_tree", "percentage_of_essential_from_open_tree", "percentage_of_essential_from_shaded_tree")
  
  data_df$time[data_df$time == 0] <- "past"
  data_df$time[data_df$time == 1] <- "future"
  
  data_df$climbing[data_df$climbing == 0] <- "not climbing"
  data_df$climbing[data_df$climbing == 1] <- "climbing"
  
  data_df$time <- factor(data_df$time)
  data_df$climbing <- factor(data_df$climbing)
  
  
  ###### past ######
  
  past_df <- data_df[data_df$time == "past",]
  
  ## climbing ##
  
  past_climbing_df <- past_df[past_df$climbing == "climbing",]
  
  ## not climbing ##
  
  past_not_climbing_df <- past_df[past_df$climbing == "not climbing",]
  
  
  
  ###### future ######
  
  future_df <- data_df[data_df$time == "future",]
  
  ## climbing ##
  
  future_climbing_df <- future_df[future_df$climbing == "climbing",]
  
  ## not climbing ##
  
  future_not_climbing_df <- future_df[future_df$climbing == "not climbing",]
  
  
  #### writing csv files ####
  dir.create("..\\csv_files", showWarnings = FALSE)
  
  write.csv(past_climbing_df, paste("..\\csv_files\\", "past_climbing.csv", sep = "") , row.names = FALSE)
  write.csv(past_not_climbing_df, paste("..\\csv_files\\", "past_not_climbing.csv", sep = ""), row.names = FALSE)
  write.csv(future_climbing_df, paste("..\\csv_files\\", "future_climbing.csv", sep = ""), row.names = FALSE)
  write.csv(future_not_climbing_df, paste("..\\csv_files\\", "future_not_climbing.csv", sep = ""), row.names = FALSE)
  
}



