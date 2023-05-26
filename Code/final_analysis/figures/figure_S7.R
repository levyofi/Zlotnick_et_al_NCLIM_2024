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

dir.create("..//results", showWarnings = F)
dir.create("..//results//figure_S7", showWarnings = F)


figure_S7 <- function(mat){
  
  rel_df <- as.data.frame(mat)
  rel_df$mean_ta_year <- rel_df$mean_ta_year - 273.15
  
  
  jet.colors <- #taken from http://senin-seblog.blogspot.com/2008/09/some-r-color-palettes.html
    colorRampPalette(c("#00007F", "blue", "#007FFF", "cyan",
                       "#7FFF7F", "yellow", "#FF7F00", "red", "#7F0000"))
  
  colord=jet.colors(100)
  
  tiff(file=paste("..\\results\\figure_S7\\figure_S7.tiff", sep = ""), width=6000, height=2500, res=300, compression="lzw")
  
  p <- ggplot(rel_df, aes(x = percentage_to_cool, y = mean_height, z = mean_ta_year)) +
    theme_bw() +
    stat_summary_hex(bins = 100) +
    xlab("Percentage of climbing done for cooling [%]") +
    ylab("Mean climbing height when climbing is essential [cm]") +
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
    xlim(0,100) +
    ylim(0,200) 
  
  print(p)
  
  dev.off()
}




