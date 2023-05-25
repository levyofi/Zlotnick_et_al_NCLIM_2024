import numpy as np
import os as os

try:
    os.mkdir("deep_data//results_np")
    
    os.mkdir("deep_data//results_np//daytime_np")
    os.mkdir("deep_data//results_np//daytime_np//seasons")
    
    os.mkdir("deep_data//results_np//night_np")
    os.mkdir("deep_data//results_np//night_np//seasons")

except FileExistsError:
    pass

# enum
id = 0
lat = 1
lon = 2
time = 3
mean_ta = 4
julian_day = 5
hour = 6
light = 7
burrow = 8
open_m = 9
shade = 10
open_tree = 11
shaded_tree = 12
ess_open_tree = 13
ess_shaded_tree = 14
season = 15
pod_m = 16

n_id = 0
n_time = 1
n_julian_day = 2
n_mean_ta = 3
n_burrow = 4
n_shade = 5

d_id = 0
d_time = 1
d_julian_day = 2
d_mean_ta = 3
d_burrow = 4
d_open = 5
d_shade = 6
d_open_tree = 7
d_shaded_tree = 8
d_ess_open_tree = 9
d_ess_shaded_tree = 10


day_winter_file = open("deep_data//results_np//daytime_np//seasons//day_winter.csv", 'w')
day_spring_file = open("deep_data//results_np//daytime_np//seasons//day_spring.csv", 'w')
day_summer_file = open("deep_data//results_np//daytime_np//seasons//day_summer.csv", 'w')
day_autumn_file = open("deep_data//results_np//daytime_np//seasons//day_autumn.csv", 'w')

night_winter_file = open("deep_data//results_np//night_np//seasons//night_winter.csv", 'w')
night_spring_file = open("deep_data//results_np//night_np//seasons//night_spring.csv", 'w')
night_summer_file = open("deep_data//results_np//night_np//seasons//night_summer.csv", 'w')
night_autumn_file = open("deep_data//results_np//night_np//seasons//night_autumn.csv", 'w')

day_sum_file = open("deep_data//results_np//day_sum_np.csv", 'w')
night_sum_file = open("deep_data//results_np//night_sum_np.csv", 'w')

day_season_columns = ["id", "lat", "lon", "time", "mean_ta", "julian_day", "hour", "daylight", "burrow", "open", "shade", "open_tree", "shaded_tree", "ess_open_tree", "ess_shaded_tree", "season", "pod"]
day_sum_columns = ["id", "time", "julian_day", "mean_ta", "burrow", "open", "shade", "open_tree", "shaded_tree", "ess_open_tree", "ess_shaded_tree"]
night_season_columns = ["id", "lat", "lon", "time", "mean_ta", "julian_day", "hour", "daylight", "burrow", "open", "shade", "open_tree", "shaded_tree", "ess_open_tree", "ess_shaded_tree", "season", "pod"]
night_sum_columns = ["id", "time", "julian_day", "mean_ta", "burrow", "shade"]

for col in day_season_columns[:-1]:
    day_autumn_file.write(col + ",")
    day_spring_file.write(col + ",")
    day_summer_file.write(col + ",")
    day_winter_file.write(col + ",")
day_autumn_file.write(day_season_columns[-1] + "\n")
day_spring_file.write(day_season_columns[-1] + "\n")
day_summer_file.write(day_season_columns[-1] + "\n")
day_winter_file.write(day_season_columns[-1] + "\n")

for col in night_season_columns[:-1]:
    night_autumn_file.write(col + ",")
    night_spring_file.write(col + ",")
    night_summer_file.write(col + ",")
    night_winter_file.write(col + ",")
night_autumn_file.write(night_season_columns[-1] + "\n")
night_spring_file.write(night_season_columns[-1] + "\n")
night_summer_file.write(night_season_columns[-1] + "\n")
night_winter_file.write(night_season_columns[-1] + "\n")

for col in day_sum_columns[:-1]:
    day_sum_file.write(col + ",")
day_sum_file.write(day_sum_columns[-1] + "\n")

for col in night_sum_columns[:-1]:
    night_sum_file.write(col + ",")
night_sum_file.write(night_sum_columns[-1] + "\n")

my_file = open("deep_data//all_summed.csv", 'r')
my_file.readline()

day_counter = 1

for i_day in range(10303 * 2 * 365):
    
    day_df = []
    daylight_hours = 0
    
    for i_hour in range(24):
        row = my_file.readline()
        s_row = row.strip().split(",")
        day_df.append(s_row)
        
        if s_row[light] == 'True':
            daylight_hours = daylight_hours + 1

    pod_hours = daylight_hours // 3
    noon_hours = (daylight_hours // 3) + daylight_hours % 3

    first = 0
    last = 23

    for i_hour in range(24):
        light_i = day_df[i_hour][light]
        
        if i_hour == 0:
            light_iminus1 = day_df[23][light]
        else:
            light_iminus1 = day_df[i_hour - 1][light]
            
        if i_hour == 23:
            light_iplus1 = day_df[0][light]
        else:
            light_iplus1 = day_df[i_hour + 1][light]
    
        if (light_i == "True") & (light_iminus1 == "False"):
            first = i_hour
        if (light_i == "True") & (light_iplus1 == "False"):
            last = i_hour
    
    sum_day_lst = [0] * 11
    sum_day_lst[d_id] = day_df[0][id]
    sum_day_lst[d_time] = day_df[0][time]
    sum_day_lst[d_julian_day] = day_df[0][julian_day]
    sum_day_lst[d_mean_ta] = day_df[0][mean_ta]
    
    sum_night_lst = [0] * 6
    sum_night_lst[n_id] = day_df[0][id]
    sum_night_lst[n_time] = day_df[0][time]
    sum_night_lst[n_julian_day] = day_df[0][julian_day]
    sum_night_lst[n_mean_ta] = day_df[0][mean_ta]
    
    for hour_lst in day_df:
    
        new_hour_lst = hour_lst
        curr_jd = float(new_hour_lst[julian_day])

        # append season cell
        if curr_jd <= 59:
            new_hour_lst.append("winter")
        elif (curr_jd > 59) and (curr_jd <= 151):
            new_hour_lst.append("spring")
        elif (curr_jd > 151) and (curr_jd <= 243):
            new_hour_lst.append("summer")
        elif (curr_jd > 243) and (curr_jd <= 334):
            new_hour_lst.append("autumn")
        elif (curr_jd > 334):
            new_hour_lst.append("winter")
            
        # append part of day
        
        i_hour = float(new_hour_lst[hour])
        
        if new_hour_lst[light] == 'False':
            pod = "night"
            
        else:
            if (first == 0) and (last == 23):
                if (i_hour < 8):
                    pod = "morning"
                elif (i_hour >= 8) and (i_hour < 16):
                    pod = "noon"
                elif (i_hour >= 16):
                    pod = "evening"

            elif first < last:
                if (i_hour >= first) & (i_hour < (first + pod_hours)):
                    pod = "morning"
                elif (i_hour >= first + pod_hours) & (i_hour < (first + pod_hours + noon_hours)):
                    pod = "noon"
                elif (i_hour >= (first + pod_hours + noon_hours)) & (i_hour <= last):
                    pod = "evening"

            elif (first > last):
                if (i_hour < first):
                    j = i_hour + 24
                else:
                    j = i_hour
        
                if (j >= first) and (j < (first + pod_hours)):
                    pod = "morning"
                elif (j >= (first + pod_hours)) and (j < (first + pod_hours + noon_hours)):
                    pod = "noon"
                elif (j >= (first + pod_hours + noon_hours)) and (j <= last + 24):
                    pod = "evening"
        
        new_hour_lst.append(pod)
        
        if new_hour_lst[light] == 'True':
            # sum things of the day
            sum_day_lst[d_burrow] += float(new_hour_lst[burrow])
            sum_day_lst[d_open] += float(new_hour_lst[open_m])
            sum_day_lst[d_shade] += float(new_hour_lst[shade])
            sum_day_lst[d_open_tree] += float(new_hour_lst[open_tree])
            sum_day_lst[d_shaded_tree] += float(new_hour_lst[shaded_tree])
            sum_day_lst[d_ess_open_tree] += float(new_hour_lst[ess_open_tree])
            sum_day_lst[d_ess_shaded_tree] += float(new_hour_lst[ess_shaded_tree])
            
            # write to seasons files
            if new_hour_lst[season] == "winter":
                for cell in new_hour_lst:
                    day_winter_file.write(str(cell) + ",")
                day_winter_file.write("\n")
                
            elif new_hour_lst[season] == "spring":
                for cell in new_hour_lst:
                    day_spring_file.write(str(cell) + ",")
                day_spring_file.write("\n")
                
            elif new_hour_lst[season] == "summer":
                for cell in new_hour_lst:
                    day_summer_file.write(str(cell) + ",")
                day_summer_file.write("\n")
                
            elif new_hour_lst[season] == "autumn":
                for cell in new_hour_lst:
                    day_autumn_file.write(str(cell) + ",")
                day_autumn_file.write("\n")
            
        else:
            # sum things of the day
            sum_night_lst[n_burrow] += float(new_hour_lst[burrow])
            sum_night_lst[n_shade] += float(new_hour_lst[shade])

            # write to seasons files
            if new_hour_lst[season] == "winter":
                for cell in new_hour_lst:
                    night_winter_file.write(str(cell) + ",")
                night_winter_file.write("\n")

            elif new_hour_lst[season] == "spring":
                for cell in new_hour_lst:
                    night_spring_file.write(str(cell) + ",")
                night_spring_file.write("\n")

            elif new_hour_lst[season] == "summer":
                for cell in new_hour_lst:
                    night_summer_file.write(str(cell) + ",")
                night_summer_file.write("\n")

            elif new_hour_lst[season] == "autumn":
                for cell in new_hour_lst:
                    night_autumn_file.write(str(cell) + ",")
                night_autumn_file.write("\n")

    if daylight_hours != 0:
        sum_day_lst[d_burrow] = sum_day_lst[d_burrow] / daylight_hours
        sum_day_lst[d_open] = sum_day_lst[d_open] / daylight_hours
        sum_day_lst[d_shade] = sum_day_lst[d_shade] / daylight_hours
        sum_day_lst[d_open_tree] = sum_day_lst[d_open_tree] / daylight_hours
        sum_day_lst[d_shaded_tree] = sum_day_lst[d_shaded_tree] / daylight_hours
        sum_day_lst[d_ess_open_tree] = sum_day_lst[d_ess_open_tree] / daylight_hours
        sum_day_lst[d_ess_shaded_tree] = sum_day_lst[d_ess_shaded_tree] / daylight_hours
    else:
        sum_day_lst[d_burrow:] = [None] * 7
    
    nighttime_hours = 24 - daylight_hours
    
    if nighttime_hours != 0:
        sum_night_lst[n_burrow] = sum_night_lst[n_burrow] / nighttime_hours
        sum_night_lst[n_shade] = sum_night_lst[n_shade] / nighttime_hours
    else:
        sum_night_lst[n_burrow:] = [None] * 2

    # write to files
    for cell in sum_day_lst:
        day_sum_file.write(str(cell) + ",")
    day_sum_file.write("\n")

    for cell in sum_night_lst:
        night_sum_file.write(str(cell) + ",")
    night_sum_file.write("\n")
    
    print(day_counter)
    day_counter += 1
    
    

day_winter_file.close()
day_spring_file.close()
day_summer_file.close()
day_autumn_file.close()

night_winter_file.close()
night_spring_file.close()
night_summer_file.close()
night_autumn_file.close()

day_sum_file.close()
night_sum_file.close()




