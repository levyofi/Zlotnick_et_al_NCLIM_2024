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

data_df <- read.csv("../../Data/lizard_output_for_analysis/sums.csv", header = FALSE)
colnames(data_df) <- c("id", "lat", "lon", "time", "climbing", "mean_ta_year", "sd_ta_year", "mean_ta_summer", "sd_ta_summer", "mean_ta_winter", "sd_ta_winter", "energy_gain_per_year", "growth_rate_per_year", "annual_activity_hours", "annual_activity_days", "first_activity_day", "last_activity_day", "length_of_activity_season", "mean_height", "std_height", "mean_height_open", "mean_height_shaded", "percentage_to_warm", "percentage_to_cool", "percentage_mixed", "percentage_on_open_tree", "percentage_on_shaded_tree", "percentage_of_essential_from_open_tree", "percentage_of_essential_from_shaded_tree")

clim_df <- data_df %>%
  filter(climbing == 1)

clim_df <- clim_df[order(clim_df$time),]

clim_melted_df <- clim_df %>%
  group_by(id) %>%
  summarise(past_gr = first(growth_rate_per_year), future_gr = last(growth_rate_per_year), first_mty = first(mean_ta_year)) %>%
  mutate(diff_gr_clim = future_gr - past_gr)

clim_hab_df <- data_df %>%
  filter((climbing == 1 & time == 0) | (climbing == 0 & time == 1))

clim_hab_df <- clim_hab_df[order(clim_hab_df$time),]

clim_hab_melted_df <- clim_hab_df %>%
  group_by(id) %>%
  summarise(past_gr = first(growth_rate_per_year), future_gr = last(growth_rate_per_year), first_mty = first(mean_ta_year)) %>%
  mutate(diff_gr_clim_hab = future_gr - past_gr)



united_melted_df <- merge(clim_melted_df, clim_hab_melted_df, by = "id") %>%
  select(c(1,4,5,9))

colnames(united_melted_df) <- c("id", "mean_ta", "clim_effect", "clim_hab_effect")

united_melted_df$group <- "blue"

united_melted_df$group[united_melted_df$clim_effect >= 0 & united_melted_df$clim_hab_effect >= 0] <- "green"
united_melted_df$group[united_melted_df$clim_effect < 0 & united_melted_df$clim_hab_effect < 0] <- "red"
united_melted_df$group[united_melted_df$clim_effect >= 0 & united_melted_df$clim_hab_effect < 0] <- "yellow"

grouped_united_melted_df <- united_melted_df %>%
  group_by(group) %>%
  summarise(percentage = round((n() / nrow(united_melted_df)), 3) * 100, 
            average_mean_ta = round(mean(mean_ta) - 273.15,2),
            sd_ta = round(sd(mean_ta),2),
            mean_clim_effect = round(mean(clim_effect),2),
            sd_clim_effect = round(sd(clim_effect),2),
            mean_clim_hab_effect = round(mean(clim_hab_effect),2),
            sd_clim_hab_effect = round(sd(clim_hab_effect),2))

write.csv(grouped_united_melted_df, "../../Data/lizard_output_for_analysis/table1.csv", row.names = F)


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


# calculations of statistics for section "the impact of tree loss", paragraph 2 
# (changes in activity season due to tree loss)

past_df_as <- past_df[c(1,5,6,18)]
past_df_wide <- pivot_wider(past_df_as, names_from = climbing, values_from = length_of_activity_season)
colnames(past_df_wide) <- c("id", "mean_ta_year", "not_climbing", "climbing")
past_df_wide$mean_ta_year <- as.numeric(past_df_wide$mean_ta_year) - 273.15
past_df_wide$diff <- past_df_wide$climbing - past_df_wide$not_climbing



cold_df_as <- past_df_wide %>%
  filter(mean_ta_year <= 2)

print(paste0("cold percentage: ", round(nrow(cold_df_as)/nrow(past_df_wide),3) * 100))

medium_df_as <- past_df_wide %>%
  filter(mean_ta_year <= 18 & mean_ta_year > 8)

print(paste0("medium percentage: ", round(nrow(medium_df_as)/nrow(past_df_wide),3) * 100))
  
hot_df_as <- past_df_wide %>%
  filter(mean_ta_year > 20)

print(paste0("hot percentage: ", round(nrow(hot_df_as)/nrow(past_df_wide),3) * 100))


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



# calculations of statistics for section "the impact of tree loss", paragraph 2 (division as in figure 1)
# (changes in activity season due to tree loss)

past_df_as <- past_df[c(1,5,6,18)]
past_df_wide <- pivot_wider(past_df_as, names_from = climbing, values_from = length_of_activity_season)
colnames(past_df_wide) <- c("id", "mean_ta_year", "not_climbing", "climbing")
past_df_wide$mean_ta_year <- as.numeric(past_df_wide$mean_ta_year) - 273.15
past_df_wide$diff <- past_df_wide$climbing - past_df_wide$not_climbing

quantile_df <- quantile(unique(past_df_wide$mean_ta_year), c(0,0.33333,0.66667,1))

cold_df_as <- past_df_wide %>%
  filter(mean_ta_year <= quantile_df[2])

medium_df_as <- past_df_wide %>%
  filter(mean_ta_year <= quantile_df[3] & mean_ta_year > quantile_df[2])

hot_df_as <- past_df_wide %>%
  filter(mean_ta_year > quantile_df[3])


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
  filter(mean_ta_year > quantile_df[2])

other_mean_climbing_as <- mean(other_df_as$climbing)
other_sd_climbing_as <- sd(other_df_as$climbing)

other_mean_diff_as <- mean(other_df_as$diff)
other_sd_diff_as <- sd(other_df_as$diff)

print(paste("other: ", other_mean_climbing_as, "+-", other_sd_climbing_as, "     ", other_mean_diff_as, "+-", other_sd_diff_as))


# calculations of statistics for section "the impact of tree loss", paragraph 2 (division to 3 unequal groups)
# (changes in activity season due to tree loss)

past_df_as <- past_df[c(1,5,6,18)]
past_df_wide <- pivot_wider(past_df_as, names_from = climbing, values_from = length_of_activity_season)
colnames(past_df_wide) <- c("id", "mean_ta_year", "not_climbing", "climbing")
past_df_wide$mean_ta_year <- as.numeric(past_df_wide$mean_ta_year) - 273.15
past_df_wide$diff <- past_df_wide$climbing - past_df_wide$not_climbing

quantile_df <- quantile(unique(past_df_wide$mean_ta_year), c(0,0.1,0.9,1))

cold_df_as <- past_df_wide %>%
  filter(mean_ta_year <= quantile_df[2])

cold_mean_ta <- mean(cold_df_as$mean_ta_year)
cold_sd_ta <- sd(cold_df_as$mean_ta_year)
print(paste("cold (ta): ", cold_mean_ta, "+-", cold_sd_ta))


medium_df_as <- past_df_wide %>%
  filter(mean_ta_year <= quantile_df[3] & mean_ta_year > quantile_df[2])

medium_mean_ta <- mean(medium_df_as$mean_ta_year)
medium_sd_ta <- sd(medium_df_as$mean_ta_year)
print(paste("medium (ta): ", medium_mean_ta, "+-", medium_sd_ta))

hot_df_as <- past_df_wide %>%
  filter(mean_ta_year > quantile_df[3])

hot_mean_ta <- mean(hot_df_as$mean_ta_year)
hot_sd_ta <- sd(hot_df_as$mean_ta_year)
print(paste("hot (ta): ", hot_mean_ta, "+-", hot_sd_ta))


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
  filter(mean_ta_year > quantile_df[2])

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







