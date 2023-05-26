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
dir.create("..//results//figure_S10", showWarnings = F)


figure_S10 <- function(){
  file_name <- paste("..\\netcdf_files\\past_climbing.nc", sep = "")
  
  nfile <- nc_open((file_name))
  mean_ta_year_mat <- ncvar_get(nfile, varid = "mean_ta_year")
  mean_ta_year_mat <- mean_ta_year_mat - 273.15
  
  status <- nc_close((nfile))
  
  mean_ta_year_l <- raster(mean_ta_year_mat)

  jet.colors <- #taken from http://senin-seblog.blogspot.com/2008/09/some-r-color-palettes.html
    colorRampPalette(c("#00007F", "blue", "#007FFF", "cyan",
                       "#7FFF7F", "yellow", "#FF7F00", "red", "#7F0000"))
  
  tiff(file=paste("..\\results\\figure_S10\\figure_S10.tiff", sep = ""), width=6000, height=2500, res=300, compression="lzw")
  
  colord=jet.colors(100)
  breaks <- seq(-5,30,length.out = 100)
  plot(mean_ta_year_l, pch = 18, col = colord, asp = 0.5, ylim=c(0,1), xlim=c(0,1), xlab="", ylab="", xaxt="n", yaxt="n", breaks = breaks, legend = FALSE)
  plot(mean_ta_year_l, pch = 18, breaks = breaks, asp = 0.45, legend.width = 3, col = colord, axis.args=list(cex.axis=1.5, tcl = -0.2, mgp=c(0,0.5,0), lwd=0.5, at=seq(-10,35,10)), axes=FALSE, box=FALSE)
  
  
  dev.off()
  
}

