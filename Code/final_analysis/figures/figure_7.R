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
dir.create("..//results//figure_7", showWarnings = F)

figure_7 <- function(){
  
  # open vegetation data
  
  path <- "..\\input\\"
  
  veg_past <- nc_open(paste(path, "FVEG_monthly_past.nc", sep = ""))
  veg_future <- nc_open(paste(path, "FVEG_monthly_future.nc", sep = ""))
  
  veg_past <- ncvar_get(veg_past, "FVEG")
  veg_future <- ncvar_get(veg_future, "FVEG")
  
  veg_past_mat <- apply(veg_past, c(1,2), mean)
  veg_past_mat <- as.data.frame(apply(t(veg_past_mat), 2, rev))
  
  veg_future_mat <- apply(veg_future, c(1,2), mean)
  veg_future_mat <- as.data.frame(apply(t(veg_future_mat), 2, rev))
  
  veg_past_mat <- veg_past_mat[1:100,]
  veg_future_mat <- veg_future_mat[1:100,]
  
  veg_time_diff <- veg_future_mat - veg_past_mat
  
  
  veg_past_mat <- veg_past_mat * 100
  veg_future_mat <- veg_future_mat * 100
  veg_time_diff <- veg_time_diff * 100
  
  
  # open model data
  
  path_2 <- "..\\netcdf_files\\"
  
  data_past_climbing <- nc_open(paste(path_2, "past_climbing.nc", sep = ""))
  data_past_not_climbing <- nc_open(paste(path_2, "past_not_climbing.nc", sep = ""))
  data_future_climbing <- nc_open(paste(path_2, "future_climbing.nc", sep = ""))
  data_future_not_climbing <- nc_open(paste(path_2, "future_not_climbing.nc", sep = ""))
  
  # growth rate data
  
  gr_past_climbing_mat <- ncvar_get(data_past_climbing, "growth_rate_per_year")
  gr_past_not_climbing_mat <- ncvar_get(data_past_not_climbing, "growth_rate_per_year")
  gr_future_climbing_mat <- ncvar_get(data_future_climbing, "growth_rate_per_year")
  gr_future_not_climbing_mat <- ncvar_get(data_future_not_climbing, "growth_rate_per_year")
  
  gr_diff_past_mat <- gr_past_climbing_mat - gr_past_not_climbing_mat
  gr_diff_future_mat <- gr_future_climbing_mat - gr_future_not_climbing_mat
  
  gr_time_diff_mat <- gr_diff_future_mat - gr_diff_past_mat
  
  
  gr_habitat_loss_mat <- gr_future_not_climbing_mat - gr_future_climbing_mat
  gr_climate_change_mat <- gr_future_climbing_mat - gr_past_climbing_mat
  
  gr_mixed_effect <- gr_habitat_loss_mat + gr_climate_change_mat
  
  
  # mean annual temperature data
  
  temp_past_mat <- ncvar_get(data_past_climbing, "mean_ta_year")
  
  
  row_num <- nrow(veg_future_mat)
  col_num <- ncol(veg_future_mat)
  
  past_rel_df <- data.frame(
    vegetation = double(),
    gr_diff = double(),
    mean_ta_year = double(),
    grp = character()
  )
  
  change_rel_df <- data.frame(
    vegetation = double(),
    gr_diff = double(),
    mean_ta_year = double(),
    grp = character()
  )
  
  for(i in 1:row_num){
    for(j in 1:col_num){
      
      if(!is.na(gr_diff_past_mat[[i,j]])){
        
        p_veg <- veg_past_mat[[i,j]]
        c_veg <- veg_time_diff[[i,j]]
        
        p_gr_diff <- gr_diff_past_mat[[i,j]]
        c_gr_diff <- gr_diff_future_mat[[i,j]]
        
        hab_loss_diff <- gr_habitat_loss_mat[[i,j]]
        clim_chng_diff <- gr_climate_change_mat[[i,j]]
        mixed_diff <- gr_mixed_effect[[i,j]]
        
        if(clim_chng_diff < 0){
          grp = "red"
        } else{
          if(mixed_diff < 0){
            grp = "yellow"
          } else{
            grp = "green"
          }
        }
        
        mean_ta_year <- temp_past_mat[[i,j]]
        
        p_row <- t(as.data.frame(c(p_veg, p_gr_diff, mean_ta_year, grp)))  
        c_row <- t(as.data.frame(c(c_veg, c_gr_diff, mean_ta_year, grp)))
        
        
        colnames(p_row) <- c("vegetation", "gr_diff", "mean_ta_year", "grp")
        colnames(c_row) <- c("vegetation", "gr_diff", "mean_ta_year", "grp")
        
        past_rel_df <- rbind(past_rel_df, p_row)
        change_rel_df <- rbind(change_rel_df, c_row)
        
      }
    }
  }
  
  rownames(change_rel_df) <- 1:nrow(change_rel_df)
  
  mat <- change_rel_df
  
  rel_df <- as.data.frame(mat)
  rel_df$mean_ta_year <- as.numeric(rel_df$mean_ta_year) - 273.15
  rel_df$gr_diff <- as.numeric(rel_df$gr_diff)
  rel_df$vegetation <- as.numeric(rel_df$vegetation)
  rel_df$grp <- as.factor(rel_df$grp)
  
  decrease <- rel_df %>%
    filter(vegetation < 0) 
  
  yellow <- decrease %>%
    filter(grp == "yellow")
    
  green <- decrease %>%
    filter(grp == "green")
  
  red <- decrease %>%
    filter(grp == "red")
    
  print(paste("out of", nrow(decrease), "locations where vegetation will decrease,", nrow(red), "are red, and", nrow(yellow), "are yellow (", nrow(green), "are green)"))
  
  jet.colors <- #taken from http://senin-seblog.blogspot.com/2008/09/some-r-color-palettes.html
    colorRampPalette(c("#00007F", "blue", "#007FFF", "cyan",
                       "#7FFF7F", "yellow", "#FF7F00", "red", "#7F0000"))
  
  colord=jet.colors(100)
  
  tiff(file=paste("..\\results\\figure_7\\figure_7.tiff", sep = ""), width=6000, height=2500, res=300, compression="lzw")
  
  p <- ggplot(rel_df, aes(x = vegetation, y = gr_diff, color = factor(grp, levels = c("red", "yellow", "green")))) +
    theme_bw() +
    geom_point(size = 2) +
    #stat_summary_hex(bins = 100) +
    xlab("Change in vegetation fraction [%]") +
    ylab("Contribution of climbing to number of growth rate (in the future)") +
    theme(axis.title.y = element_text(size = 22, face = "bold", vjust = 3),
          axis.title.x = element_text(size = 22, face = "bold", vjust = 0),
          legend.text = element_text(size = 18),
          legend.title = element_blank(),
          legend.key.height = unit(2,"cm"),
          legend.title.align = 0.5,
          axis.text.x = element_text(size = 26),
          axis.text.y = element_text(size = 26),
          plot.margin = margin(1,1,1,1, "cm"),
          panel.grid = element_blank()) +
    scale_colour_manual(values = c("red" = "red", "yellow" = "yellow2", "green" = "chartreuse3")) +
    xlim(-25,15) +
    ylim(0,10) +
    stat_ellipse(geom = "polygon", level = 0.9, alpha = 0.25, size = 1, color = "black",
                 aes(fill = grp)) +
    scale_fill_manual(values = c("red" = "red", "yellow" = "yellow2", "green" = "chartreuse3"))
  
  
  print(p)
  
  dev.off()
  
}




