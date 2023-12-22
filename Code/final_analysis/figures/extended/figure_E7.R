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
library(ggpmisc)

dir.create("results", showWarnings = F)
dir.create("results//extended", showWarnings = F)
dir.create("results//extended//figure_E7", showWarnings = F)


figure_E7_facet_a <- function(mat){
  
  rel_df <- as.data.frame(mat)
  rel_df$mean_ta_year <- rel_df$mean_ta_year - 273.15
  
  time_df <- rel_df %>%
    group_by(id) %>%
    summarise(first_ah = first(annual_activity_hours), last_ah = last(annual_activity_hours), first_gr = first(growth_rate_per_year), last_gr = last(growth_rate_per_year), first_mty = first(mean_ta_year)) %>%
    mutate(diff_ah = first_ah - last_ah, diff_gr = first_gr - last_gr)
  
  
  big_rel_df <- merge(rel_df, time_df, by = c("id"))
  
  jet.colors <- #based on http://senin-seblog.blogspot.com/2008/09/some-r-color-palettes.html
    colorRampPalette(c("#00007F", "blue", "#007FFF", "cyan",
                       "gray", "yellow", "#FF7F00", "red", "#7F0000"))
  
  colord=jet.colors(100)
  
  tiff(file=paste("results//extended//figure_E7//facet_a.tiff", sep = ""), width=6000, height=2500, res=300, compression="lzw")
  
  p <- ggplot(big_rel_df, aes(x = diff_ah, y = diff_gr, z = first_mty)) +
    theme_bw() +
    stat_summary_hex(bins = 100) +
    xlab("Change in mean annual activity hours due to habitat loss") +
    ylab("Change in growth rate due to habitat loss [lizards/year]") +
    theme(axis.title.y = element_text(size = 22, face = "bold", vjust = 3),
          axis.title.x = element_text(size = 22, face = "bold", vjust = 0),
          legend.text = element_text(size = 18),
          legend.title = element_text(size = 18),
          legend.key.height = unit(2,"cm"),
          legend.title.align = 0.5,
          axis.text.x = element_text(size = 30),
          axis.text.y = element_text(size = 30),
          plot.margin = margin(1,1,1,1, "cm"),
          panel.grid = element_blank()) +
    labs(fill = "Mean annual air\ntemperature [\u00B0C]\n") +
    scale_fill_gradientn(colors = colord) +
    xlim(-1500,0) +
    ylim(-10,0) 
  
  print(p)
  
  dev.off()
}


figure_E7_facet_b <- function(mat){
  
  rel_df <- as.data.frame(mat)
  rel_df$mean_ta_year <- rel_df$mean_ta_year - 273.15
  
  time_df <- rel_df %>%
    group_by(id) %>%
    summarise(first_ah = first(annual_activity_hours), last_ah = last(annual_activity_hours), first_gr = first(growth_rate_per_year), last_gr = last(growth_rate_per_year), first_mty = first(mean_ta_year)) %>%
    mutate(diff_ah = ((first_ah - last_ah)/last_ah)*100, diff_gr = ((first_gr - last_gr)/last_gr)*100)
  
  
  big_rel_df <- merge(rel_df, time_df, by = c("id"))
  
  jet.colors <- #based on http://senin-seblog.blogspot.com/2008/09/some-r-color-palettes.html
    colorRampPalette(c("#00007F", "blue", "#007FFF", "cyan",
                       "gray", "yellow", "#FF7F00", "red", "#7F0000"))
  
  colord=jet.colors(100)
  
  tiff(file=paste("results//extended//figure_E7//facet_b.tiff", sep = ""), width=6000, height=2500, res=300, compression="lzw")
  
  p <- ggplot(big_rel_df, aes(x = diff_ah, y = diff_gr, z = first_mty)) +
    theme_bw() +
    stat_summary_hex(bins = 100) +
    xlab("Change in mean annual activity hours due to habitat loss [%]") +
    ylab("Change in growth rate due to habitat loss [%]") +
    theme(axis.title.y = element_text(size = 22, face = "bold", vjust = 3),
          axis.title.x = element_text(size = 22, face = "bold", vjust = 0),
          legend.text = element_text(size = 18),
          legend.title = element_text(size = 18),
          legend.key.height = unit(2,"cm"),
          legend.title.align = 0.5,
          axis.text.x = element_text(size = 30),
          axis.text.y = element_text(size = 30),
          plot.margin = margin(1,1,1,1, "cm"),
          panel.grid = element_blank()) +
    labs(fill = "Mean annual air\ntemperature [\u00B0C]\n") +
    scale_fill_gradientn(colors = colord) +
    xlim(-75,0) +
    ylim(-100,0) 
  
  print(p)
  
  dev.off()
}




