import numpy as np
import pandas as pd
import os
import netCDF4

def find_nth(string, substring, n):
    if (n==1):
        return string.find(substring)
    else:
        return string.find(substring, find_nth(string, substring, n-1) + 1)

os.makedirs("deep_data", exist_ok = True)
files_lst = os.listdir("input/climbing_info_files")

columns = ['julian_day', 'hour', 'daylight', 'burrow', 'open', 'shade', 'open_tree', 'shaded_tree', "ess_open_tree",
           'ess_shaded_tree', 'id', 'lat', 'lon', 'time', 'mean_ta']
ordered_columns = ['id', 'lat', 'lon', 'time', 'mean_ta', 'julian_day', 'hour', 'daylight', 'burrow', 'open', 'shade', 'open_tree', 'shaded_tree', "ess_open_tree",
           'ess_shaded_tree']
big_lst = []


out_file = open("deep_data//all_summed.csv", 'w')
for col in ordered_columns[:-1]:
    out_file.write(str(col) + ",")
out_file.write(str(ordered_columns[-1]))
out_file.write("\n")
out_file.close()


sums_df = pd.read_csv("input/sums.csv", header = None)
sums_df.columns = ["id", "lat", "lon", "time", "climbing", "mean_ta_year", "sd_ta_year", "mean_ta_summer", "sd_ta_summer", "mean_ta_winter", "sd_ta_winter", "energy_gain", "growth_rate", "activity_hours", "activity_days", "first_day", "last_day", "activity_season", "mean_height", "std_height", "mean_height_open", "mean_height_shaded", "perc_to_warm", "perc_to_cool", "perc_mixed", "perc_open", "perc_shaded", "perc_ess_open", "perc_ess_shaded"]

k = 1

for filename in files_lst:
    
    print(k)
    k += 1
    
    id_index = filename.find("_")
    id = filename[0:id_index]
    
    filename_strip = filename.strip(".csv")
    lat_index = find_nth(filename_strip, "_", 5)
    lon_index = find_nth(filename_strip, "_", 6)
    lat = filename_strip[lat_index + 1:lon_index]
    lon = filename_strip[lon_index + 1:]
    
    if "past" in filename_strip:
        time = 0
    elif "future" in filename_strip:
        time = 1
    
    rel_df = sums_df.loc[(sums_df["id"] == float(id)) & (sums_df["time"] == time)]
    mean_ta = list(rel_df.loc[:, "mean_ta_year"])[0] - 273.15
    
    file_df = pd.read_csv("input/climbing_info_files//" + filename)
    file_df = file_df.iloc[:,:-1]
    file_df["id"] = id
    file_df["lat"] = lat
    file_df["lon"] = lon
    file_df["time"] = time
    file_df["mean_ta"] = mean_ta
    
    file_df = file_df[ordered_columns]

    file_df.to_csv("deep_data//all_summed.csv", mode = 'a', header = False, index = False)
    

