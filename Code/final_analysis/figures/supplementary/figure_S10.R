library(ncdf4)
library(raster)
library(maptools)
library(plotrix)
library(gplots)
library(rasterVis)
library(maps)
library(RColorBrewer)
library(ggplot2)

dir.create("results", showWarnings = F)
dir.create("results//supplementary", showWarnings = F)
dir.create("results//supplementary//figure_S10", showWarnings = F)

clip<-function(raster,shape) {
  a1_crop<-crop(raster,shape)
  step1<-rasterize(shape,a1_crop, silent=TRUE)
  step1[!is.na(step1)]=1
  a1_crop*step1}

set_coordinates<-function(rs){
  xmin(rs) <- min(lon_ncdf)
  xmax(rs) <- max(lon_ncdf)
  ymin(rs) <- min(lat_ncdf)
  ymax(rs) <- max(lat_ncdf)
  rs
}

figure_S10 <- function(){
  nc = nc_open("..\\..\\Data\\lizard_output_for_analysis\\us_output.nc")
  lat_ncdf = ncvar_get(nc, varid="lat", start=c(1,1), count=c(1,-1))
  lon_ncdf = ncvar_get(nc, varid="lon", start=c(1,1), count=c(-1,1))
  
  #set the projection and extent of the maps
  lat <- raster("..\\..\\Data\\lizard_output_for_analysis\\us_output.nc", varname="lat")
  lon <- raster("..\\..\\Data\\lizard_output_for_analysis\\us_output.nc", varname="lon")
  plat <- rasterToPoints(lat)
  plon <- rasterToPoints(lon)
  lonlat <- cbind(plon[,3], plat[,3])
  lonlat <- SpatialPoints(lonlat, proj4string = CRS("+proj=longlat +datum=WGS84"))
  
  # Need the rgdal package to project it to the original coordinate system
  p = CRS("+proj=lcc +lat_1=25.0 +lat_2=45.0 +lat_0=38.0 +lon_0=-100.0 +datum=WGS84 +R=6370000 +units=m +no_defs")
  shp = readShapeSpatial("..\\..\\Data\\lizard_output_for_analysis\\scel_undu_pl.shp", proj4string =  CRS("+proj=longlat +datum=WGS84"))
  shp<- spTransform(shp, p)
  
  mycrs <- p
  plonlat <- spTransform(lonlat, CRSobj = mycrs)
  
  
  tiff(file=paste("results//supplementary//figure_S10//figure_S10.tiff", sep = ""), width=6000, height=2500, res=300, compression="lzw")
  
  rs_current_ta<-raster("..\\..\\Data\\lizard_output_for_analysis\\us_output.nc", varname = "mean_air50")
  rs = rs_current_ta-273
  max_r= cellStats(rs , stat='max')
  min_r= cellStats(rs , stat='min')
  byz = 1
  range = seq(min_r, max_r+1, by = byz)
  colord <- magma(length(range))
  projection(rs) <- p
  extent(rs) <- extent(plonlat)
  plot(rs, col=colord, xlab="", ylab="", xaxt="n", yaxt="n", bty="n", box=F, breaks = range , legend = F)
  plot(rs, col=colord, xlab="", ylab="", xaxt="n", yaxt="n", bty="n", box=F, breaks = range , legend.only = T, axis.args=list(at=seq(-5, 30, 5)), smallplot=c(0.83,0.9,0.25,0.75))
  plot(shp, add=T, lwd=3)
  
  dev.off()
  
}



