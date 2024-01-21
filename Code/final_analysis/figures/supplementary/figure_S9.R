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
dir.create("results/supplementary", showWarnings = F)
dir.create("results/supplementary/figure_S9", showWarnings = F)

figure_S9 <- function(){
  
  rel_df <- read.csv("../../Data/lizard_output_for_analysis/canopy_analysis/sums_with_canopy_cover.csv")
  
  rel_df$time[rel_df$time == 0] <- "past"
  rel_df$time[rel_df$time == 1] <- "future"
  
  rel_df$climbing[rel_df$climbing == 0] <- "not climbing"
  rel_df$climbing[rel_df$climbing == 1] <- "climbing"
  
  rel_df$time <- factor(rel_df$time)
  rel_df$climbing <- factor(rel_df$climbing)
  
  rel_df <- rel_df %>%
    filter(veg >= 10)
  rel_df$mean_ta_year <- rel_df$mean_ta_year - 273.15
  
  clim_df <- rel_df %>%
    filter(climbing == "climbing")
  
  clim_df <- clim_df[order(clim_df$time, decreasing = T),]
  
  clim_melted_df <- clim_df %>%
    group_by(id) %>%
    summarise(past_gr = first(growth_rate_per_year), future_gr = last(growth_rate_per_year), first_mty = first(mean_ta_year)) %>%
    mutate(diff_gr_clim = future_gr - past_gr)
  
  clim_hab_df <- rel_df %>%
    filter((climbing == "climbing" & time == "past") | (climbing == "not climbing" & time == "future"))
  
  clim_hab_df <- clim_hab_df[order(clim_hab_df$time, decreasing = T),]
  
  
  clim_hab_melted_df <- clim_hab_df %>%
    group_by(id) %>%
    summarise(past_gr = first(growth_rate_per_year), future_gr = last(growth_rate_per_year)) %>%
    mutate(diff_gr_clim_hab = future_gr - past_gr)
  
  
  united_melted_df <- merge(clim_melted_df, clim_hab_melted_df, by = "id") %>%
    select(c("id", "first_mty","diff_gr_clim","diff_gr_clim_hab"))
  
  colnames(united_melted_df) <- c("id", "mean_ta", "clim_effect", "clim_hab_effect")
  
  
  colord <- magma(100)
  
  tiff(file=paste("results/supplementary/figure_S9/figure_S9.tiff", sep = ""), width=4500, height=3500, res=300, compression="lzw")
  
  p <- ggplot(united_melted_df, aes(x = clim_effect, y = clim_hab_effect, z = mean_ta)) +
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
          axis.text.x = element_text(size = 30),
          axis.text.y = element_text(size = 30),
          plot.margin = margin(1,1,1,1, "cm"),
          panel.grid = element_blank()) +
    labs(fill = "Mean annual air\ntemperature [\u00B0C]\n") +
    scale_fill_gradientn(colors = colord) +
    xlim(-12.5,10) +
    ylim(-12.5,10) 
  
  print(p)
  
  dev.off()
  
}
