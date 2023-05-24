setwd("Code/trunk_model")
source("air_density.R")
source("solar_partition.R")
source("convective_heat_trans.R")
source("create_ncdf_function.R")

library(ncdf4)
library(parallel)
library(foreach)
library(suncalc)
library(solrad)
library(bigleaf)
library(lubridate)


input_dir = "../../Data/input_data/"
setwd(input_dir)
input_files = read.table(file = "inputs.txt", comment.char = "#", header = F)#"2013_MIC_CLIM_36_past_33.832_-111.502.nc"
locations = read.table("locations.txt", header=F, sep=" ")

n.cores=parallel::detectCores()/2 - 2

library(doParallel)

library(humidity)

vapor_pressure = function(RH, SVP){#RH - relative humidity [0-100 %]; T - air temperature [Kelvin]
  SVP*RH/100*100 #return Pa
}

#setting the constants
# Trunk energy balance model with thermal inertia
slp = 0;       # slope, in degrees
asp = 90;      # aspect, in degrees Q:: of the trunk?
rad = 0.15;    # trunk radius including bark, in meters
barkthick = 0.007; # bark thickness in meters
tvf = 0.2;     # Trunk view factor
hmax = 0.05;   # Max. length size of the triangular mesh elements (e.g. 0.05 m)
rho = 900;     # trunk density, kg/m3
rho_bark = 600;# bark density,
# basic density of (DRY) spruce stem bark (342 kg·m-3, south-west Germany; 333 kg·m-3, Switzerland) Dietz(1975)
cp = 2800;     # trunk heat capacity, J/(kg*K)
cp_bark = 2000;# bark heat capacity, J/(kg*K)
k = 0.32;       # Coefficient of trunk heat conduction, W/m/K [Dupleix et al, 2013 Measuring the thermal 
# properties of green wood by the transient plane source (TPS) technique 
k_bark = 0.15;  #0.08; # Coefficient of bark heat conduction, W/m/K
# Kain et al (2013) Bark as Heat Insulation Material
H=0;           # Internal heat source (e.g., latent heat of freezing/melting)
trunk_alb = 0.09;     # Trunk albedo
emiss = 0.96;  # Trunk emissivity
D2R = pi/180;   # convert degrees to radians
R2D = 180/pi;   # convert radians to degrees
T_0 = 273.15;   # Conversion to Kelvin
SB=5.67e-8;  # Stefan-Boltzman constant (W/m^2/K^4)
kappa=0.4;      # Von Karman constant (-)
basal = 0.004; # trunk basal area, m2/m2
hgt = 13; # tree height in meters
EMG = 0.95 #ground emissivity

#create a table of saturated vapor pressures for different temperatures
temps = seq(200,360,0.1) # in Kelvin
svp = data.table(T=temps, SVP=SVP(temps))

#run through all locations on the inputs.txt file
results = foreach (
  input = input_files$V1[1]
  ) %do% { 
    
  ####   get the input data
  location_id = as.numeric(strsplit(input, "_")[[1]][1])
  vars = c("WIND10", "Tair", "Tsurface", "SWDOWN", "GLW", "TV", "TAH", "ALBEDO", "QAIR", "RHOAIR")
  microclimate = list()
  print(location_id)
  #read the netcdf input files
  for (var in vars){
    var_nc = nc_open(paste(var, input, sep="_"))
    microclimate[[var]] = ncvar_get(var_nc, varid = var)
    nc_close(var_nc)
  }
  #get the location lat,lon,and elevation
  lat = locations[location_id, 2]
  lon = locations[location_id, 3]
  elev = locations[location_id, 4]
  
  #get the times 
  time_nc = nc_open(paste(vars[1], input, sep="_"))
  dt = ncvar_get(time_nc, varid = "time")
  nc_close(time_nc)
  
  #### finished reading the input data
  
  #### prepare other variables for the model
  
  # air density
  aden = microclimate$RHOAIR
  
  # Day of Year
  date = as_datetime(as.character(dt), format="%Y%m%d%H" )
  DOY = yday(date)#  - datenum(Y,1,1) + 1; # Compute the day-of-year (Jan. 1st = 1)
  
  # relative humidity
  P = pressure.from.elevation(elev, microclimate$Tair - 273.15)*1000
  rh = SH2RH(microclimate$QAIR, t = microclimate$Tair[,1,1], p = P[,1,19])
  
  # sky emissivity
  vp = data.table(T=round(microclimate$Tair[,1,19]*10)/10)
  svpt=merge(vp, svp, by="T", all.x = T)
  SKYEMISS = 1.72*( (vapor_pressure(rh, svpt$SVP)/1000)/microclimate$Tair[,1,19])^(1/7)
  
  # output arrays
  sun_data = array(dim=c(length(microclimate$SWDOWN), 3)) #an array to save solar radiation predictions
  Ttrunk = array(dim=dim(microclimate$Tair[,1:2,])) #an array to save trunk temperature predictions. Set trunk array with 2 shade values (0% and 100%), and 19 heights

  #for initial conditions, set the first time step as air temperature
  Ttrunk[1,,] = microclimate$Tair[1,c(1,5),]

  #### finished prepare other variables for the model
  
  #### start calculating trunk temperatures for each time step 
  for (itime in 2:10000){#length(date)){ #time step loop
    
    #calculate the solar radiation features
    if (microclimate$SWDOWN[itime]>0){ #daytime
      solar.partition =solar_partition(elev, lat,lon,date[itime],microclimate$SWDOWN[itime],P[itime],microclimate$Tair[itime],rh[[itime]], microclimate$ALBEDO[itime]) ;
      sun_data[itime, ] = c(solar.partition$Isun_trunk, solar.partition$Ishade_trunk, solar.partition$diffuse_ratio)
    } else { #night
      solar.partition =solar_partition(elev, lat,lon,date[itime],microclimate$SWDOWN[itime],P[itime],microclimate$Tair[itime],rh[[itime]], microclimate$ALBEDO[itime]) ;
      solar.partition[]=0
      sun_data[itime, ] = 0
    }
    
    # calculate trunk temperatures
    alb = microclimate$ALBEDO[itime] #ground albedo
    TV = microclimate$TV[itime] #canopy leaf temperature
    for (iheight in 1:length(microclimate$Tair[1,1,])){ #height loop
      for (ishade in c(1,5)){ #shade loop 1-no shade, 5-full shade
        ishade_trunk = ifelse(ishade==1, 1, 2) #index to be used to save results
        cur_ttrunk = Ttrunk[itime-1, ishade_trunk, iheight] #get current trunk temperature
        
        #calculate sky longwave radiation
        L_g = microclimate$GLW[itime] #longwave radiation towards the ground
        FVEG = 0.5 #assume 50% of the radiation can penetrate the tree canopy
        L_c = (1-FVEG)*emiss*L_g + FVEG*emiss*emiss*SB*TV**4. # total longwave radiation
        skylw = L_c 
        
        #calculate ground longwave radiation towards the trunk
        EMG = 0.95
        CIR = emiss*EMG*SB # see eq. 53 in Gouttevin et al. 2015 
        groundlw = 0.5*CIR * microclimate$Tsurface[itime, ishade]**4 #0.5 is for assuming only 0.5 of the radiation heats the trunk
        
        #calculate incoming longwave radiation
        lw_in = 0.5*skylw + groundlw 
        
        #calculate outgoing logwave radiation, not used in the matlab code and in equations below 
        trunklw = emiss*SB*cur_ttrunk**4 #  
        
        # Compute the net (solar + longwave) radiation at the trunk surface, W/m^2
        if (ishade==5) { #shaded trunk
          dir_net = solar.partition$Ishade_trunk*(1-trunk_alb) + lw_in #- trunklw
          #print(paste(ishade, solar.partition$Ishade_trunk))
          } else { #sunlit trunk
          dir_net = solar.partition$Isun_trunk*(1-trunk_alb) + lw_in #- trunklw
          #print(paste(ishade, solar.partition$Isun_trunk))
        }
  
        #iterate over 5 time steps (720 seconds each) for the hour. the matlab code had one iteration but here I divided it to five
        # For the first time step, trunk temperatures are assumed equal to air
        t0 = cur_ttrunk;
        TAIR = microclimate$Tair[itime,ishade,iheight] # air temperature
        for (iter in 1:5){
          # Convective heat transfer coefficient, W/(m^2-K)
          hc = convective_heat_trans(TAIR,cur_ttrunk,aden[itime],microclimate$WIND10[itime, iheight],rad);    
          
          g = dir_net
          r0p = g;    
          r1p = -SB*emiss;
          r0 = r0p - 3.*r1p*cur_ttrunk^4;
          r1 = 4*r1p*cur_ttrunk^3;
          
          scalingfactor = 1;
          tr_top_rad = 0.26 - (0.26/13)*0.2*13; # tapered trunk radius at canopy base height
          V = (1/3)*pi*0.2*13*((0.26^2) + tr_top_rad^2 + 0.26*(tr_top_rad));
          hm = V*basal*rho*cp;
          hm0 = -scalingfactor*(hm/720)*cur_ttrunk #720 seconds is the time step
          hm1 = scalingfactor*hm/720
          
          ch_can = hc 
          h1 = ch_can
          h0 = -ch_can*TAIR
          
          temp_change = (h0 - r0 + hm0) / (r1 - h1 - hm1) - cur_ttrunk
          tbole = temp_change + cur_ttrunk
          cur_ttrunk = tbole
        }
        Ttrunk[itime, ishade_trunk, iheight] = cur_ttrunk #save the results
      }
    }
  }
  #### finish calculating trunk temperatures for each time step 
  
  #save the results for this input file as netcdf file
  save_ncdf(location_id, Ttrunk, sun_data, file = paste0("../../../Ttrunk_", input),lat,lon,elev)
}

parallel::stopCluster(cl = my.cluster)

