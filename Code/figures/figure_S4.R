library(tidyverse)
library(ggplot2)
library(dplyr)
library(hash)

dir.create("..//results", showWarnings = F)
dir.create("..//results//figure_S4", showWarnings = F)

figure_S4 <- function(){
  
  locations <- c("2013", "3871", "10523")
  location_coos <- c("33.832_-111.502", "37.573_-104.976", "39.774_-74.563")
  times <- c("past", "future")
  climbs <- c("climbing", "not_climbing")
  limiteds <- c("limited")
  limiteds_file_name <- c("limited_emergence_")
  
  h <- hash()
  
  for(i_location in 1:3){
    
    location <- locations[[i_location]]
    location_coo <- location_coos[[i_location]]
    
    for(i_time in 1:2){
      time <- times[[i_time]]
      
      for(i_climb in 1:2){
        climb <- climbs[[i_climb]]
        
        for(i_limited in 1:1){
          limited <- limiteds[[i_limited]]
          limited_file_name <- limiteds_file_name[[i_limited]]
          
          file_name <- character(0)
          path <- paste("..\\input\\results_for_locations\\", sep = "")
          
          path <- paste(path, location, "\\", time, "\\", climb, "\\", limited, "\\", sep="")
          file_name <- paste(file_name, climb, "_", limited_file_name, location, "_MIC_CLIM_36_", time, "_", location_coo, "_statistics.csv", sep="")
          
          key <- paste(location, "_", time, "_", climb, "_", limited, sep="")
          
          h[[key]] <- read.csv(paste(path, file_name, sep=""), header = FALSE, na.strings= c("", NA), col.names = paste0("V",seq_len(25)), fill = TRUE)
          
        }
      }
    }
  }
  
  df <- data.frame(location = character(),
                   time = character(),
                   climbing = character(),
                   limited = character(),
                   hour = numeric(),
                   micro_environment = character(),
                   minutes = double()) 
  
  micro_environments <- c("shade", "open", "burrow", "open_tree", "shaded_tree")
  
  for(i_location in 1:3){
    location <- locations[[i_location]]
    
    for(i_time in 1:2){
      time <- times[[i_time]]
      
      for(i_climb in 1:2){
        climb <- climbs[[i_climb]]
        
        for(i_limited in 1:1){
          limited <- limiteds[[i_limited]]
          
          key <- paste(location, "_", time, "_", climb, "_", limited, sep="" )
          
          for(i_hour in 0:23){
            
            if(climb == "climbing"){
              for(i_micro in 1:5){
                micro <- micro_environments[[i_micro]]
                
                minutes <- h[[key]][i_micro + 34, i_hour + 2]
                
                row <- c(location, time, climb, limited, i_hour, micro, minutes)
                df <- rbind(df, setNames(as.list(row), names(df)))
              }
            }
            else{   
              for(i_micro in 1:3){
                micro <- micro_environments[[i_micro]]
                
                minutes <- h[[key]][i_micro + 24, i_hour + 2]
                
                row <- c(location, time, climb, limited, i_hour, micro, minutes)
                df <- rbind(df, setNames(as.list(row), names(df)))
              }
            }
          }
        }
      }
    }
  }
  
  
  location_names <- c("Arizona", "Colorado", "New Jersey")
  facets <- c("c","b","a")
  df$location[df$location == 2013] <- "Arizona"
  df$location[df$location == 3871] <- "Colorado"
  df$location[df$location == 10523] <- "New Jersey"
  
  
  for(i in 1:length(location_names)){
    
    curr_location <- location_names[i]
    
    rel_df <- df %>%
      filter(limited == "limited") %>%
      filter(location == curr_location) %>%
      filter(time == "future") %>%
      filter(climbing == "climbing")
    
    rel_df$minutes <- as.numeric(rel_df$minutes)
    rel_df$hour <- as.numeric(rel_df$hour)
    
    ground_rel_df <- rel_df %>%
      filter(micro_environment == "open" | micro_environment == "shade") %>%
      group_by(hour) %>%
      summarise(minutes = sum(minutes)) %>%
      mutate(micro_environment = "ground")

    tree_rel_df <- rel_df %>%
      filter(micro_environment == "open_tree" | micro_environment == "shaded_tree") %>%
      select(c(hour, minutes, micro_environment))
    
    
    big_rel_df <- rbind(ground_rel_df, tree_rel_df)
    
    if(curr_location == "Arizona" |  curr_location == "Colorado"){
      big_rel_df$hour <- (big_rel_df$hour - 7) %% 24
    } 
    if(curr_location == "New Jersey"){
      big_rel_df$hour <- (big_rel_df$hour - 5) %% 24
    }
    
    
    ggplot(big_rel_df, aes(x = hour, y = minutes, colour = factor(micro_environment, levels = c("burrow", "ground", "open_tree", "shaded_tree")))) +
      geom_line(size = 2) +
      scale_colour_manual(labels = c("ground", "open tree", "shaded tree"),
                          values = c("dodgerblue3", "red", "green4")) +
      guides(fill = guide_legend(reverse = TRUE)) +
      scale_x_continuous(breaks = seq(0,24,2)) +
      theme_bw() +
      xlab("hour") +
      ylab("mean minutes per hour") +
      theme(panel.grid = element_blank(),
            axis.title.y = element_text(size = 24, face = "bold", vjust = 1),
            axis.title.x = element_text(size = 24, face = "bold", vjust = -1),
            legend.text = element_text(size = 14),
            axis.text.x = element_text(face = "italic", size = 24),
            axis.text.y = element_text(size = 24),
            strip.text.x = element_text(face = "italic", size = 20),
            strip.text.y = element_text(face = "bold", size = 18),
            legend.title = element_blank(),
            legend.spacing.y = unit(0, "cm"),
            plot.margin = margin(1,1,1,1, "cm"),
            panel.spacing = unit(2, "lines")) +
      ylim(0,62)
    
    facet <- facets[i]
    
    plot_path <- paste("..\\results\\figure_S4\\facet_",facet, ".tiff", sep = "")
    ggsave(plot_path, plot = last_plot(), dpi = 1200, height = 17.66, width = 35, units = "cm")
    
  }
  
}
