library(ncdf4)
library(raster)
library(maptools)
library(plotrix)
library(gplots)
library(rasterVis)
library(maps)
library(RColorBrewer)
library(ggplot2)
library(dplyr)

dir.create("results", showWarnings = F)
dir.create("results//extended", showWarnings = F)
dir.create("results//extended//figure_E9", showWarnings = F)

figure_E9_facet_a <- function(){
  
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
  
  case <- "future_climbing"
  file_name <- paste("..\\..\\Data\\lizard_output_for_analysis\\netcdf_files\\", case, ".nc", sep = "")
  nfile <- nc_open((file_name))
  future_climbing_mat <- ncvar_get(nfile, varid = "growth_rate_per_year")
  status <- nc_close((nfile))
  
  
  # only climate change
  diff_climbing_cc_mat <- future_climbing_mat - past_climbing_mat
  
  # habitat loss and climate change
  diff_habitat_loss_cc_mat <- future_not_climbing_mat - past_climbing_mat
  
  minimal_tree_percentage_mat <- (diff_habitat_loss_cc_mat / (diff_habitat_loss_cc_mat - diff_climbing_cc_mat)) * 100
  minimal_tree_percentage_mat[diff_habitat_loss_cc_mat > 0] <- NA
  minimal_tree_percentage_mat[diff_climbing_cc_mat < 0] <- NA
  
  always_pos_mat <- diff_habitat_loss_cc_mat > 0
  always_pos_mat[always_pos_mat == FALSE] <- NA
  
  always_neg_mat <- diff_climbing_cc_mat < 0
  always_neg_mat[always_neg_mat == FALSE] <- NA
  
  min <- 0
  max <- 100
  by <- 20
  
  growth_rate_l <- raster(minimal_tree_percentage_mat)
  pos_l <- raster(always_pos_mat)
  neg_l <- raster(always_neg_mat)
  
  jet.colors <- #taken from http://senin-seblog.blogspot.com/2008/09/some-r-color-palettes.html
    colorRampPalette(c("yellow", "#FF7F00", "red", "#7F0000"))
  tiff(file=paste("results\\extended\\figure_E9\\facet_a.tiff", sep = ""), width=6000, height=2500, res=300, compression="lzw")
  
  colord=jet.colors(100)
  breaks <- seq(min,max,length.out = 100)
  plot(growth_rate_l, pch = 18, col = colord, asp = 0.5, ylim=c(0,1), xlim=c(0,1), xlab="", ylab="", xaxt="n", yaxt="n", breaks = breaks, legend = FALSE)
  plot(growth_rate_l, pch = 18, breaks = breaks, asp = 0.45, legend.width = 3, col = colord, axis.args=list(cex.axis=1.5, tcl = -0.2, mgp=c(0,0.5,0), lwd=0.5, at=seq(min,max,by)), axes=FALSE, box=FALSE)
  plot(pos_l, add = TRUE, pch = 18, breaks = breaks, asp = 0.45, legend.width = 3, col = "gray85", axis.args=list(cex.axis=1.5, tcl = -0.2, mgp=c(0,0.5,0), lwd=0.5, at=seq(min,max,by)), axes=FALSE, box=FALSE)
  plot(neg_l, add = TRUE, pch = 18, breaks = breaks, asp = 0.45, legend.width = 3, col = "gray50", axis.args=list(cex.axis=1.5, tcl = -0.2, mgp=c(0,0.5,0), lwd=0.5, at=seq(min,max,by)), axes=FALSE, box=FALSE)
  
  dev.off()
}



figure_E9_facet_b <- function(mat){
  rel_df <- as.data.frame(mat)
  rel_df$mean_ta_year <- rel_df$mean_ta_year - 273.15
  
  rel_df <- rel_df[order(rel_df$climbing, decreasing = TRUE), ]
  rel_df <- rel_df[order(rel_df$time, decreasing = TRUE), ]
  
  climbing_df <- rel_df %>%
    filter(climbing == "climbing") %>%
    group_by(id) %>%
    summarise(first_c_gr = first(growth_rate_per_year), last_c_gr = last(growth_rate_per_year), first_mty = first(mean_ta_year)) %>%
    mutate(diff_c_gr = last_c_gr - first_c_gr)
  
  
  big_rel_df <- merge(rel_df, climbing_df, by = c("id"))
  
  not_climbing_df <- rel_df %>%
    filter(climbing == "not climbing") %>%
    group_by(id) %>%
    summarise(first_nc_gr = first(growth_rate_per_year), last_nc_gr = last(growth_rate_per_year)) %>%
    mutate(diff_nc_gr = last_nc_gr - first_nc_gr)
  
  
  big_rel_df <- merge(big_rel_df, not_climbing_df, by = c("id"))
  
  big_rel_df <- big_rel_df %>%
    filter(time == "past") %>%
    filter(climbing == "climbing") %>%
    mutate(diff_habloss_gr = last_nc_gr - first_c_gr)
  
  red <- big_rel_df %>%
    filter((diff_habloss_gr < 0) & (diff_c_gr < 0))
  
  green <- big_rel_df %>%
    filter((diff_habloss_gr > 0) & (diff_c_gr > 0))
  
  yellow <- big_rel_df %>%
    filter((diff_habloss_gr < 0) & (diff_c_gr > 0))
  
  blue <- big_rel_df %>%
    filter((diff_habloss_gr > 0) & (diff_c_gr < 0))
  
  # print(paste("red:", as.character(nrow(red)), as.character(round(mean(red$first_mty),2))))
  # print(paste("green:", as.character(nrow(green)), as.character(round(mean(green$first_mty),2))))
  # print(paste("yellow:", as.character(nrow(yellow)), as.character(round(mean(yellow$first_mty),2))))
  # print(paste("blue:", as.character(nrow(blue)), as.character(round(mean(blue$first_mty),2))))
  
  rel_yellow <- yellow %>%
    select(id, lat, lon, time, climbing, first_mty, diff_c_gr, diff_nc_gr, diff_habloss_gr)
  
  rel_yellow <- rel_yellow %>%
    mutate(min_tree_percentage = (diff_habloss_gr / (diff_habloss_gr - diff_c_gr)) * 100) %>%
    mutate(max_tree_to_cut = 100 - min_tree_percentage)
  
  
  jet.colors <- #based on http://senin-seblog.blogspot.com/2008/09/some-r-color-palettes.html
    colorRampPalette(c("#00007F", "blue", "#007FFF", "cyan",
                       "gray", "yellow", "#FF7F00", "red", "#7F0000"))
  
  colord=jet.colors(100)
  
  tiff(file=paste("results\\extended\\figure_E9\\facet_b.tiff", sep = ""), width=5000, height=2500, res=300, compression="lzw")
  
  p <- ggplot(rel_yellow, aes(x = first_mty, y = min_tree_percentage, z = first_mty)) +
    theme_bw() +
    stat_summary_hex(bins = 100) +
    xlab("Mean annual air temperature [\u00B0C]") +
    ylab("Minimal tree availability (%)") +
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
    scale_fill_gradientn(colors = colord)
  
  print(p)
  
  dev.off()
  
}








