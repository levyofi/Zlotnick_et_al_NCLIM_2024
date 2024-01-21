import numpy as np
import os as os
import pandas as pd

df = pd.read_csv("..//..//Data//lizard_output_for_analysis//deep_data//day_sum_np.csv", index_col= False)

try:
    os.mkdir("..//..//Data//lizard_output_for_analysis//deep_data")

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


d_id = 0
d_time = 1
d_julian_day = 2
d_mean_ta = 3
d_burrow = 4

day_sum_file = open("..//..//Data//lizard_output_for_analysis//deep_data//day_sum_np.csv", 'w')

day_sum_columns = ["id", "time", "julian_day", "mean_ta", "burrow"]

for col in day_sum_columns[:-1]:
    day_sum_file.write(col + ",")
day_sum_file.write(day_sum_columns[-1] + "\n")

my_file = open("..//..//Data//lizard_output_for_analysis//deep_data//all_summed.csv", 'r')
my_file.readline()

day_counter = 1

for i_day in range(10303 * 2 * 365):
    
    day_df = []
    daylight_hours = 0
    
    for i_hour in range(24):
        row = my_file.readline()
        s_row = row.strip().split(",")

        if len(s_row) == 15:
            day_df.append(s_row)

            if s_row[light] == 'True':
                daylight_hours = daylight_hours + 1

    if len(day_df) != 0:
        sum_day_lst = [0] * 5
        sum_day_lst[d_id] = day_df[0][id]
        sum_day_lst[d_time] = day_df[0][time]
        sum_day_lst[d_julian_day] = day_df[0][julian_day]
        sum_day_lst[d_mean_ta] = day_df[0][mean_ta]

        for hour_lst in day_df:
            if hour_lst[light] == 'True':
                sum_day_lst[d_burrow] += float(hour_lst[burrow])


        if daylight_hours != 0:
            sum_day_lst[d_burrow] = sum_day_lst[d_burrow] / daylight_hours

        else:
            sum_day_lst[d_burrow] = None

        # write to files
        for cell in sum_day_lst:
            day_sum_file.write(str(cell) + ",")
        day_sum_file.write("\n")

    print(day_counter)
    day_counter += 1

day_sum_file.close()





