library(raster)
library(dplyr)

locations = read.csv("../lizard_model/short_past_climate_files.txt", sep="_", header = F)
names(locations) = c("id", "MIC", "CLIM", "36", "time", "lat", "lon")
locations$lon <- as.numeric(gsub(".nc", "", locations$lon))

ex = extent(min(locations$lon), max(locations$lon), min(locations$lat), max(locations$lat))
rs1 = crop(raster("../../Data/lizard_output_for_analysis/canopy_analysis/consensus_full_class_1.tif"), ex)
rs2 = crop(raster("../../Data/lizard_output_for_analysis/canopy_analysis/consensus_full_class_2.tif"), ex)
rs3 = crop(raster("../../Data/lizard_output_for_analysis/canopy_analysis/consensus_full_class_3.tif"), ex)
rs4 = crop(raster("../../Data/lizard_output_for_analysis/canopy_analysis/consensus_full_class_4.tif"), ex)

rs_total = rs1 + rs2 + rs3 + rs4
writeRaster(rs_total, filename = "../../Data/lizard_output_for_analysis/canopy_analysis/all_classes.tif", format="GTiff", overwrite = T)
plot(rs_total)

map = raster("../../Data/lizard_output_for_analysis/netcdf_files/past_climbing.nc", varname = "id")
#"map" is a raster but with no projection, let's add the projection and extent
#get projection
p = CRS("+proj=longlat +lat_1=25.0 +lat_2=45.0 +lat_0=38.0 +lon_0=-100.0 +datum=WGS84 +R=6370000 +units=m +no_defs")
#set the projection and extent of "map"
projection(map) <- p
extent(map) <- ex
veg_raster = resample(rs_total, map, method="bilinear")
plot(veg_raster)

writeRaster(veg_raster, filename = "../../Data/lizard_output_for_analysis/canopy_analysis/all_classes_model_resolution.tif", format="GTiff", overwrite = T)

sp1 <- SpatialPoints(matrix(c(locations$lon,locations$lat), ncol=2), proj4string = p)
vals = raster::extract(veg_raster, coordinates(sp1) )

locations$veg <- vals

locations_id_veg <- locations %>%
  select(c("id", "veg"))

veg_raster_above_5 <- veg_raster
veg_raster_above_5[veg_raster[] < 5] <- NA
plot(veg_raster_above_5)

veg_raster_above_10 <- veg_raster
veg_raster_above_10[veg_raster[] < 10] <- NA
plot(veg_raster_above_10)

veg_raster_above_20 <- veg_raster
veg_raster_above_20[veg_raster[] < 20] <- NA
plot(veg_raster_above_20)

# same calculation as in "important_statistics.R", but only for location with >5% tree canopy cover

data_df <- read.csv("..\\..\\Data\\lizard_output_for_analysis\\sums.csv", header = FALSE)
colnames(data_df) <- c("id", "lat", "lon", "time", "climbing", "mean_ta_year", "sd_ta_year", "mean_ta_summer", "sd_ta_summer", "mean_ta_winter", "sd_ta_winter", "energy_gain_per_year", "growth_rate_per_year", "annual_activity_hours", "annual_activity_days", "first_activity_day", "last_activity_day", "length_of_activity_season", "mean_height", "std_height", "mean_height_open", "mean_height_shaded", "percentage_to_warm", "percentage_to_cool", "percentage_mixed", "percentage_on_open_tree", "percentage_on_shaded_tree", "percentage_of_essential_from_open_tree", "percentage_of_essential_from_shaded_tree")

full_data_df <- merge(data_df, locations_id_veg, by = "id")

write.csv(full_data_df, "../../Data/lizard_output_for_analysis/canopy_analysis/sums_with_canopy_cover.csv", row.names = F)

data_df <- full_data_df %>%
  filter(veg >= 10)
print(length(unique(data_df$id)))

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

write.csv(grouped_united_melted_df, "../../Data/lizard_output_for_analysis/canopy_analysis/table1_canopy_analysis.csv", row.names = F)
