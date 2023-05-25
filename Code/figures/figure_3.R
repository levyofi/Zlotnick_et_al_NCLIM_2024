library(ncdf4)
library(raster)
library(maptools)
library(plotrix)
library(gplots)
library(rasterVis)
library(maps)
library(RColorBrewer)
library(ggplot2)

dir.create("..//results", showWarnings = F)
dir.create("..//results//figure_3", showWarnings = F)

figure_3 <- function(){
  
  # load data from netcdf files
  
  case <- "past_climbing"
  file_name <- paste("..\\netcdf_files\\", case, ".nc", sep = "")
  nfile <- nc_open((file_name))
  past_climbing_mat <- ncvar_get(nfile, varid = "annual_activity_hours")
  status <- nc_close((nfile))
  
  case <- "future_climbing"
  file_name <- paste("..\\netcdf_files\\", case, ".nc", sep = "")
  nfile <- nc_open((file_name))
  future_climbing_mat <- ncvar_get(nfile, varid = "annual_activity_hours")
  status <- nc_close((nfile))
  
  
  # climbing - effect of climate change
  
  climbing_change_in_time_mat <- future_climbing_mat - past_climbing_mat
  activity_hours_l <- raster(climbing_change_in_time_mat)
  
  
  min <- -1000
  max <- 1500
  by <- 500
  
  jet.colors <- #taken from http://senin-seblog.blogspot.com/2008/09/some-r-color-palettes.html
    colorRampPalette(c("#00007F", "#007FFF", "grey79",
                       "yellow", "red", "#7F0000"))
  
  tiff(file=paste("..\\results\\figure_3\\figure_3.tiff", sep = ""), width=6000, height=2500, res=300, compression="lzw")
  
  colord=jet.colors(100)
  breaks <- seq(min,max,length.out = 100)
  plot(activity_hours_l, pch = 18, col = colord, asp = 0.5, ylim=c(0,1), xlim=c(0,1), xlab="", ylab="", xaxt="n", yaxt="n", breaks = breaks, legend = FALSE)
  plot(activity_hours_l, pch = 18, breaks = breaks, asp = 0.45, legend.width = 3, col = colord, axis.args=list(cex.axis=1.5, tcl = -0.2, mgp=c(0,0.5,0), lwd=0.5, at=seq(min,max,by)), axes=FALSE, box=FALSE)
  
  dev.off()
}






