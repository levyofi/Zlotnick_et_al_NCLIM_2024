library(dplyr)
library(ggplot2)
library(rasterVis)
library(tidyverse)
library(ncdf4)
library(reshape2)

path <- "..//input//deep_data//day_sum_np.csv"
dir.create("..//results", showWarnings = F)
dir.create("..//results//figure_2", showWarnings = F)


figure_2_facet_a <- function(mat){
  
  rel_df <- as.data.frame(mat)
  rel_df$mean_ta_year <- rel_df$mean_ta_year - 273.15
  
  time_df <- rel_df %>%
    group_by(id) %>%
    summarise(first_ah = first(annual_activity_hours), last_ah = last(annual_activity_hours), first_gr = first(growth_rate_per_year), last_gr = last(growth_rate_per_year), first_mty = first(mean_ta_year)) %>%
    mutate(diff_abs_ah = last_ah - first_ah, diff_rel_ah = ((last_ah - first_ah)/last_ah)*100)
  
  
  big_rel_df <- merge(rel_df, time_df, by = c("id"))
  
  jet.colors <- #taken from http://senin-seblog.blogspot.com/2008/09/some-r-color-palettes.html
    colorRampPalette(c("#00007F", "blue", "#007FFF", "cyan",
                                "#7FFF7F", "yellow", "#FF7F00", "red", "#7F0000"))
                                
  colord=jet.colors(100)
  
  tiff(file=paste("..\\results\\figure_2\\facet_a.tiff", sep = ""), width=5000, height=2500, res=300, compression="lzw")
  
  p <- ggplot(big_rel_df, aes(x = last_ah, y = diff_abs_ah, z = first_mty)) +
    theme_bw() +
    stat_summary_hex(bins = 100) +
    xlab("mean activity hours without habitat loss [hours]") +
    ylab("absolute decline in mean activity hours due to habitat loss [hours]") +
    theme(axis.title.y = element_text(size = 22, face = "bold", vjust = 3),
          axis.title.x = element_text(size = 22, face = "bold", vjust = 0),
          legend.text = element_text(size = 18),
          legend.title = element_text(size = 18),
          legend.key.height = unit(2,"cm"),
          legend.title.align = 0.5,
          axis.text.x = element_text(size = 24),
          axis.text.y = element_text(size = 24),
          plot.margin = margin(1,1,1,1, "cm"),
          panel.grid = element_blank()) +
    labs(fill = "Mean annual air\ntemperature [\u00B0C]\n") +
    scale_fill_gradientn(colors = colord) +
    xlim(0,4000) +
    ylim(0,1700)
  
  print(p)
  
  dev.off()
}

figure_2_facet_b <- function(mat){
  
  rel_df <- as.data.frame(mat)
  rel_df$mean_ta_year <- rel_df$mean_ta_year - 273.15
  
  time_df <- rel_df %>%
    group_by(id) %>%
    summarise(first_ah = first(annual_activity_hours), last_ah = last(annual_activity_hours), first_gr = first(growth_rate_per_year), last_gr = last(growth_rate_per_year), first_mty = first(mean_ta_year)) %>%
    mutate(diff_abs_ah = last_ah - first_ah, diff_rel_ah = ((last_ah - first_ah)/last_ah)*100)
  
  
  big_rel_df <- merge(rel_df, time_df, by = c("id"))
  
  jet.colors <- #taken from http://senin-seblog.blogspot.com/2008/09/some-r-color-palettes.html
    colorRampPalette(c("#00007F", "blue", "#007FFF", "cyan",
                                "#7FFF7F", "yellow", "#FF7F00", "red", "#7F0000"))
                                
  colord=jet.colors(100)
  
  tiff(file=paste("..\\results\\figure_2\\facet_b.tiff", sep = ""), width=5000, height=2500, res=300, compression="lzw")
  
  p <- ggplot(big_rel_df, aes(x = diff_abs_ah, y = diff_rel_ah, z = first_mty)) +
    theme_bw() +
    stat_summary_hex(bins = 100) +
    xlab("absolute decline in activity hours due to habitat loss [hours/year]") +
    ylab("relative decline in activity hours due to habitat loss [%]") +
    theme(axis.title.y = element_text(size = 22, face = "bold", vjust = 3),
          axis.title.x = element_text(size = 22, face = "bold", vjust = 0),
          legend.text = element_text(size = 18),
          legend.title = element_text(size = 18),
          legend.key.height = unit(2,"cm"),
          legend.title.align = 0.5,
          axis.text.x = element_text(size = 24),
          axis.text.y = element_text(size = 24),
          plot.margin = margin(1,1,1,1, "cm"),
          panel.grid = element_blank()) +
    labs(fill = "Mean annual air\ntemperature [\u00B0C]\n") +
    scale_fill_gradientn(colors = colord) +
    xlim(0,1500) +
    ylim(0,80)
  
  print(p)
  
  dev.off()
}


figure_2_facet_c <- function(mat){
  
  rel_df <- as.data.frame(mat)
  rel_df$mean_ta_year <- rel_df$mean_ta_year - 273.15
  
  time_df <- rel_df %>%
    group_by(id) %>%
    summarise(first_as = first(length_of_activity_season), last_as = last(length_of_activity_season), first_gr = first(growth_rate_per_year), last_gr = last(growth_rate_per_year), first_mty = first(mean_ta_year)) %>%
    mutate(diff_abs_as = last_as - first_as, diff_rel_as = ((last_as - first_as)/last_as)*100)
  
  
  big_rel_df <- merge(rel_df, time_df, by = c("id"))
  
  jet.colors <- #taken from http://senin-seblog.blogspot.com/2008/09/some-r-color-palettes.html
    colorRampPalette(c("#00007F", "blue", "#007FFF", "cyan",
                                "#7FFF7F", "yellow", "#FF7F00", "red", "#7F0000"))
                                
  colord=jet.colors(100)
  
  tiff(file=paste("..\\results\\figure_2\\facet_c.tiff", sep = ""), width=5000, height=2500, res=300, compression="lzw")
  
  p <- ggplot(big_rel_df, aes(x = last_as, y = diff_abs_as, z = first_mty)) +
    theme_bw() +
    stat_summary_hex(bins = 100) +
    xlab("mean activity season length without habitat loss [days]") +
    ylab("absolute decline in mean activity season length due to habitat loss [days]") +
    theme(axis.title.y = element_text(size = 22, face = "bold", vjust = 3),
          axis.title.x = element_text(size = 22, face = "bold", vjust = 0),
          legend.text = element_text(size = 18),
          legend.title = element_text(size = 18),
          legend.key.height = unit(2,"cm"),
          legend.title.align = 0.5,
          axis.text.x = element_text(size = 24),
          axis.text.y = element_text(size = 24),
          plot.margin = margin(1,1,1,1, "cm"),
          panel.grid = element_blank()) +
    labs(fill = "Mean annual air\ntemperature [\u00B0C]\n") +
    scale_fill_gradientn(colors = colord) +
    xlim(0,365) +
    ylim(0,80)
  
  print(p)
  
  dev.off()
}

figure_2_facet_d <- function(mat){
  
  rel_df <- as.data.frame(mat)
  rel_df$mean_ta_year <- rel_df$mean_ta_year - 273.15
  
  time_df <- rel_df %>%
    group_by(id) %>%
    summarise(first_as = first(length_of_activity_season), last_as = last(length_of_activity_season), first_gr = first(growth_rate_per_year), last_gr = last(growth_rate_per_year), first_mty = first(mean_ta_year)) %>%
    mutate(diff_abs_as = last_as - first_as, diff_rel_as = ((last_as - first_as)/last_as)*100)
  
  
  big_rel_df <- merge(rel_df, time_df, by = c("id"))
  
  jet.colors <- #taken from http://senin-seblog.blogspot.com/2008/09/some-r-color-palettes.html
    colorRampPalette(c("#00007F", "blue", "#007FFF", "cyan",
                                "#7FFF7F", "yellow", "#FF7F00", "red", "#7F0000"))
                                
  colord=jet.colors(100)
  
  tiff(file=paste("..\\results\\figure_2\\facet_d.tiff", sep = ""), width=5000, height=2500, res=300, compression="lzw")
  
  p <- ggplot(big_rel_df, aes(x = diff_abs_as, y = diff_rel_as, z = first_mty)) +
    theme_bw() +
    stat_summary_hex(bins = 100) +
    xlab("absolute decline in mean activity season length due to habitat loss [days]") +
    ylab("relative decline in mean activity season length due to habitat loss [%]") +
    theme(axis.title.y = element_text(size = 22, face = "bold", vjust = 3),
          axis.title.x = element_text(size = 22, face = "bold", vjust = 0),
          legend.text = element_text(size = 18),
          legend.title = element_text(size = 18),
          legend.key.height = unit(2,"cm"),
          legend.title.align = 0.5,
          axis.text.x = element_text(size = 24),
          axis.text.y = element_text(size = 24),
          plot.margin = margin(1,1,1,1, "cm"),
          panel.grid = element_blank()) +
    labs(fill = "Mean annual air\ntemperature [\u00B0C]\n") +
    scale_fill_gradientn(colors = colord) +
    xlim(0,100) +
    ylim(0,50)
  
  print(p)
  
  dev.off()
}



