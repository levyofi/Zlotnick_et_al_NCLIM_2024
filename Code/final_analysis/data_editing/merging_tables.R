library(dplyr)
library(ggplot2)
library(tidyverse)
library(ncdf4)

merging_tables <- function() {
  
  geo_em <- nc_open("../../Data/lizard_output_for_analysis/geo_em.d01.NC")
  
  netcdf_lons <- ncvar_get(geo_em, "XLONG_M")
  netcdf_lats <- ncvar_get(geo_em, "XLAT_M")
  
  netcdf_lons <- netcdf_lons[,30:129]
  netcdf_lats <- netcdf_lats[,30:129]
  
  
  landmask <- ncvar_get(geo_em, "LANDMASK")
  landmask <- landmask[,30:129]
  
  cases <- c("past_climbing", "past_not_climbing", "future_climbing", "future_not_climbing")
  dir.create("../../Data/lizard_output_for_analysis/netcdf_files", showWarnings = FALSE)
  
  for(case in cases){
    
    rel_df <- read.csv(paste("../../Data/lizard_output_for_analysis/csv_files/", case,".csv", sep = ""))
    
    num_of_coordinates <- nrow(rel_df)
    
    sum_lats_all <- rel_df$lat
    sum_lons_all <- rel_df$lon
    
    
    lats_index <- rep(0, num_of_coordinates)
    lons_index <- rep(0, num_of_coordinates)
    
    for(i in 1:num_of_coordinates){
      for(y in 1:ncol(netcdf_lats)){
        for(x in 1:nrow(netcdf_lats)){
          
          if ((abs(sum_lats_all[i] - netcdf_lats[x,y]) < 0.001) & (abs(sum_lons_all[i] - netcdf_lons[x,y]) < 0.001)){
            lats_index[i] <- y
            lons_index[i] <- x
          }
        }
      }
      
      if (lats_index[i] == 0){
        print(paste("couldn't find lat/lon for coordinate", i, sum_lats_all[i], sum_lons_all[i], sep = ""))
      }
    }
    
    rel_df <- rel_df %>%
      mutate(netcdf_lats = lats_index) %>%
      mutate(netcdf_lons = lons_index)
    
    nlats <- ncol(netcdf_lats)
    nlons <- nrow(netcdf_lats)
    
    id_mat <- matrix(-10000, nlons, nlats)
    lat_mat <- matrix(-10000, nlons, nlats)
    lon_mat <- matrix(-10000, nlons, nlats)
    mean_ta_year_mat <- matrix(-10000, nlons, nlats)
    sd_ta_year_mat <- matrix(-10000, nlons, nlats)
    mean_ta_summer_mat <- matrix(-10000, nlons, nlats)
    sd_ta_summer_mat <- matrix(-10000, nlons, nlats)
    mean_ta_winter_mat <- matrix(-10000, nlons, nlats)
    sd_ta_winter_mat <- matrix(-10000, nlons, nlats)
    energy_gain_per_year_mat <- matrix(-10000, nlons, nlats)
    growth_rate_per_year_mat <- matrix(-10000, nlons, nlats)
    annual_activity_hours_mat <- matrix(-10000, nlons, nlats)
    annual_activity_days_mat <- matrix(-10000, nlons, nlats)
    first_activity_day_mat <- matrix(-10000, nlons, nlats)
    last_activity_day_mat <- matrix(-10000, nlons, nlats)
    length_of_activity_season_mat <- matrix(-10000, nlons, nlats)
    mean_height_mat <- matrix(-10000, nlons, nlats)
    std_height_mat <- matrix(-10000, nlons, nlats)
    percentage_to_warm_mat <- matrix(-10000, nlons, nlats)
    percentage_to_cool_mat <- matrix(-10000, nlons, nlats)
    percentage_mixed_mat <- matrix(-10000, nlons, nlats)
    percentage_on_open_tree_mat <- matrix(-10000, nlons, nlats)
    percentage_on_shaded_tree_mat <- matrix(-10000, nlons, nlats)
    
    for (i in 1:nrow(rel_df)){
      row <- rel_df[i,]
      
      y <- row$netcdf_lats
      x <- row$netcdf_lons
      
      if (landmask[x,y] == 1){
        id_mat[x,y] <- row$id
        lat_mat[x,y] <- row$lat
        lon_mat[x,y] <- row$lon
        mean_ta_year_mat[x,y] <- row$mean_ta_year
        sd_ta_year_mat[x,y] <- row$sd_ta_year
        mean_ta_summer_mat[x,y] <- row$mean_ta_summer
        sd_ta_summer_mat[x,y] <- row$sd_ta_summer
        mean_ta_winter_mat[x,y] <- row$mean_ta_winter
        sd_ta_winter_mat[x,y] <- row$sd_ta_winter
        energy_gain_per_year_mat[x,y] <- row$energy_gain_per_year
        growth_rate_per_year_mat[x,y] <- row$growth_rate_per_year
        annual_activity_hours_mat[x,y] <- row$annual_activity_hours
        annual_activity_days_mat[x,y] <- row$annual_activity_days
        first_activity_day_mat[x,y] <- row$first_activity_day
        last_activity_day_mat[x,y] <- row$last_activity_day
        length_of_activity_season_mat[x,y] <- row$length_of_activity_season
        mean_height_mat[x,y] <- row$mean_height
        std_height_mat[x,y] <- row$std_height
        percentage_to_warm_mat[x,y] <- row$percentage_to_warm
        percentage_to_cool_mat[x,y] <- row$percentage_to_cool
        percentage_mixed_mat[x,y] <- row$percentage_mixed
        percentage_on_open_tree_mat[x,y] <- row$percentage_on_open_tree
        percentage_on_shaded_tree_mat[x,y] <- row$percentage_on_shaded_tree
        
      } else {
        print("on the ocean!")
      }
    }
    
    id_mat <- apply(t(id_mat), 2, rev)
    lat_mat <- apply(t(lat_mat), 2, rev)
    lon_mat <- apply(t(lon_mat), 2, rev)
    mean_ta_year_mat <- apply(t(mean_ta_year_mat), 2, rev)
    sd_ta_year_mat <- apply(t(sd_ta_year_mat), 2, rev)
    mean_ta_summer_mat <- apply(t(mean_ta_summer_mat), 2, rev)
    sd_ta_summer_mat <- apply(t(sd_ta_summer_mat), 2, rev)
    mean_ta_winter_mat <- apply(t(mean_ta_winter_mat), 2, rev)
    sd_ta_winter_mat <- apply(t(sd_ta_winter_mat), 2, rev)
    energy_gain_per_year_mat <- apply(t(energy_gain_per_year_mat), 2, rev)
    growth_rate_per_year_mat <- apply(t(growth_rate_per_year_mat), 2, rev)
    annual_activity_hours_mat <- apply(t(annual_activity_hours_mat), 2, rev)
    annual_activity_days_mat <- apply(t(annual_activity_days_mat), 2, rev)
    first_activity_day_mat <- apply(t(first_activity_day_mat), 2, rev)
    last_activity_day_mat <- apply(t(last_activity_day_mat), 2, rev)
    length_of_activity_season_mat <- apply(t(length_of_activity_season_mat), 2, rev)
    mean_height_mat <- apply(t(mean_height_mat), 2, rev)
    std_height_mat <- apply(t(std_height_mat), 2, rev)
    percentage_to_warm_mat <- apply(t(percentage_to_warm_mat), 2, rev)
    percentage_to_cool_mat <- apply(t(percentage_to_cool_mat), 2, rev)
    percentage_mixed_mat <- apply(t(percentage_mixed_mat), 2, rev)
    percentage_on_open_tree_mat <- apply(t(percentage_on_open_tree_mat), 2, rev)
    percentage_on_shaded_tree_mat <- apply(t(percentage_on_shaded_tree_mat), 2, rev)
    
    #raster(growth_rate_per_year_mat)
    
    #### to netCDF file ####
    
    # set dimensions
    sn_dim <- ncdim_def('south_north', '', 1:nlats, unlim=FALSE, create_dimvar=FALSE)
    we_dim <- ncdim_def('west_east', '', 1:nlons, unlim=FALSE, create_dimvar=FALSE)
    
    # set id var
    id <- ncvar_def('id', 'none', list(sn_dim, we_dim),
                     -10000, longname='coordinate ID', prec='integer')
    
    # set lat and lon vars
    lon <- ncvar_def('lon', 'degrees_east', list(sn_dim, we_dim),
                     -10000, longname='longitude_east', prec='float')
    lat <- ncvar_def('lat', 'degrees_north', list(sn_dim, we_dim),
                     -10000, longname='latitude_north', prec='float')
    
    
    # set different variables
    mean_ta_year <- ncvar_def('mean_ta_year', 'Kelvin', list(sn_dim, we_dim), -10000, longname='Mean annual air temperature in 50% shade', prec='float')
    sd_ta_year <- ncvar_def('sd_ta_year', 'Kelvin', list(sn_dim, we_dim), -10000, longname='standard deviation of annual air temperature in 50% shade', prec='float')
    mean_ta_summer <- ncvar_def('mean_ta_summer', 'Kelvin', list(sn_dim, we_dim), -10000, longname='Mean air temperature in 50% shade, in the summer (June-August)', prec='float')
    sd_ta_summer <- ncvar_def('sd_ta_summer', 'Kelvin', list(sn_dim, we_dim), -10000, longname='standard deviation of air temperature in 50% shade, in the summer (June-August)', prec='float')
    mean_ta_winter <- ncvar_def('mean_ta_winter', 'Kelvin', list(sn_dim, we_dim), -10000, longname='Mean air temperature in 50% shade, in the winter (December-February)', prec='float')
    sd_ta_winter <- ncvar_def('sd_ta_winter', 'Kelvin', list(sn_dim, we_dim), -10000, longname='standard deviation of air temperature in 50% shade, in the winter (December-February)', prec='float')
    
    energy_gain_per_year <- ncvar_def('energy_gain_per_year', 'Joule/year', list(sn_dim, we_dim), -10000, longname='mean annual energy gain', prec='float')
    growth_rate_per_year <- ncvar_def('growth_rate_per_year', 'lizard/year', list(sn_dim, we_dim), -10000, longname='mean annual growth rate', prec='float')
    annual_activity_hours <- ncvar_def('annual_activity_hours', 'hour/year', list(sn_dim, we_dim), -10000, longname='mean number of activity hours per year', prec='float')
    annual_activity_days <- ncvar_def('annual_activity_days', 'day/year', list(sn_dim, we_dim), -10000, longname='mean number of days with activity per year', prec='float')
    
    first_activity_day <- ncvar_def('first_activity_day', 'julian day', list(sn_dim, we_dim), -10000, longname='mean first julian day with activity', prec='float')
    last_activity_day <- ncvar_def('last_activity_day', 'julian day', list(sn_dim, we_dim), -10000, longname='mean last julian day with activity', prec='float')
    length_of_activity_season <- ncvar_def('length_of_activity_season', 'day', list(sn_dim, we_dim), -10000, longname='mean length of activity season', prec='float')
    
    mean_height <- ncvar_def('mean_height', 'centimeter', list(sn_dim, we_dim), -10000, longname='mean climbing height when climbing', prec='float')
    std_height <- ncvar_def('std_height', 'centimeter', list(sn_dim, we_dim), -10000, longname='standard deviation of climbing heights when climbing', prec='float')
    
    percentage_to_warm <- ncvar_def('percentage_to_warm', 'percentage', list(sn_dim, we_dim), -10000, longname='percentage of times the lizard climbed to warm', prec='float')
    percentage_to_cool <- ncvar_def('percentage_to_cool', 'percentage', list(sn_dim, we_dim), -10000, longname='percentage of times the lizard climbed to cool', prec='float')
    percentage_mixed <- ncvar_def('percentage_mixed', 'percentage', list(sn_dim, we_dim), -10000, longname='percentage of times the lizard climbed because other micro-environments were both too cool or too hot for activity (mixed)', prec='float')
    
    percentage_on_open_tree <- ncvar_def('percentage_on_open_tree', 'percentage', list(sn_dim, we_dim), -10000, longname='percentage of times the lizard climbed on open tree', prec='float')
    percentage_on_shaded_tree <- ncvar_def('percentage_on_shaded_tree', 'percentage', list(sn_dim, we_dim), -10000, longname='percentage of times the lizard climbed on shaded tree', prec='float')
    
    
    # creating the netCDF file
    
    nc <- nc_create( paste("../../Data/lizard_output_for_analysis/netcdf_files/", case,".nc", sep=""), list(id,lon,lat,mean_ta_year,sd_ta_year,mean_ta_summer,sd_ta_summer,mean_ta_winter,sd_ta_winter, energy_gain_per_year, growth_rate_per_year, annual_activity_hours, annual_activity_days, first_activity_day, last_activity_day, length_of_activity_season, mean_height, std_height, percentage_to_warm, percentage_to_cool, percentage_mixed, percentage_on_open_tree, percentage_on_shaded_tree))
    
    # ********** GLOBAL ATTRIBUTES **********
    attval <- format(Sys.time(), '%F %r %Z')
    status <- ncatt_put(nc, 0, 'CREATION_DATE', attval)
    
    # ********** WRITE VARIABLES **********
    ncvar_put(nc, id, id_mat)
    ncvar_put(nc, lat, lat_mat)
    ncvar_put(nc, lon, lon_mat)
    ncvar_put(nc, mean_ta_year, mean_ta_year_mat)
    ncvar_put(nc, sd_ta_year, sd_ta_year_mat)
    ncvar_put(nc, mean_ta_summer, mean_ta_summer_mat)
    ncvar_put(nc, sd_ta_summer, sd_ta_summer_mat)
    ncvar_put(nc, mean_ta_winter, mean_ta_winter_mat)
    ncvar_put(nc, sd_ta_winter, sd_ta_winter_mat)
    
    ncvar_put(nc, energy_gain_per_year, energy_gain_per_year_mat)
    ncvar_put(nc, growth_rate_per_year, growth_rate_per_year_mat)
    ncvar_put(nc, annual_activity_hours, annual_activity_hours_mat)
    ncvar_put(nc, annual_activity_days, annual_activity_days_mat)
    
    ncvar_put(nc, first_activity_day, first_activity_day_mat)
    ncvar_put(nc, last_activity_day, last_activity_day_mat)
    ncvar_put(nc, length_of_activity_season, length_of_activity_season_mat)
    
    ncvar_put(nc, mean_height, mean_height_mat)
    ncvar_put(nc, std_height, std_height_mat)
    
    ncvar_put(nc, percentage_to_warm, percentage_to_warm_mat)
    ncvar_put(nc, percentage_to_cool, percentage_to_cool_mat)
    ncvar_put(nc, percentage_mixed, percentage_mixed_mat)
    
    ncvar_put(nc, percentage_on_open_tree, percentage_on_open_tree_mat)
    ncvar_put(nc, percentage_on_shaded_tree, percentage_on_shaded_tree_mat)
    
    # ********** ADD EXTRA VARIABLE ATTRIBUTES **********
    status <- ncatt_put(nc, mean_ta_year, 'coordinates', 'lat lon')
    status <- ncatt_put(nc, sd_ta_year, 'coordinates', 'lat lon')
    status <- ncatt_put(nc, mean_ta_summer, 'coordinates', 'lat lon')
    status <- ncatt_put(nc, sd_ta_summer, 'coordinates', 'lat lon')
    status <- ncatt_put(nc, mean_ta_winter, 'coordinates', 'lat lon')
    status <- ncatt_put(nc, sd_ta_winter, 'coordinates', 'lat lon')
    
    status <- ncatt_put(nc, energy_gain_per_year, 'coordinates', 'lat lon')
    status <- ncatt_put(nc, growth_rate_per_year, 'coordinates', 'lat lon')
    status <- ncatt_put(nc, annual_activity_hours, 'coordinates', 'lat lon')
    status <- ncatt_put(nc, annual_activity_days, 'coordinates', 'lat lon')
    
    status <- ncatt_put(nc, first_activity_day, 'coordinates', 'lat lon')
    status <- ncatt_put(nc, last_activity_day, 'coordinates', 'lat lon')
    status <- ncatt_put(nc, length_of_activity_season, 'coordinates', 'lat lon')
    
    status <- ncatt_put(nc, mean_height, 'coordinates', 'lat lon')
    status <- ncatt_put(nc, std_height, 'coordinates', 'lat lon')
    
    status <- ncatt_put(nc, percentage_to_warm, 'coordinates', 'lat lon')
    status <- ncatt_put(nc, percentage_to_cool, 'coordinates', 'lat lon')
    status <- ncatt_put(nc, percentage_mixed, 'coordinates', 'lat lon')
    
    status <- ncatt_put(nc, percentage_on_open_tree, 'coordinates', 'lat lon')
    status <- ncatt_put(nc, percentage_on_shaded_tree, 'coordinates', 'lat lon')
    
    # ********** CLOSE **********
    status <- nc_close(nc)
    
  }
  
}










