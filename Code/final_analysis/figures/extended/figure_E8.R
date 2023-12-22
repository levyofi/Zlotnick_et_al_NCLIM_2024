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
dir.create("results//extended", showWarnings = F)
dir.create("results//extended//figure_E8", showWarnings = F)

figure_E8_facet_a <- function(){
  
  # load data from netcdf files
  
  case <- "past_climbing"
  file_name <- paste("..\\..\\Data\\lizard_output_for_analysis\\netcdf_files\\", case, ".nc", sep = "")
  nfile <- nc_open((file_name))
  past_climbing_mat <- ncvar_get(nfile, varid = "growth_rate_per_year")
  status <- nc_close((nfile))
  
  case <- "future_climbing"
  file_name <- paste("..\\..\\Data\\lizard_output_for_analysis\\netcdf_files\\", case, ".nc", sep = "")
  nfile <- nc_open((file_name))
  future_climbing_mat <- ncvar_get(nfile, varid = "growth_rate_per_year")
  status <- nc_close((nfile))
  
  
  # climbing - effect of climate change
  climbing_change_in_time_mat <- future_climbing_mat - past_climbing_mat

  min <- -20
  max <- 10
  by <- 5
  
  growth_rate_l <- raster(climbing_change_in_time_mat)
  
  jet.colors <- #taken from http://senin-seblog.blogspot.com/2008/09/some-r-color-palettes.html
    colorRampPalette(c("#00007F","blue", "#007FFF", "cyan2", "grey79", "yellow", "red"))
  
  tiff(file=paste("results\\extended\\figure_E8\\facet_a.tiff", sep = ""), width=6000, height=2500, res=300, compression="lzw")
  
  colord=jet.colors(100)
  breaks <- seq(min,max,length.out = 100)
  plot(growth_rate_l, pch = 18, col = colord, asp = 0.5, ylim=c(0,1), xlim=c(0,1), xlab="", ylab="", xaxt="n", yaxt="n", breaks = breaks, legend = FALSE)
  plot(growth_rate_l, pch = 18, breaks = breaks, asp = 0.45, legend.width = 3, col = colord, axis.args=list(cex.axis=1.5, tcl = -0.2, mgp=c(0,0.5,0), lwd=0.5, at=seq(min,max,by)), axes=FALSE, box=FALSE)
  
  dev.off()
}

figure_E8_facet_b <- function(){
  
  # load data from netcdf files

  case <- "past_climbing"
  file_name <- paste("..\\..\\Data\\lizard_output_for_analysis\\netcdf_files\\", case, ".nc", sep = "")
  nfile <- nc_open((file_name))
  past_climbing_mat <- ncvar_get(nfile, varid = "growth_rate_per_year")
  status <- nc_close((nfile))
  
  case <- "future_not_climbing"
  file_name <- paste("..\\..\\Data\\lizard_output_for_analysis\\netcdf_files\\", case, ".nc", sep = "")
  nfile <- nc_open((file_name))
  future_not_climbing_mat <- ncvar_get(nfile, varid = "growth_rate_per_year")
  status <- nc_close((nfile))
  
  
  # habitat loss and climate change
  habitat_loss_cc_mat <- future_not_climbing_mat - past_climbing_mat

  min <- -20
  max <- 10
  by <- 5
  
  growth_rate_l <- raster(habitat_loss_cc_mat)
  
  jet.colors <- #taken from http://senin-seblog.blogspot.com/2008/09/some-r-color-palettes.html
    colorRampPalette(c("#00007F","blue", "#007FFF", "cyan2", "grey79", "yellow", "red"))
  
  tiff(file=paste("results\\extended\\figure_E8\\facet_b.tiff", sep = ""), width=6000, height=2500, res=300, compression="lzw")
  
  colord=jet.colors(100)
  breaks <- seq(min,max,length.out = 100)
  plot(growth_rate_l, pch = 18, col = colord, asp = 0.5, ylim=c(0,1), xlim=c(0,1), xlab="", ylab="", xaxt="n", yaxt="n", breaks = breaks, legend = FALSE)
  plot(growth_rate_l, pch = 18, breaks = breaks, asp = 0.45, legend.width = 3, col = colord, axis.args=list(cex.axis=1.5, tcl = -0.2, mgp=c(0,0.5,0), lwd=0.5, at=seq(min,max,by)), axes=FALSE, box=FALSE)
  
  dev.off()
}



