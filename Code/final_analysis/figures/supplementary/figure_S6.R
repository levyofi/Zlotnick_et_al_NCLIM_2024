library(dplyr)
library(ggplot2)
library(rasterVis)
library(tidyverse)
library(ncdf4)
library(reshape2)


dir.create("results", showWarnings = F)
dir.create("results//supplementary", showWarnings = F)
dir.create("results//supplementary//figure_S6", showWarnings = F)

figure_S6 <- function(){
  
  path <- "..//..//Data//lizard_output_for_analysis//deep_data//day_sum_np.csv"
  
  df <- fread(path, sep = ",")
  colnames(df) <- c(colnames(df)[2:length(colnames(df))],"")
  df <- df[,1:(ncol(df)-1)]
  
  df <- df %>%
    mutate(activity = 60 - burrow) 
  
  df <- df[order(time),]
  
  mean_ta_past <- df %>%
    group_by(id) %>%
    summarise(past_mean_ta = first(mean_ta))
  
  
  rel_df <- merge(df, mean_ta_past)
  
  
  rel_df$time <- ifelse(rel_df$time == 0, "past", "future")
  
  
  colord <- magma(100)
  
  days_per_month <- c(0,31,59,90,120,151,181,212,243,273,304,334, 365)
  months <- c("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "")
  
  
  
  tiff(file=paste("results\\supplementary\\figure_S6\\figure_S6.tiff", sep = ""), width=10000, height=4000, res=300, compression="lzw")
  
  p <- ggplot(rel_df, aes(x = julian_day, y = activity, z = past_mean_ta)) + 
    theme_bw() +
    stat_summary_hex(bins = 100) +
    ylab(expression(paste("Time of essential climbing [", frac("minute","hour"),"]", sep = ""))) +
    xlab("Julian day                                                                                         Julian day") +
    theme(axis.title.y = element_text(size = 26, face = "bold", vjust = 6),
          axis.title.x = element_text(size = 26, face = "bold", vjust = -2),
          legend.text = element_text(size = 20),
          legend.title = element_text(size = 24),
          legend.title.align = 0.5,
          axis.text.x = element_text(size = 20, hjust = -0.35),
          axis.text.y = element_text(size = 26),
          strip.text = element_text(size = 34, face = "italic", vjust = 2),
          plot.margin = margin(2,2,2,2, "cm"),
          strip.background = element_blank(),
          panel.grid = element_blank()) +
    scale_fill_gradientn(colors = colord, guide = guide_colorbar(barheight = 20, barwidth = 2, vjust = 10)) + 
    labs(fill = "Mean annual\nair temperature\nin the past\n[Celsius]") +
    facet_grid(. ~ factor(time, levels = c("past", "future"))) +
    scale_y_continuous(limits = c(0,60),breaks = c(0,15,30,45,60)) +
    scale_x_continuous(limits = c(-1,366), breaks = days_per_month , labels = months) +
    facet_grid(. ~ factor(time, levels = c("past", "future")))
  
  print(p)
  
  dev.off()
  
  
}








