import os

import numpy as np
import pandas as pd
import warnings
from numpy.core._multiarray_umath import ndarray

import Parameters as p
from Lizard_climbing import Lizard_climbing
from Lizard_climbing_13 import Lizard_climbing_13
from Lizard_energy import Lizard_energy

class Summary:
    def __init__(self , climate, lizard):
        self.statistics_data = []
        self.climate = climate
        self.lizard = lizard

    def calculate_statistics(self):

        # id
        id = self.climate.inputfilename[0 : self.climate.inputfilename.index("_")]
        self.statistics_data.append(float(id))

        # coordinates
        self.statistics_data.append(self.climate.lat)
        self.statistics_data.append(self.climate.lon)

        # past / future
        if "past" in self.climate.inputfilename:
            time = 0.0
        elif "future" in self.climate.inputfilename:
            time = 1.0

        self.statistics_data.append(time)

        # climbing?
        if isinstance(self.lizard, Lizard_climbing):
            is_climbing = 1.0
        else:
            is_climbing = 0.0

        self.statistics_data.append(is_climbing)

        # coordinate temperatures
        self.statistics_data.append(self.climate.mean_ta_year)
        self.statistics_data.append(self.climate.sd_ta_year)
        self.statistics_data.append(self.climate.mean_ta_summer)
        self.statistics_data.append(self.climate.sd_ta_summer)
        self.statistics_data.append(self.climate.mean_ta_winter)
        self.statistics_data.append(self.climate.sd_ta_winter)

        #self.statistics_data.append(310.0)
        #self.statistics_data.append(310.0)
        #self.statistics_data.append(310.0)
        #self.statistics_data.append(310.0)
        #self.statistics_data.append(310.0)
        #self.statistics_data.append(310.0)

        # total energy
        self.statistics_data.append(sum(self.lizard.energy_gain_per_year) / 20)

        # annual growth rate
        self.statistics_data.append(sum(self.lizard.growth_rate_per_year) / 20)

        # micro-climate counters
        months = np.array(self.climate.climate_data[p.month,:])
        months_per_day = np.array(self.climate.month_per_day)
        days_per_month = [31,28,31,30,31,30,31,31,30,31,30,31]
        SWDOWNs = np.array(self.climate.climate_data[p.SWDOWN,:])
        mask_daylight = np.array([False])
        mask_daylight = np.concatenate((mask_daylight, (SWDOWNs > 1)[:-1]))

        # mean activity hours per day in different months
        activity_ph = np.array(self.lizard.active_per_hour)
        activity_pm = [0] * 12

        for month in range(1, 13):
            mask_month_per_hour = (months == month)
            mask_month_per_day = (months_per_day == month)

            mean_activity_hours_per_day = (sum(activity_ph[mask_month_per_hour]) / 60) / sum(mask_month_per_day)
            activity_pm[month - 1] = mean_activity_hours_per_day * days_per_month[month - 1]

        self.statistics_data.append(sum(activity_pm))

        # activity
        activity_pd = self.lizard.activity_per_day
        # days with activity
        self.statistics_data.append(sum(activity_pd) / 20)

        # first julian day of activity
        activity_pd_a = np.array(activity_pd)
        activity_pd_a = np.reshape(activity_pd_a,(20,365))
        
        first_activity_days = []
        last_activity_days = []
        length_of_activity_season = []
        years_with_no_activity = []

        j = 1
        for year in activity_pd_a:
            if np.any(year) == False:
                years_with_no_activity.append(j)
                length_of_activity_season.append(0)

            else:
                indices = np.nonzero(year)

                first_activity_days.append(indices[0][0] + 1)
                last_activity_days.append(indices[0][-1] + 1)
                season_length = last_activity_days[-1] - first_activity_days[-1]
                length_of_activity_season.append(season_length)

            j += 1
        
        years_with_activity = 20 - len(years_with_no_activity)

        if years_with_activity != 0:
            self.statistics_data.append(sum(first_activity_days) / years_with_activity)
            self.statistics_data.append(sum(last_activity_days) / years_with_activity)
            self.statistics_data.append(sum(length_of_activity_season) / 20)
        else:
            self.statistics_data.append(None)
            self.statistics_data.append(None)
            self.statistics_data.append(0.0)

        # heights
        if isinstance(self.lizard, Lizard_climbing):
            if len(self.lizard.climbing_heights_when_essential) != 0:
                mean_height = np.mean(self.lizard.climbing_heights_when_essential)
                std_height = np.std(self.lizard.climbing_heights_when_essential)
            else:
                mean_height = None
                std_height = None
                
            self.statistics_data.append(mean_height)
            self.statistics_data.append(std_height)
            
            
            if len(self.lizard.climbing_heights_when_essential_open_tree) != 0:
                mean_height_open = np.mean(self.lizard.climbing_heights_when_essential_open_tree)
            else:
                mean_height_open = None

            self.statistics_data.append(mean_height_open)
            
            #print(self.lizard.climbing_heights_when_essential_shaded_tree)
            
            if len(self.lizard.climbing_heights_when_essential_shaded_tree) != 0:
                mean_height_shaded = np.mean(self.lizard.climbing_heights_when_essential_shaded_tree)
            else:
                mean_height_shaded = None

            self.statistics_data.append(mean_height_shaded)

            

            # why climbing?
            if sum(self.lizard.essential_climbing_per_hour) != 0:
                to_warm = (sum(self.lizard.climbing_to_warm_per_hour) / sum(self.lizard.essential_climbing_per_hour)) * 100
                to_cool = (sum(self.lizard.climbing_to_cool_per_hour) / sum(self.lizard.essential_climbing_per_hour)) * 100
                mixed = (sum(self.lizard.climbing_mixed) / sum(self.lizard.essential_climbing_per_hour)) * 100
                
                open_tree = (sum(self.lizard.essential_climbing_on_open_tree) / sum(self.lizard.essential_climbing_per_hour)) * 100
                shaded_tree = (sum(self.lizard.essential_climbing_on_shaded_tree) / sum(self.lizard.essential_climbing_per_hour)) * 100
            else:
                to_warm = -1.0
                to_cool = -1.0
                mixed = -1.0

                open_tree = -1.0
                shaded_tree = -1.0

            self.statistics_data.append(to_warm)
            self.statistics_data.append(to_cool)
            self.statistics_data.append(mixed)

            self.statistics_data.append(open_tree)
            self.statistics_data.append(shaded_tree)
            
            # how much essential from all climbing (for open and shaded tree)?

            if sum(self.lizard.open_tree_per_hour) != 0:
                prec_of_essential_open_tree = (sum(self.lizard.essential_climbing_on_open_tree) / sum(self.lizard.open_tree_per_hour)) * 100
            else:
                prec_of_essential_open_tree = -1.0
            
            if sum(self.lizard.shaded_tree_per_hour) != 0:
                prec_of_essential_shaded_tree = (sum(self.lizard.essential_climbing_on_shaded_tree) / sum(self.lizard.shaded_tree_per_hour)) * 100
            else:
                prec_of_essential_shaded_tree = -1.0

            self.statistics_data.append(prec_of_essential_open_tree)
            self.statistics_data.append(prec_of_essential_shaded_tree)

        else:
            for i in range(11):
                self.statistics_data.append(None)

        self.statistics_data = np.array(self.statistics_data).astype(np.float64)

        
        
        ## additional information - about climbing

        """
        if isinstance(self.lizard, Lizard_climbing):

            number_of_rows = 365 * 24
            columns = ['julian_day', 'hour', 'daylight', 'burrow', 'open', 'shade', 'open_tree', 'shaded_tree', 'ess_open_tree', 'ess_shaded_tree']
            big_lst = []
            big_lst.append(columns)
            
            daylight_mat_add = np.array(self.lizard.daylight_per_hour)
            burrow_mat_add = np.array(self.lizard.burrow_per_hour)
            burrow_night_mat_add = np.array(self.lizard.burrow_per_hour_night)
            open_mat_add = np.array(self.lizard.open_per_hour)
            shade_mat_add = np.array(self.lizard.shade_per_hour)
            shade_night_mat_add = np.array(self.lizard.shade_per_hour_night)
            open_tree_mat_add = np.array(self.lizard.open_tree_per_hour)
            shaded_tree_mat_add = np.array(self.lizard.shaded_tree_per_hour)
            ess_open_tree_mat_add = np.array(self.lizard.essential_climbing_on_open_tree)
            ess_shaded_tree_mat_add = np.array(self.lizard.essential_climbing_on_shaded_tree)

            #daylight_for_print = pd.DataFrame(np.reshape(daylight_mat_add, (20, 8760)).tolist())
            #daylight_for_print.to_csv("daylight.csv")
            

            daylight_mat_add = np.reshape(daylight_mat_add, (20, 365, 24))
            burrow_mat_add = np.reshape(burrow_mat_add, (20, 365, 24))
            burrow_night_mat_add = np.reshape(burrow_night_mat_add, (20, 365, 24))
            open_mat_add = np.reshape(open_mat_add, (20, 365, 24))
            shade_mat_add = np.reshape(shade_mat_add, (20, 365, 24))
            shade_night_mat_add = np.reshape(shade_night_mat_add, (20, 365, 24))
            open_tree_mat_add = np.reshape(open_tree_mat_add, (20, 365, 24))
            shaded_tree_mat_add = np.reshape(shaded_tree_mat_add, (20, 365, 24))
            ess_open_tree_mat_add = np.reshape(ess_open_tree_mat_add, (20, 365, 24))
            ess_shaded_tree_mat_add = np.reshape(ess_shaded_tree_mat_add, (20, 365, 24))
            
            #daylight_means_add = np.all(daylight_mat_add, axis = 0)
            daylight_means_add = np.sum(daylight_mat_add, axis=0) >= 10
            daylight_sums_add = np.sum(daylight_mat_add, axis = 0)
            special_hours = np.logical_and((np.sum(daylight_mat_add, axis = 0) != 0), (np.sum(daylight_mat_add, axis = 0) != 20))
            #daylight_special_hours = (np.sum(daylight_mat_add, axis = 0) != 0) or (np.sum(daylight_mat_add, axis = 0) != 0)
            #print(daylight_special_hours)
            #daylight_for_print = pd.DataFrame(daylight_special_hours.tolist())
            #daylight_for_print.to_csv("daylight.csv")
            
            burrow_means_add = np.mean(burrow_mat_add, axis = 0)
            burrow_night_means_add = np.mean(burrow_night_mat_add, axis=0)
            open_means_add = np.mean(open_mat_add, axis=0)
            shade_means_add = np.mean(shade_mat_add, axis=0)
            shade_night_means_add = np.mean(shade_night_mat_add, axis=0)
            open_tree_means_add = np.mean(open_tree_mat_add, axis=0)
            shaded_tree_means_add = np.mean(shaded_tree_mat_add, axis=0)
            ess_open_tree_means_add = np.mean(ess_open_tree_mat_add, axis=0)
            ess_shaded_tree_means_add = np.mean(ess_shaded_tree_mat_add, axis=0)
            
            #daylight_for_print = pd.DataFrame(daylight_means_add.tolist())
            #daylight_for_print.to_csv("daylight.csv")
            
            for jd in range(365):
                for h in range(24):
                    
                    special_hour_val = special_hours[jd, h]
                    daylight_val_add = daylight_means_add[jd, h]
                    burrow_day_val_add = burrow_means_add[jd, h]
                    burrow_night_val_add = burrow_night_means_add[jd, h]
                    open_val_add = open_means_add[jd, h]
                    shade_day_val_add = shade_means_add[jd, h]
                    shade_night_val_add = shade_night_means_add[jd, h]
                    open_tree_val_add = open_tree_means_add[jd, h]
                    shaded_tree_val_add = shaded_tree_means_add[jd, h]
                    ess_open_tree_val_add = ess_open_tree_means_add[jd, h]
                    ess_shaded_tree_val_add = ess_shaded_tree_means_add[jd, h]
                    
                    if special_hour_val == True:
    
                        day_years = daylight_sums_add[jd, h]
                        night_years = 20 - day_years
                        
                        if daylight_val_add == True:    # marked as day
                            burrow_val_add = (burrow_day_val_add * 20) / day_years
                            shade_val_add = (shade_day_val_add * 20) / day_years
                            open_val_add = (open_val_add * 20) / day_years
                            open_tree_val_add = (open_tree_val_add * 20) / day_years
                            shaded_tree_val_add = (shaded_tree_val_add * 20) / day_years
                            ess_open_tree_val_add = (ess_open_tree_val_add * 20) / day_years
                            ess_shaded_tree_val_add = (ess_shaded_tree_val_add * 20) / day_years
                        else:
                            burrow_val_add = (burrow_night_val_add * 20) / night_years
                            shade_val_add = (shade_night_val_add * 20) / night_years
                            open_val_add = 0
                            open_tree_val_add = 0
                            shaded_tree_val_add = 0
                            ess_open_tree_val_add = 0
                            ess_shaded_tree_val_add = 0
                    else:
                        burrow_val_add = burrow_day_val_add + burrow_night_val_add
                        shade_val_add = shade_day_val_add + shade_night_val_add
                    
                    
                    row_lst = [jd + 1, h, daylight_val_add, burrow_val_add, open_val_add, shade_val_add, open_tree_val_add, shaded_tree_val_add, ess_open_tree_val_add, ess_shaded_tree_val_add]
                    big_lst.append(row_lst)

            os.makedirs("climbing_info_files", exist_ok=True)
            out_file_name = "climbing_info_files/" + self.climate.inputfilename[:-3] + ".csv"
            out_file = open(out_file_name, 'w')
            for row in big_lst:
                for column in row:
                    out_file.write(str(column) + ",")
                out_file.write("\n")
            out_file.close()

        """
        
        return self.statistics_data


