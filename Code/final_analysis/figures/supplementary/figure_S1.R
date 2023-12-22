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
library(data.table)

dir.create("results", showWarnings = FALSE)
dir.create(paste("results\\supplementary", sep = ""), showWarnings = FALSE)
dir.create(paste("results\\supplementary\\figure_S1", sep = ""), showWarnings = FALSE)

figure_S1 <- function(){
  
  file_name <- "climbing_limited_emergence_2013_MIC_CLIM_36_past_33.832_-111.502__heat_pars.csv"
  path <- paste("..\\..\\Data\\lizard_output_for_analysis\\heat_pars\\", file_name, sep = "")

  df <- read.csv(path) %>%
    filter(shade_level == "open") %>%
    filter(posture == "lying") %>%
    filter(height == "3" | height == "None")
  
  df$height[df$height == "None"] <- "0"
  df$hour <- (df$hour - 6) %% 24
  
  ggplot(df, aes(x = hour, y = solar, colour = height)) +
    geom_line(size = 2) +
    scale_colour_manual(labels = c("on the ground", "on the tree"),
                        values = c("darkorange3","chartreuse3")) +
    #guides(fill = guide_legend(reverse = TRUE)) +
    scale_x_continuous(breaks = c(0,4,8,12,16,20,24)) +
    theme_bw() +
    xlab("Hour") +
    ylab("Solar radiation absorbed by the lizard (watt)") +
    theme(axis.title.x = element_text(size = 18, face = "bold", vjust = -1),
          axis.title.y = element_text(size = 18, face = "bold", vjust = 3),
          legend.text = element_text(size = 14),
          axis.text.x = element_text(face = "italic", size = 26),
          axis.text.y = element_text(size = 26),
          legend.title = element_blank(),
          legend.spacing.y = unit(0, "cm"),
          plot.margin = margin(1,1,1,1, "cm"),
          panel.spacing = unit(2, "lines"),
          panel.grid = element_blank())
  
  plot_path <- "results\\supplementary\\figure_S1\\figure_S1.jpg"
  ggsave(plot_path, plot = last_plot(), dpi = 1200, height = 17.66, width = 35, units = "cm")
  
  
}

