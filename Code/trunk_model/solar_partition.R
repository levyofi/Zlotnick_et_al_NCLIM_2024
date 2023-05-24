library(insol)
solar_partition = function(elev, lat,long,dt,SWDOWN,P,Ta,RH, ALBEDO=0.4){
  
  # if (SWDOWN>0){ #day
  #   browser()
  # }
  
  #calculate absolute julian day in seconds  - needed for the insolation function
  jd = JD(dt) #number of seconds since the beginning of 1970 (in the UTC timezone) 
  
  #calculate solar zenith and azimuth angles
  sunv = sunvector(jd,lat,long, timezone = 0) #we took timezone into account already 
  zenith = sunpos(sunv)[,2]
  azimuth = sunpos(sunv)[,1]
  
  #calculate clean sky radiation and diffuse_ratio
  Idirdif = insol::insolation(zenith,jd,elev,90,RH,Ta,0.003,ALBEDO) # 90 is the view distance 
  diffuse_ratio = Idirdif[,2]/(Idirdif[,1]+Idirdif[,2])
  
  #diffuse radiation
  Idiff = Idirdif[,2] 
  
  #calculate downward beam 
  Ibeam_surface = max(0,(SWDOWN - Idiff)) 
  #print(paste("SWDOWN Ibeam:", Ibeam_surface))
  
  #calculate downward beam of clean sky using Idirdif[,1]
  cleansky_Ibean_surface = Idirdif[,1]*cos(radians(zenith))
  #print(paste("Clean sky beam:", cleansky_Ibean_surface))
  
  #calculate the percentage of clean sky based on the ratio between cleansky and SWDOWN values
  if (cleansky_Ibean_surface>0){ #day 
    frac_clean_sky = Ibeam_surface/cleansky_Ibean_surface
    if (frac_clean_sky>1){
      #print("cloud cover lower than 0")
      frac_clean_sky=1
    }
  } else { #night
    frac_clean_sky=0
  }
  
  #based on cloud cover, calculate real total beam, accounting for cloud cover
  Itotal=frac_clean_sky*Idirdif[,1]
  #print(paste("Total beam after clouds:", Itotal))
  
  #calculate beam towards the trunk
  Ibeam_trunk = sin(radians(zenith))*Itotal
  
  #calculate total solar radiation towards the trunk
  #sunlight
  Isun_trunk = Ibeam_trunk + ALBEDO*Ibeam_surface*sin(radians(zenith)) + Idiff #direct to trunk + reflected to trunk + diffuse 
  #print(paste(Idirdif[,1], Itotal, SWDOWN, Ibeam_trunk, Isun_trunk, cloud_cover))

  if (Isun_trunk<0){
    browser()
  }
  #shade
  Ishade_trunk = Idiff
  
  return(list("Isun_trunk" = Isun_trunk, "Ishade_trunk" = Ishade_trunk, "diffuse_ratio" = diffuse_ratio, "direct" = Idirdif[,1], "diffuse" = Idirdif[,2], "diffuse_ratio" = diffuse_ratio))
}
  
