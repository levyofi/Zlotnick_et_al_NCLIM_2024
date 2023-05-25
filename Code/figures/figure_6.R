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
dir.create("..//results//figure_6", showWarnings = F)

figure_6 <- function(mat){
  
  rel_df <- as.data.frame(mat)
  rel_df$mean_ta_year <- rel_df$mean_ta_year - 273.15
  
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

  jet.colors <- #taken from http://senin-seblog.blogspot.com/2008/09/some-r-color-palettes.html
    colorRampPalette(c("#00007F", "blue", "#007FFF", "cyan",
                       "#7FFF7F", "yellow", "#FF7F00", "red", "#7F0000"))
  
  colord=jet.colors(100)
  
  tiff(file=paste("..\\results\\figure_6\\figure_6.tiff", sep = ""), width=4500, height=3500, res=300, compression="lzw")
  
  p <- ggplot(big_rel_df, aes(x = diff_c_gr, y = diff_habloss_gr, z = first_mty)) +
    theme_bw() +
    stat_summary_hex(bins = 100) +
    xlab("Change in growth rate without habitat loss [lizards/year]") +
    ylab("Change in growth rate with habitat loss [lizards/year]") +
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
    xlim(-12.5,10) +
    ylim(-12.5,10) 
  
  print(p)
  
  dev.off()
  
}
