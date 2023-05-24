import sys

sys.path.append("../")

from Summary_by_locations import Summary_by_locations
from Lizard import Lizard
from Lizard_climbing import Lizard_climbing
from Lizard_climbing_13 import Lizard_climbing_13
from Lizard_energy import Lizard_energy
from Climate import Climate
from Day_summary import Day_summary
from Summary import Summary
import Parameters as p
import numpy as np
import time
import argparse


def run_model(inputfilename, path, is_climbing, limited_emergence=True, wanted_day="", var = "0", change = "0"):
    climate = Climate()
    climate.load_data(inputfilename)

    if is_climbing:
        lizard = Lizard_climbing_13(limited_emergence)
    else:
        lizard = Lizard_energy(limited_emergence)

    lizard.sensitivity_analysis(var, change)
    print("lizard mass: " + str(lizard.mass))

    # is there a day we'd like to learn more about?
    if wanted_day != "":
        if wanted_day == True:
            hottest_day = climate.return_hottest_day()
            coldest_day = climate.return_coldest_day()

            m_day_h = hottest_day[0]
            m_month_h = hottest_day[1]
            m_year_h = hottest_day[2]

            m_day_c = coldest_day[0]
            m_month_c = coldest_day[1]
            m_year_c = coldest_day[2]
        else:
            date_of_interest = wanted_day

            m_day = date_of_interest[0]
            m_month = date_of_interest[1]
            m_year = date_of_interest[2]

    # calculating coordinate
    for time_step in range(climate.number_of_steps):
        lizard.step(climate.current_climate, climate.time_step) 
        climate.step()

        if isinstance(lizard, Lizard_climbing):
            if wanted_day != "":
                if (time_step != climate.number_of_steps - 1):
                    if (wanted_day == True):
                        if (climate.current_climate[p.day] == m_day_h) and (
                                climate.current_climate[p.month] == m_month_h) and (
                                climate.current_climate[p.year] == m_year_h) and (climate.current_climate[p.hour] == 0):
                            initial_values_in_hottest_day = vars(lizard).copy()
                        elif (climate.current_climate[p.day] == m_day_c) and (
                                climate.current_climate[p.month] == m_month_c) and (
                                climate.current_climate[p.year] == m_year_c) and (climate.current_climate[p.hour] == 0):
                            initial_values_in_coldest_day = vars(lizard).copy()
                    else:
                        if (climate.current_climate[p.day] == m_day) and (
                                climate.current_climate[p.month] == m_month) and (
                                climate.current_climate[p.year] == m_year) and (climate.current_climate[p.hour] == 0):
                            initial_values_in_wanted_day = vars(lizard).copy()

        print(time_step)

    summary = Summary_by_locations(climate, lizard)
    summary.calculate_statistics(path)
    
    big_summary = Summary(climate,lizard)
    big_summary.calculate_statistics()
    
    # for check
    print("mass of c lizard: " + str(lizard.mass))
    print("emergence_min_To c lizard: " + str(lizard.emergence_min_To))
    print("Vtmin of c lizard: " + str(lizard.Vtmin))
    print("Vtmax of c lizard: " + str(lizard.Vtmax))
    print("alpha_L_direct of c lizard: " + str(lizard.alpha_L_direct))
    print("alpha_L_scattered of c lizard: " + str(lizard.alpha_L_scattered))
    print("ground_insect_abundance of c lizard: " + str(lizard.ground_insect_abundance))
    if isinstance(lizard, Lizard_climbing):
        print("tree_insect_abundance of c lizard: " + str(lizard.tree_insect_abundance))

    print('model running finished successfully!')

    if (isinstance(lizard, Lizard_climbing)) and (wanted_day != ""):
        if (wanted_day == True):
            # day summary of hottest day
            lizard.assign_att_from_dict(initial_values_in_hottest_day)
            # print(initial_values_in_hottest_day)
            # print(lizard)
            climate.go_to_date(m_day_h, m_month_h, m_year_h)

            day_summary = Day_summary()
            day_summary.calculate_day_statistics(climate, lizard, (m_day_h, m_month_h, m_year_h), path, "hottest")

            # day summary of coldest day
            lizard.assign_att_from_dict(initial_values_in_coldest_day)
            # print(initial_values_in_coldest_day)
            # print(lizard)
            climate.go_to_date(m_day_c, m_month_c, m_year_c)

            day_summary = Day_summary()
            day_summary.calculate_day_statistics(climate, lizard, (m_day_c, m_month_c, m_year_c), path, "coldest")
        else:
            lizard.assign_att_from_dict(initial_values_in_wanted_day)
            #print(initial_values_in_wanted_day)
            #print(lizard)
            climate.go_to_date(m_day, m_month, m_year)

            day_summary = Day_summary()
            day_summary.calculate_day_statistics(climate, lizard, (m_day, m_month, m_year), path)



start_time = time.time()

# 2013_MIC_CLIM_36_future_33.832_-111.502
# 2013_MIC_CLIM_36_past_33.832_-111.502
# 3871_MIC_CLIM_36_future_37.573_-104.976
# 3871_MIC_CLIM_36_past_37.573_-104.976
# 10523_MIC_CLIM_36_future_39.774_-74.563
# 10523_MIC_CLIM_36_past_39.774_-74.563

"""
# for sensitivity analysis    
ap = argparse.ArgumentParser()

ap.add_argument("-a", "--var", required = True, help = "variable")
ap.add_argument("-b", "--change", required = True, help = "change rate")

args = vars(ap.parse_args())
var = str(args['var'])
change = float(args['change'])
"""

var = '0'
change = '0'

run = "3.5.22_run"

location = ["2013", "3871", "10523"]
coor = ["_33.832_-111.502", "_37.573_-104.976", "_39.774_-74.563"]
times = ["past", "future"]
#times = ["past"]
climbing = [True, False]
limited = [True]
#possibility for unlimited emeregence of the lizard (no cues needed to get out of the burrow), not used in the paper
#limited = [True, False]


# create directory - use only in the beginning of new run!
import os

path_run = run + "_" + str(var) + "_" + str(change) + "/" + run + "/"


try:
	os.makedirs(path_run)

except OSError:
	print("directory was created earlier, model keeps running...")
	pass

# creating location directories
for i_location in range(len(location)):
		l = location[i_location]
		c = coor[i_location]

		for i_time in range(len(times)):
			t = times[i_time]

			for i_climb in range(len(climbing)):
				if climbing[i_climb]:
					cl = "climbing"
				else:
					cl = "not_climbing"

				for i_limited in range(len(limited)):
					if limited[i_limited]:
						lim = "limited"
					else:
						lim = "unlimited"

					path_new = path_run + "/" + l + "/" + t + "/" + cl + "/" + lim

					try:
						os.makedirs(path_new)

					except OSError:
						print("directory was created earlier, model keeps running...")
						pass

					input_name = l + "_MIC_CLIM_36_" + t + c

					run_model(input_name, path_new, is_climbing = climbing[i_climb], limited_emergence = limited[i_limited], wanted_day = True, var = var, change = change)


"""

# lst = ["2013_MIC_CLIM_36_future_33.832_-111.502", "2013_MIC_CLIM_36_past_33.832_-111.502", "3871_MIC_CLIM_36_future_37.573_-104.976", "3871_MIC_CLIM_36_past_37.573_-104.976", "10523_MIC_CLIM_36_future_39.774_-74.563", "10523_MIC_CLIM_36_past_39.774_-74.563"]

path_run = ".."

# one run template
#run_model("2013_MIC_CLIM_36_future_33.832_-111.502", path_run , is_climbing = False, limited_emergence = True, var = var, change = change)
#run_model("2013_MIC_CLIM_36_past_33.832_-111.502", path_run , is_climbing = False, limited_emergence = True, var = var, change = change)
#run_model("2013_MIC_CLIM_36_future_33.832_-111.502", path_run , is_climbing = True, limited_emergence = True, wanted_day = True, var = var, change = change)
#run_model("2013_MIC_CLIM_36_past_33.832_-111.502", path_run , is_climbing = True, limited_emergence = True, wanted_day = (1,6,1990), var = var, change = change)
#run_model("3871_MIC_CLIM_36_future_37.573_-104.976", path_run , is_climbing = False, limited_emergence = True, var = var, change = change)
#run_model("3871_MIC_CLIM_36_past_37.573_-104.976", path_run , is_climbing = False, limited_emergence = True, var = var, change = change)
#run_model("3871_MIC_CLIM_36_future_37.573_-104.976", path_run , is_climbing = True, limited_emergence = True, wanted_day = True, var = var, change = change)
#run_model("3871_MIC_CLIM_36_past_37.573_-104.976", path_run , is_climbing = True, limited_emergence = True, wanted_day = True, var = var, change = change)
#run_model("10523_MIC_CLIM_36_future_39.774_-74.563", path_run , is_climbing = False, limited_emergence = True, var = var, change = change)
#run_model("10523_MIC_CLIM_36_past_39.774_-74.563", path_run , is_climbing = False, limited_emergence = True, var = var, change = change)
#run_model("10523_MIC_CLIM_36_future_39.774_-74.563", path_run , is_climbing = True, limited_emergence = True, wanted_day = True, var = var, change = change)
#run_model("10523_MIC_CLIM_36_past_39.774_-74.563", path_run , is_climbing = True, limited_emergence = True, wanted_day = True, var = var, change = change)

#run_model("6305_MIC_CLIM_36_past_17.210_-97.372", path_run , is_climbing = True, limited_emergence = True, wanted_day = True, var = var, change = change)
#run_model("6305_MIC_CLIM_36_future_17.210_-97.372", path_run , is_climbing = True, limited_emergence = True, wanted_day = True, var = var, change = change)
#run_model("6305_MIC_CLIM_36_past_17.210_-97.372", path_run , is_climbing = False, limited_emergence = True, var = var, change = change)
#run_model("6305_MIC_CLIM_36_future_17.210_-97.372", path_run , is_climbing = False, limited_emergence = True, var = var, change = change)


"""

# running time calculation
running_time = time.time() - start_time  # in seconds
hours = running_time // 3600
minutes = (running_time % 3600) // 60
seconds = (running_time % 60)
print("Running time: " + str(hours) + " hours, " + str(minutes) + " minutes, " + str(seconds) + " seconds")





