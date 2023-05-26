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

dir_path <- "../input/sums_for_sensitivity_analysis/"

normal <- read.csv(paste0(dir_path,"sums.csv"), header = FALSE)
activity_temp_range_05 <- read.csv(paste0(dir_path,"sums_activity_temp_range_0.5.csv"), header = FALSE)
activity_temp_range_15 <- read.csv(paste0(dir_path,"sums_activity_temp_range_1.5.csv"), header = FALSE)
emergence_min_05 <- read.csv(paste0(dir_path,"sums_emergence_min_0.5.csv"), header = FALSE)
emergence_min_15 <- read.csv(paste0(dir_path,"sums_emergence_min_1.5.csv"), header = FALSE)
food_supply_05 <- read.csv(paste0(dir_path,"sums_food_supply_0.5.csv"), header = FALSE)
food_supply_15 <- read.csv(paste0(dir_path,"sums_food_supply_1.5.csv"), header = FALSE)
mass_05 <- read.csv(paste0(dir_path,"sums_mass_0.5.csv"), header = FALSE)
mass_15 <- read.csv(paste0(dir_path,"sums_mass_1.5.csv"), header = FALSE)
lizard_color_value_065 <- read.csv(paste0(dir_path,"sums_lizard_color_value_0.65.csv"), header = FALSE)

sums <- list(normal,
             activity_temp_range_05,
             activity_temp_range_15,
             emergence_min_05,
             emergence_min_15,
             food_supply_05,
             food_supply_15,
             mass_05,
             mass_15,
             lizard_color_value_065)

sums_names <- c("normal",
                "activity_temp_range_05",
                "activity_temp_range_15",
                "emergence_min_05",
                "emergence_min_15",
                "food_supply_05",
                "food_supply_15",
                "mass_05",
                "mass_15",
                "lizard_color_value_065")

columns <- c("id", "lat", "lon", "time", "climbing", "mean_ta_year", "sd_ta_year", "mean_ta_summer", "sd_ta_summer", "mean_ta_winter", "sd_ta_winter", "energy_gain_per_year", "growth_rate_per_year", "annual_activity_hours", "annual_activity_days", "first_activity_day", "last_activity_day", "length_of_activity_season", "mean_height", "std_height", "mean_height_open", "mean_height_shaded", "percentage_to_warm", "percentage_to_cool", "percentage_mixed", "percentage_on_open_tree", "percentage_on_shaded_tree", "percentage_of_essential_from_open_tree", "percentage_of_essential_from_shaded_tree", "nan")


var_of_interest <- "growth_rate_per_year"

df_for_csv <- data.frame(matrix(ncol = 8, nrow = 0))

for(j in 1:length(sums)){
  
  rel_df <- sums[[j]]
  colnames(rel_df) <- columns
  
  sum_name <- sums_names[[j]]
  cat(paste(sum_name,"\n", sep = ""))
  
  rel_df$mean_ta_year <- rel_df$mean_ta_year - 273.15
  
  past_df <- rel_df %>%
    filter(time == 0)
  
  quantile_df <- quantile(unique(past_df$mean_ta_year), c(0,0.33,0.67,1))
  
  names <- c("cold", "med", "hot")
  col_i <- c(0,33,67,100)
  
  
  
  for(i in 1:3){
    
    name <- names[[i]]
    
    min <- quantile_df[[i]]
    max <- quantile_df[[i+1]]
    
    spec_df <- rel_df %>%
      filter((mean_ta_year >= min) & (mean_ta_year < max))
    
    climbing_df <- spec_df %>%
      filter(climbing == 1) %>%
      group_by(id) %>%
      summarise(first_c_gr = first(growth_rate_per_year), last_c_gr = last(growth_rate_per_year), first_mty = first(mean_ta_year)) %>%
      mutate(diff_c_gr = last_c_gr - first_c_gr)
    
    
    big_rel_df <- merge(spec_df, climbing_df, by = c("id"))
    
    not_climbing_df <- spec_df %>%
      filter(climbing == 0) %>%
      group_by(id) %>%
      summarise(first_nc_gr = first(growth_rate_per_year), last_nc_gr = last(growth_rate_per_year)) %>%
      mutate(diff_nc_gr = last_nc_gr - first_nc_gr)
    
    
    big_rel_df <- merge(big_rel_df, not_climbing_df, by = c("id"))
    big_rel_df <- big_rel_df %>%
      mutate(future_contribution = last_c_gr - last_nc_gr) %>%
      mutate(hab_loss_diff = first_nc_gr - first_c_gr) %>%
      mutate(hab_loss_climate_change_diff = last_nc_gr - first_c_gr) %>%
      mutate(climate_change_diff = last_c_gr - first_c_gr)
    
    mean_future_contribution <- round(mean(big_rel_df$future_contribution),2)
    sd_future_contribution <- round(sd(big_rel_df$future_contribution),2)
    mean_hab_loss_diff <- round(mean(big_rel_df$hab_loss_diff),2)
    sd_hab_loss_diff <- round(sd(big_rel_df$hab_loss_diff),2)
    mean_hab_loss_climate_change_diff <- round(mean(big_rel_df$hab_loss_climate_change_diff),2)
    sd_hab_loss_climate_change_diff <- round(sd(big_rel_df$hab_loss_climate_change_diff),2)
    mean_climate_change_diff <- round(mean(big_rel_df$climate_change_diff),2)
    sd_climate_change_diff <- round(sd(big_rel_df$climate_change_diff),2)
    
    
    cat(paste(name, ":", "\n", 
              "mean future contribution: ",as.character(mean_future_contribution), "\n",
              "sd future contribution: ", as.character(sd_future_contribution), "\n",
              "mean hab loss diff: ", as.character(mean_hab_loss_diff), "\n",
              "sd hab loss diff: ", as.character(sd_hab_loss_diff), "\n",
              "mean hab loss climate change diff: ", as.character(mean_hab_loss_climate_change_diff), "\n",
              "sd hab loss climate change diff: ", as.character(sd_hab_loss_climate_change_diff), "\n",
              "mean climate change diff: ", as.character(mean_climate_change_diff), "\n",
              "sd climate change diff: ", as.character(sd_climate_change_diff), "\n", sep = ""))
    
    row <- c(sum_name,name,mean_future_contribution, sd_future_contribution,
             mean_hab_loss_diff, sd_hab_loss_diff, mean_hab_loss_climate_change_diff,
             sd_hab_loss_climate_change_diff, mean_climate_change_diff,
             sd_climate_change_diff)
    
    df_for_csv <- rbind(df_for_csv, row)
    
    
  }
  
}

colnames(df_for_csv) <- c("sum_name","group","mean_future_contribution", "sd_future_contribution",
                          "mean_hab_loss_diff", "sd_hab_loss_diff", "mean_hab_loss_climate_change_diff",
                          "sd_hab_loss_climate_change_diff", "mean_climate_change_diff",
                          "sd_climate_change_diff")

write.csv(df_for_csv, "../results/sensitivity_analysis_results.csv")





































































