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
dir.create("results//extended//figure_E6", showWarnings = F)


figure_E6_facet_a <- function(){
  
  # load data from netcdf files
  case <- "past_climbing"
  file_name <- paste("..//..//Data//lizard_output_for_analysis//netcdf_files//", case, ".nc", sep = "")
  nfile <- nc_open((file_name))
  past_climbing_mat <- ncvar_get(nfile, varid = "growth_rate_per_year")
  status <- nc_close((nfile))
  
  min <- -5
  max <- 25
  by <- 5
  
  growth_rate_l <- raster(past_climbing_mat)
  
  color_palette <- colorRampPalette(c("#BFD9E9","#FBF8F7","#FBB59E","#EF6653","#C32320","#67000D"))
  colord <- color_palette(100)
  
  tiff(file=paste("results//extended//figure_E6//facet_a.tiff", sep = ""), width=6000, height=2500, res=300, compression="lzw")
  
  breaks <- seq(min,max,length.out = 100)
  plot(growth_rate_l, pch = 18, col = colord, asp = 0.5, ylim=c(0,1), xlim=c(0,1), xlab="", ylab="", xaxt="n", yaxt="n", breaks = breaks, legend = FALSE)
  plot(growth_rate_l, pch = 18, breaks = breaks, asp = 0.45, legend.width = 3, col = colord, axis.args=list(cex.axis=1.5, tcl = -0.2, mgp=c(0,0.5,0), lwd=0.5, at=seq(min,max,by)), axes=FALSE, box=FALSE)
  
  dev.off()
}


figure_E6_facet_b <- function(file_name, growth_rate_mat, min, max, by){
  
  # load data from netcdf files
  case <- "past_not_climbing"
  file_name <- paste("..//..//Data//lizard_output_for_analysis//netcdf_files//", case, ".nc", sep = "")
  nfile <- nc_open((file_name))
  past_not_climbing_mat <- ncvar_get(nfile, varid = "growth_rate_per_year")
  status <- nc_close((nfile))
  
  case <- "past_climbing"
  file_name <- paste("..//..//Data//lizard_output_for_analysis//netcdf_files//", case, ".nc", sep = "")
  nfile <- nc_open((file_name))
  past_climbing_mat <- ncvar_get(nfile, varid = "growth_rate_per_year")
  status <- nc_close((nfile))
  
  
  # habitat loss - change in past
  
  habitat_loss_past_mat <- past_not_climbing_mat - past_climbing_mat
  
  min <- -15
  max <- 0
  by <- 5
  
  growth_rate_l <- raster(habitat_loss_past_mat)
  
  color_palette <- colorRampPalette(c("#08306B","#3787C0","#ABCFE5","#FBF8F7"))
  colord <- color_palette(100)
  
  tiff(file=paste("results//extended//figure_E6//facet_b.tiff", sep = ""), width=6000, height=2500, res=300, compression="lzw")
  
  breaks <- seq(min,max,length.out = 100)
  plot(growth_rate_l, pch = 18, col = colord, asp = 0.5, ylim=c(0,1), xlim=c(0,1), xlab="", ylab="", xaxt="n", yaxt="n", breaks = breaks, legend = FALSE)
  plot(growth_rate_l, pch = 18, breaks = breaks, asp = 0.45, legend.width = 3, col = colord, axis.args=list(cex.axis=1.5, tcl = -0.2, mgp=c(0,0.5,0), lwd=0.5, at=seq(min,max,by)), axes=FALSE, box=FALSE)
  
  dev.off()
}


figure_E6_facet_c <- function(file_name, growth_rate_mat, min, max, by){
  
  # load data from netcdf files
  case <- "past_not_climbing"
  file_name <- paste("..//..//Data//lizard_output_for_analysis//netcdf_files//", case, ".nc", sep = "")
  nfile <- nc_open((file_name))
  past_not_climbing_mat <- ncvar_get(nfile, varid = "growth_rate_per_year")
  status <- nc_close((nfile))
  
  case <- "past_climbing"
  file_name <- paste("..//..//Data//lizard_output_for_analysis//netcdf_files//", case, ".nc", sep = "")
  nfile <- nc_open((file_name))
  past_climbing_mat <- ncvar_get(nfile, varid = "growth_rate_per_year")
  status <- nc_close((nfile))
  
  
  # past - change if climbing - percentage
  past_change_if_climbing_per_mat <- ((past_climbing_mat - past_not_climbing_mat) / past_climbing_mat) * 100
  min <- quantile(past_change_if_climbing_per_mat, 0.05, na.rm = TRUE)
  max <- quantile(past_change_if_climbing_per_mat, 0.95, na.rm = TRUE)
  
  past_change_if_climbing_per_mat[past_change_if_climbing_per_mat < 0] <- 0
  past_change_if_climbing_per_mat[past_change_if_climbing_per_mat > max] <- max
  
  past_change_if_climbing_per_mat <- -1 * past_change_if_climbing_per_mat
  
  min <- -75
  max <- 0
  by <- 15
  
  growth_rate_l <- raster(past_change_if_climbing_per_mat)
  #print(min(growth_rate_mat[growth_rate_mat != -10000], na.rm = TRUE))
  #print(max(growth_rate_mat[growth_rate_mat != -10000], na.rm = TRUE))
  
  color_palette <- colorRampPalette(c("#08306B","#3787C0","#ABCFE5","#FBF8F7"))
  colord <- color_palette(100)
  
  tiff(file=paste("results//extended//figure_E6//facet_c.tiff", sep = ""), width=6000, height=2500, res=300, compression="lzw")
  
  breaks <- seq(min,max,length.out = 100)
  plot(growth_rate_l, pch = 18, col = colord, asp = 0.5, ylim=c(0,1), xlim=c(0,1), xlab="", ylab="", xaxt="n", yaxt="n", breaks = breaks, legend = FALSE)
  plot(growth_rate_l, pch = 18, breaks = breaks, asp = 0.45, legend.width = 3, col = colord, axis.args=list(cex.axis=1.5, tcl = -0.2, mgp=c(0,0.5,0), lwd=0.5, at=seq(min,max,by)), axes=FALSE, box=FALSE)
  
  dev.off()
}


figure_E6_facet_d <- function(mat){
  
  rel_df <- as.data.frame(mat)
  rel_df$mean_ta_year <- rel_df$mean_ta_year - 273.15
  
  habitat_loss_df <- rel_df %>%
    group_by(id) %>%
    summarise(first_gr = first(growth_rate_per_year), last_gr = last(growth_rate_per_year), first_mty = first(mean_ta_year)) %>%
    mutate(diff_gr = first_gr - last_gr, rel_diff_gr = ((first_gr - last_gr) / abs(last_gr))*100)
  
  big_rel_df <- merge(rel_df, habitat_loss_df, by = c("id"))
  
  
  colord <- magma(100)
  
  tiff(file=paste("results//extended//figure_E6//facet_d.tiff", sep = ""), width=5000, height=2500, res=300, compression="lzw")
  
  p <- ggplot(big_rel_df, aes(x = first_mty, y = diff_gr, z = first_mty)) +
    theme_bw() +
    stat_summary_hex(bins = 100) +
    xlab("Mean annual air\ntemperature [\u00B0C]\n") +
    ylab("Absolute change in growth rate due to habitat loss [lizards/year]") +
    theme(axis.title.y = element_text(size = 22, face = "bold", vjust = 3),
          axis.title.x = element_text(size = 22, face = "bold", vjust = 0),
          legend.text = element_text(size = 18),
          legend.title = element_text(size = 18),
          legend.key.height = unit(2,"cm"),
          legend.title.align = 0.5,
          axis.text.x = element_text(size = 28),
          axis.text.y = element_text(size = 28),
          plot.margin = margin(1,1,1,1, "cm"),
          panel.grid = element_blank()) +
    labs(fill = "Mean annual air\ntemperature [\u00B0C]\n") +
    scale_fill_gradientn(colors = colord) +
    xlim(-10,30) +
    ylim(-10,0) 
  
  print(p)
  
  dev.off()
  
}

figure_E6_facet_e <- function(mat){
  
  rel_df <- as.data.frame(mat)
  rel_df$mean_ta_year <- rel_df$mean_ta_year - 273.15
  
  habitat_loss_df <- rel_df %>%
    group_by(id) %>%
    summarise(first_gr = first(growth_rate_per_year), last_gr = last(growth_rate_per_year), first_mty = first(mean_ta_year)) %>%
    mutate(diff_gr = first_gr - last_gr, rel_diff_gr = ((first_gr - last_gr) / abs(last_gr))*100)
  
  big_rel_df <- merge(rel_df, habitat_loss_df, by = c("id"))
  
  
  colord <- magma(100)
  
  tiff(file=paste("results//extended//figure_E6//facet_e.tiff", sep = ""), width=5000, height=2500, res=300, compression="lzw")
  
  p <- ggplot(big_rel_df, aes(x = first_mty, y = rel_diff_gr, z = first_mty)) +
    theme_bw() +
    stat_summary_hex(bins = 100) +
    xlab("Mean annual air\ntemperature [\u00B0C]\n") +
    ylab("Relative change in growth rate due to habitat loss [lizards/year]") +
    theme(axis.title.y = element_text(size = 22, face = "bold", vjust = 3),
          axis.title.x = element_text(size = 22, face = "bold", vjust = 0),
          legend.text = element_text(size = 18),
          legend.title = element_text(size = 18),
          legend.key.height = unit(2,"cm"),
          legend.title.align = 0.5,
          axis.text.x = element_text(size = 28),
          axis.text.y = element_text(size = 28),
          plot.margin = margin(1,1,1,1, "cm"),
          panel.grid = element_blank()) +
    labs(fill = "Mean annual air\ntemperature [\u00B0C]\n") +
    scale_fill_gradientn(colors = colord) +
    xlim(-10,30) +
    ylim(-100,0) 
  
  print(p)
  
  dev.off()
}
