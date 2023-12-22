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
dir.create("results//supplementary//figure_S8", showWarnings = F)


figure_S8_facet_a <- function(){
  
  # load data from netcdf files
  
  case <- "past_climbing"
  file_name <- paste("..//..//Data//lizard_output_for_analysis//netcdf_files//", case, ".nc", sep = "")
  nfile <- nc_open((file_name))
  past_mat_cool <- ncvar_get(nfile, varid = "percentage_to_cool")
  status <- nc_close((nfile))
  
  case <- "future_climbing"
  file_name <- paste("..//..//Data//lizard_output_for_analysis//netcdf_files//", case, ".nc", sep = "")
  nfile <- nc_open((file_name))
  future_mat_cool <- ncvar_get(nfile, varid = "percentage_to_cool")
  status <- nc_close((nfile))
  
  
  # to cool - effect of climate change
  
  change_mat <- future_mat_cool - past_mat_cool
  
  min <- -25
  max <- 75
  by <- 25
  
  change_mat[change_mat == -1] <- NA
  
  percentage_l <- raster(change_mat)
  
  jet.colors <- #taken from http://senin-seblog.blogspot.com/2008/09/some-r-color-palettes.html
    colorRampPalette(c("#007FFF",
                       "grey79", "yellow", "red", "#7F0000"))
  
  tiff(file=paste("results//supplementary//figure_S8//facet_a.tiff", sep = ""), width=6000, height=2500, res=300, compression="lzw")
  
  colord=jet.colors(100)
  breaks <- seq(min,max,length.out = 100)
  plot(percentage_l, pch = 18, col = colord, asp = 0.5, ylim=c(0,1), xlim=c(0,1), xlab="", ylab="", xaxt="n", yaxt="n", breaks = breaks, legend = FALSE)
  plot(percentage_l, pch = 18, breaks = breaks, asp = 0.45, legend.width = 3, col = colord, axis.args=list(cex.axis=1.5, tcl = -0.2, mgp=c(0,0.5,0), lwd=0.5, at=seq(min,max,by)), axes=FALSE, box=FALSE)
  
  dev.off()
}


figure_S8_facet_b <- function(){
  
  # load data from netcdf files
  
  case <- "past_climbing"
  file_name <- paste("..//..//Data//lizard_output_for_analysis//netcdf_files//", case, ".nc", sep = "")
  nfile <- nc_open((file_name))
  past_mat_shaded <- ncvar_get(nfile, varid = "percentage_on_shaded_tree")
  status <- nc_close((nfile))
  
  case <- "future_climbing"
  file_name <- paste("..//..//Data//lizard_output_for_analysis//netcdf_files//", case, ".nc", sep = "")
  nfile <- nc_open((file_name))
  future_mat_shaded <- ncvar_get(nfile, varid = "percentage_on_shaded_tree")
  status <- nc_close((nfile))
  
  
  # to cool - effect of climate change
  
  change_mat <- future_mat_shaded - past_mat_shaded
  
  min <- -25
  max <- 75
  by <- 25
  
  change_mat[change_mat == -1] <- NA
  
  percentage_l <- raster(change_mat)
  
  jet.colors <- #taken from http://senin-seblog.blogspot.com/2008/09/some-r-color-palettes.html
    colorRampPalette(c("#007FFF",
                                "grey79", "yellow", "red", "#7F0000"))
                                
  tiff(file=paste("results//supplementary//figure_S8//facet_b.tiff", sep = ""), width=6000, height=2500, res=300, compression="lzw")
  
  colord=jet.colors(100)
  breaks <- seq(min,max,length.out = 100)
  plot(percentage_l, pch = 18, col = colord, asp = 0.5, ylim=c(0,1), xlim=c(0,1), xlab="", ylab="", xaxt="n", yaxt="n", breaks = breaks, legend = FALSE)
  plot(percentage_l, pch = 18, breaks = breaks, asp = 0.45, legend.width = 3, col = colord, axis.args=list(cex.axis=1.5, tcl = -0.2, mgp=c(0,0.5,0), lwd=0.5, at=seq(min,max,by)), axes=FALSE, box=FALSE)
  
  dev.off()
}



figure_S8_facet_c <- function(){
  
  # load data from netcdf files
  
  case <- "past_climbing"
  file_name <- paste("..//..//Data//lizard_output_for_analysis//netcdf_files//", case, ".nc", sep = "")
  nfile <- nc_open((file_name))
  past_mat <- ncvar_get(nfile, varid = "mean_height")
  status <- nc_close((nfile))
  
  case <- "future_climbing"
  file_name <- paste("..//..//Data//lizard_output_for_analysis//netcdf_files//", case, ".nc", sep = "")
  nfile <- nc_open((file_name))
  future_mat <- ncvar_get(nfile, varid = "mean_height")
  status <- nc_close((nfile))
  
  
  # change to the future
  change_mat <- future_mat - past_mat
  
  min <- -50
  max <- 125
  by <- 25
  
  mean_height_l <- raster(change_mat)
  
  jet.colors <- #taken from http://senin-seblog.blogspot.com/2008/09/some-r-color-palettes.html
    colorRampPalette(c("#00007F", "blue", "grey79",
                                "yellow", "Orange", "#FF7F00", "red", "#7F0000"))
                                
  tiff(file=paste("results//supplementary//figure_S8//facet_c.tiff", sep = ""), width=6000, height=2500, res=300, compression="lzw")
  
  colord=jet.colors(100)
  breaks <- seq(min,max,length.out = 100)
  plot(mean_height_l, pch = 18, col = colord, asp = 0.5, ylim=c(0,1), xlim=c(0,1), xlab="", ylab="", xaxt="n", yaxt="n", breaks = breaks, legend = FALSE)
  plot(mean_height_l, pch = 18, breaks = breaks, asp = 0.45, legend.width = 3, col = colord, axis.args=list(cex.axis=1.5, tcl = -0.2, mgp=c(0,0.5,0), lwd=0.5, at=seq(min,max,by)), axes=FALSE, box=FALSE)
  
  dev.off()
}

