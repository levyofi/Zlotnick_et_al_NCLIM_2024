n.cores=parallel::detectCores()/2 - 2
library(ncdf4)
# setwd("/home/ofir/Dropbox/eclipse workspace/trunk_temperature")
# 
# input_dir = "input_files"
# input_files = read.table(file = "inputs.txt", comment.char = "#", header = F, stringsAsFactors = F)#"2013_MIC_CLIM_36_past_33.832_-111.502.nc"
# setwd(input_dir)
# input_files_RData = read.table(file = "input_RData.txt", comment.char = "#", header = F, stringsAsFactors = F)#"2013_MIC_CLIM_36_past_33.832_-111.502.nc"

save_ncdf = function(location_id, Ttrunk_data, sun_data, file_name, lat, lon, elev ){
  vars = c("WIND10") #just to get the time values
  var_nc = nc_open(paste(vars[1], input_files$V1[1], sep="_"))
  dt = ncvar_get(var_nc, varid = "time")
  layers_m = ncvar_get(var_nc, varid = "layers_mic")
  nc_close(var_nc)
  Ttrunk_data = Ttrunk
  #get lat, lon, elevation
  locations = read.table("locations.txt", header=F, sep=" ")
  
  curlat = locations[location_id, 2]
  curlon = locations[location_id, 3]
  elev = locations[location_id, 4]

  nlats = 1
  nlons = 1
  ntimes = length(dt)
  sn_dim <- ncdim_def('south_north', '', 1:nlats, unlim=FALSE, create_dimvar=FALSE)
  we_dim <- ncdim_def('west_east', '', 1:nlons, unlim=FALSE, create_dimvar=FALSE)
  time_dim <- ncdim_def('time', '', 1:ntimes, unlim=FALSE, create_dimvar=FALSE)
  shade_dim <- ncdim_def('shade', '', 1:2, unlim=FALSE, create_dimvar=FALSE)
  layers_wrf_dim <- ncdim_def('soil_wrf', '', 1:4, unlim=FALSE, create_dimvar=FALSE)
  layers_mic_dim <- ncdim_def('soil_mic', '', 1:19, unlim=FALSE, create_dimvar=FALSE)
  #air_mic_dim <- ncdim_def('air_mic', '', 1:19, unlim=FALSE, create_dimvar=FALSE)

  #add variables definitions TODO
  lon <- ncvar_def('lon', 'degrees_east', list(we_dim),-999, longname='longitude east', prec='float')
  lat <- ncvar_def('lat', 'degrees_north', list(sn_dim),-999, longname='latitude north', prec='float')
  time <- ncvar_def('time', 'time', list(time_dim),-999, longname='date and time (YYYYMMDDHH)', prec='integer')
  shade = ncvar_def('shade', 'percent', list(shade_dim), -999, longname='shade levels', prec='float')
  layers_wrf = ncvar_def('layers_wrf', 'meter', list(layers_wrf_dim), -999, longname='soil layers from WRF output', prec='float')
  layers_mic= ncvar_def('layers_mic', 'meter', list(layers_mic_dim), -999, longname='air and soil layers', prec='float')
  #hours = ncvar_def('hour', 'hour', list(time_dim), -999, longname='hour of day (0-23)', prec='integer')
  #days= ncvar_def('day', 'day', list(time_dim), -999, longname='day of month', prec='integer')
  #months = ncvar_def('month', 'month', list(time_dim), -999, longname='month of year', prec='integer')
  #years = ncvar_def('year', 'year', list(time_dim), -999, longname='year', prec='integer')
  Ttrunk <- ncvar_def('Ttrunk', 'K', list(time_dim, shade_dim, layers_mic_dim), -999, longname='trunk temperature', prec='float')
  solarb <- ncvar_def('solar_trunk_beam', 'W/m2', list(time_dim), -999, longname='direct solar radiation that hits the trunk', prec='float')
  solard <- ncvar_def('solar_trunk_diffuse', 'W/m2', list(time_dim), -999, longname='diffuse solar radiation that hits the trunk', prec='float')
  diffuse <- ncvar_def('diffuse_ratio', 'dec %', list(time_dim), -999, longname='percentage of diffuse radiation', prec='float')
  
  climate.nc = file_name
  nc <- nc_create(climate.nc, list(lon,lat,time,shade,layers_wrf, layers_mic,Ttrunk, solarb, solard, diffuse))
  # ********** GLOBAL ATTRIBUTES **********
  attval <- format(Sys.time(), '%F %r %Z')
  status <- ncatt_put(nc, 0, 'CREATION_DATE', attval)
  # ********** WRITE VARIABLES **********
  ncvar_put(nc, lat,  curlat)
  ncvar_put(nc, lon,  curlon)
  ncvar_put(nc, time, dt)
  ncvar_put(nc, shade, c(0., 100.))
  ncvar_put(nc, layers_wrf, c(0.05,0.1,0.4,1.))
  ncvar_put(nc, layers_mic, layers_m)
  ncvar_put(nc, Ttrunk, Ttrunk_data)
  ncvar_put(nc, solarb, sun_data[,1])
  ncvar_put(nc, solard, sun_data[,2])
  ncvar_put(nc, diffuse, sun_data[,3])
  
  # ********** CLOSE **********
  status <- nc_close(nc)
}