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
library(reshape2)
library(tidyr)

data_df <- read.csv("..\\input\\sums.csv", header = FALSE)
colnames(data_df) <- c("id", "lat", "lon", "time", "climbing", "mean_ta_year", "sd_ta_year", "mean_ta_summer", "sd_ta_summer", "mean_ta_winter", "sd_ta_winter", "energy_gain_per_year", "growth_rate_per_year", "annual_activity_hours", "annual_activity_days", "first_activity_day", "last_activity_day", "length_of_activity_season", "mean_height", "std_height", "mean_height_open", "mean_height_shaded", "percentage_to_warm", "percentage_to_cool", "percentage_mixed", "percentage_on_open_tree", "percentage_on_shaded_tree", "percentage_of_essential_from_open_tree", "percentage_of_essential_from_shaded_tree")

clim_df <- data_df %>%
  filter(climbing == 1)

clim_melted_df <- clim_df %>%
  group_by(id) %>%
  summarise(past_gr = first(growth_rate_per_year), future_gr = last(growth_rate_per_year), first_mty = first(mean_ta_year)) %>%
  mutate(diff_gr_clim = future_gr - past_gr)

clim_hab_df <- data_df %>%
  filter((climbing == 1 & time == 0) | (climbing == 0 & time == 1))

clim_hab_melted_df <- clim_hab_df %>%
  group_by(id) %>%
  summarise(past_gr = first(growth_rate_per_year), future_gr = last(growth_rate_per_year), first_mty = first(mean_ta_year)) %>%
  mutate(diff_gr_clim_hab = future_gr - past_gr)


united_melted_df <- merge(clim_melted_df, clim_hab_melted_df, by = "id") %>%
  select(c(1,4,5,9))

colnames(united_melted_df) <- c("id", "mean_ta", "clim_effect", "clim_hab_effect")

united_melted_df <- united_melted_df %>%
  mutate(diff = clim_hab_effect - clim_effect)

group_a <- united_melted_df %>%
  filter(clim_effect >= 0 & clim_hab_effect >= 0)

group_b <- united_melted_df %>%
  filter(clim_effect < 0 & clim_hab_effect < 0)

group_c <- united_melted_df %>%
  filter(clim_effect >= 0 & clim_hab_effect < 0)

group_d <- united_melted_df %>%
  filter(clim_effect < 0 & clim_hab_effect >= 0)

mean_ta_a <- mean(group_a$mean_ta) - 273.15
sd_ta_a <- sd(group_a$mean_ta)

print(paste("a:", mean_ta_a, "+-", sd_ta_a))

mean_diff_a <- mean(group_a$diff)
sd_diff_a <- sd(group_a$diff)

print(paste("diff     a:", mean_diff_a, "+-", sd_diff_a))

mean_clim_a <- mean(group_a$clim_effect)
sd_clim_a <- sd(group_a$clim_effect)

print(paste("clim     a:", mean_clim_a, "+-", sd_clim_a))

mean_clim_hab_a <- mean(group_a$clim_hab_effect)
sd_clim_hab_a <- sd(group_a$clim_hab_effect)

print(paste("clim_hab     a:", mean_clim_hab_a, "+-", sd_clim_hab_a))

mean_ta_b <- mean(group_b$mean_ta) - 273.15
sd_ta_b <- sd(group_b$mean_ta)

print(paste("b:", mean_ta_b, "+-", sd_ta_b))

mean_diff_b <- mean(group_b$diff)
sd_diff_b <- sd(group_b$diff)

print(paste("diff     b:", mean_diff_b, "+-", sd_diff_b))

mean_clim_b <- mean(group_b$clim_effect)
sd_clim_b <- sd(group_b$clim_effect)

print(paste("clim     b:", mean_clim_b, "+-", sd_clim_b))

mean_clim_hab_b <- mean(group_b$clim_hab_effect)
sd_clim_hab_b <- sd(group_b$clim_hab_effect)

print(paste("clim_hab     b:", mean_clim_hab_b, "+-", sd_clim_hab_b))

mean_ta_c <- mean(group_c$mean_ta) - 273.15
sd_ta_c <- sd(group_c$mean_ta)

print(paste("c:", mean_ta_c, "+-", sd_ta_c))

mean_diff_c <- mean(group_c$diff)
sd_diff_c <- sd(group_c$diff)

print(paste("diff     c:", mean_diff_c, "+-", sd_diff_c))

mean_clim_c <- mean(group_c$clim_effect)
sd_clim_c <- sd(group_c$clim_effect)

print(paste("clim     c:", mean_clim_c, "+-", sd_clim_c))

mean_clim_hab_c <- mean(group_c$clim_hab_effect)
sd_clim_hab_c <- sd(group_c$clim_hab_effect)

print(paste("clim_hab     c:", mean_clim_hab_c, "+-", sd_clim_hab_c))

mean_ta_d <- mean(group_d$mean_ta) - 273.15
sd_ta_d <- sd(group_d$mean_ta)

print(paste("d:", mean_ta_d, "+-", sd_ta_d))

mean_diff_d <- mean(group_d$diff)
sd_diff_d <- sd(group_d$diff)

print(paste("diff     d:", mean_diff_d, "+-", sd_diff_d))

# in how much locations the lizard climb mostly to warm?
warm <- data_df %>%
  filter(time == 0) %>%
  filter(percentage_to_warm > 50)

cool <- data_df %>%
  filter(time == 0) %>%
  filter(percentage_to_warm < 50)

# warm <- data_df %>%
#   filter(time == 0) %>%
#   filter(percentage_to_cool < 50)
# 
# cool <- data_df %>%
#   filter(time == 0) %>%
#   filter(percentage_to_cool > 50)



past_df <- data_df %>%
  filter(time == 0)

past_df_as <- past_df[c(1,5,6,18)]
past_df_wide <- pivot_wider(past_df_as, names_from = climbing, values_from = length_of_activity_season)
colnames(past_df_wide) <- c("id", "mean_ta_year", "not_climbing", "climbing")
past_df_wide$mean_ta_year <- as.numeric(past_df_wide$mean_ta_year) - 273.15
past_df_wide$diff <- past_df_wide$climbing - past_df_wide$not_climbing

#quantile_df <- quantile(unique(past_df_wide$mean_ta_year), c(0,0.15,0.7,0.85,1))

cold_df_as <- past_df_wide %>%
  filter(mean_ta_year <= 2)

medium_df_as <- past_df_wide %>%
  filter(mean_ta_year <= 18 & mean_ta_year > 8)
  
hot_df_as <- past_df_wide %>%
  filter(mean_ta_year > 20)


cold_mean_climbing_as <- mean(cold_df_as$climbing)
cold_sd_climbing_as <- sd(cold_df_as$climbing)

cold_mean_diff_as <- mean(cold_df_as$diff)
cold_sd_diff_as <- sd(cold_df_as$diff)

print(paste("cold: ", cold_mean_climbing_as, "+-", cold_sd_climbing_as, "     ", cold_mean_diff_as, "+-", cold_sd_diff_as))


medium_mean_climbing_as <- mean(medium_df_as$climbing)
medium_sd_climbing_as <- sd(medium_df_as$climbing)

medium_mean_diff_as <- mean(medium_df_as$diff)
medium_sd_diff_as <- sd(medium_df_as$diff)

print(paste("medium: ", medium_mean_climbing_as, "+-", medium_sd_climbing_as, "     ", medium_mean_diff_as, "+-", medium_sd_diff_as))


hot_mean_climbing_as <- mean(hot_df_as$climbing)
hot_sd_climbing_as <- sd(hot_df_as$climbing)

hot_mean_diff_as <- mean(hot_df_as$diff)
hot_sd_diff_as <- sd(hot_df_as$diff)

print(paste("hot: ", hot_mean_climbing_as, "+-", hot_sd_climbing_as, "     ", hot_mean_diff_as, "+-", hot_sd_diff_as))

other_df_as <- past_df_wide %>%
  filter(mean_ta_year > 2)

other_mean_climbing_as <- mean(other_df_as$climbing)
other_sd_climbing_as <- sd(other_df_as$climbing)

other_mean_diff_as <- mean(other_df_as$diff)
other_sd_diff_as <- sd(other_df_as$diff)

print(paste("other: ", other_mean_climbing_as, "+-", other_sd_climbing_as, "     ", other_mean_diff_as, "+-", other_sd_diff_as))


past_temp_df <- past_df %>%
  filter(climbing == 0)
past_temp_df <- past_temp_df[c(1,6)]
past_temp_df$mean_ta_year <- past_temp_df$mean_ta_year - 273.15

quantile_df <- quantile(unique(past_temp_df$mean_ta_year), c(0,0.33333,0.66667,1))

low_df <- past_temp_df %>%
  filter(mean_ta_year <= quantile_df[2])

med_df <- past_temp_df %>%
  filter(mean_ta_year <= quantile_df[3] & mean_ta_year > quantile_df[2])

high_df <- past_temp_df %>%
  filter(mean_ta_year > quantile_df[3])

mean_low_ta <- mean(low_df$mean_ta_year)
sd_low_ta <- sd(low_df$mean_ta_year)

print(paste("low: ", mean_low_ta, "+-", sd_low_ta))

mean_med_ta <- mean(med_df$mean_ta_year)
sd_med_ta <- sd(med_df$mean_ta_year)

print(paste("med: ", mean_med_ta, "+-", sd_med_ta))

mean_high_ta <- mean(high_df$mean_ta_year)
sd_high_ta <- sd(high_df$mean_ta_year)

print(paste("high: ", mean_high_ta, "+-", sd_high_ta))


