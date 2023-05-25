library(tidyverse)
library(ggplot2)
library(dplyr)

dir.create("..\\results", showWarnings = FALSE)
dir.create(paste("..\\results\\figure_S8", sep = ""), showWarnings = FALSE)

figure_S8_facet_a <- function(){
  
  path <- paste("..\\input\\heat_pars\\climbing_limited_emergence_2013_MIC_CLIM_36_past_33.832_-111.502__heat_pars.csv", sep = "")
  
  df <- read.csv(path) %>%
    filter(shade_level == "shade") %>%
    filter(posture == "lying") %>%
    filter(hour == 22) %>%
    filter(height != "None")
  
  df$height[df$height == "None"] <- 0
  df$height <- as.numeric(df$height)
  
  rel_df <- pivot_longer(df, c("cond", "conv"))
  rel_df$value <- -1 * rel_df$value
  
  ggplot(rel_df, aes(x = height, y = value, colour = name)) +
    geom_line(size = 2) +
    scale_colour_manual(labels = c("By conduction", "By convection"),
                        values = c("goldenrod4","dodgerblue3")) +
    #guides(fill = guide_legend(reverse = TRUE)) +
    scale_x_continuous(breaks = c(3,12,21,30,48,66,84,102,120,138,156,174,198)) +
    theme_bw() +
    xlab("Height") +
    ylab("Heat loss of the lizard (watt)") +
    theme(axis.title.x = element_text(size = 18, face = "bold", vjust = -1),
          axis.title.y = element_text(size = 18, face = "bold", vjust = 3),
          legend.text = element_text(size = 14),
          axis.text.x = element_text(size = 20),
          axis.text.y = element_text(size = 20),
          legend.title = element_blank(),
          legend.spacing.y = unit(0, "cm"),
          plot.margin = margin(1,1,1,1, "cm"),
          panel.spacing = unit(2, "lines"),
          panel.grid = element_blank())
  
  plot_path <- "..\\results\\figure_S8\\facet_a.jpeg"
  ggsave(plot_path, plot = last_plot(), dpi = 1200, height = 17.66, width = 35, units = "cm")
  
}

figure_S8_facet_b <- function(){
  
  path <- paste("..\\input\\heat_pars\\tree_height.csv", sep = "")
  
  df <- read.csv(path)
  
  rel_df <- pivot_longer(df, c("wv", "air_temp", "trunk_temp"))
  rel_df$value[rel_df$name != "wv"] <- rel_df$value[rel_df$name != "wv"] - 273.15
  rel_df$value[rel_df$name == "wv"] <- rel_df$value[rel_df$name == "wv"] * 2 + 25
  
  ggplot(rel_df, aes(x = height, y = value, colour = name)) +
    geom_line(size = 2) +
    scale_colour_manual(labels = c("Air temperature", "Trunk temperature", "Wind velocity"),
                        values = c("dodgerblue3", "goldenrod4", "darkgreen")) +
    guides(fill = guide_legend(reverse = TRUE)) +
    scale_x_continuous(breaks = c(3,12,21,30,48,66,84,102,120,138,156,174,198)) +
    theme_bw() +
    xlab("Height") +
    ylab("Temperature (Celsius)") +
    theme(axis.title.x = element_text(size = 18, face = "bold", vjust = -1),
          axis.title.y = element_text(size = 18, face = "bold", vjust = 3),
          legend.text = element_text(size = 14),
          axis.text.x = element_text(size = 20),
          axis.text.y = element_text(size = 20),
          legend.title = element_blank(),
          legend.spacing.y = unit(0, "cm"),
          plot.margin = margin(1,1,1,1, "cm"),
          panel.spacing = unit(2, "lines"),
          panel.grid = element_blank()) + 
    scale_y_continuous(sec.axis = sec_axis(trans = (~.), breaks = c(27,31,35,39), labels = c(1,3,5,7), name=""))
  
  plot_path <- "..\\results\\figure_S8\\facet_b.jpeg"
  ggsave(plot_path, plot = last_plot(), dpi = 1200, height = 17.66, width = 35, units = "cm")
  
}


