import operator

import numpy as np
import warnings
from numpy.core._multiarray_umath import ndarray

import Parameters as p
from Lizard_climbing import Lizard_climbing
from Lizard_energy import Lizard_energy


class Summary_by_locations:
    def __init__(self, climate, lizard):
        self.statistics_data = []
        self.statistics_names = []
        self.climate = climate
        self.lizard = lizard

    def calculate_statistics(self, path):

        # coordinate temperatures
        self.statistics_data.append(self.climate.mean_ta_year)
        self.statistics_data.append(self.climate.sd_ta_year)
        self.statistics_data.append(self.climate.mean_ta_summer)
        self.statistics_data.append(self.climate.sd_ta_summer)
        self.statistics_data.append(self.climate.mean_ta_winter)
        self.statistics_data.append(self.climate.sd_ta_winter)

        self.statistics_names.append("mean annual temperature")
        self.statistics_names.append("sd of mean annual temperature")
        self.statistics_names.append("mean summer temperature")
        self.statistics_names.append("sd of mean summer temperature")
        self.statistics_names.append("mean winter temperature")
        self.statistics_names.append("sd of mean winter temperature")

        # total energy
        self.statistics_data.append(sum(self.lizard.energy_gain_per_year) / 20)
        self.statistics_names.append("mean energy gain per year")

        # annual growth rate
        self.statistics_data.append(sum(self.lizard.growth_rate_per_year) / 20)
        self.statistics_names.append("mean growth rate per year")


        months = np.array(self.climate.climate_data[p.month, :])
        months_per_day = np.array(self.climate.month_per_day)

        # mean activity hours per day in different months and different micro-environments
        activity_ph = np.array(self.lizard.active_per_hour)
        activity_pm = [0] * 12

        activity_open_ph = np.array(self.lizard.active_in_open_per_hour)
        activity_open_pm = [0] * 12

        activity_shade_ph = np.array(self.lizard.active_in_shade_per_hour)
        activity_shade_pm = [0] * 12

        if isinstance(self.lizard, Lizard_climbing):
            activity_open_tree_ph = np.array(self.lizard.active_on_open_tree_per_hour)
            activity_open_tree_pm = [0] * 12

            activity_shaded_tree_ph = np.array(self.lizard.active_on_shaded_tree_per_hour)
            activity_shaded_tree_pm = [0] * 12

        for month in range(1, 13):
            mask_month_per_hour = (months == month)
            mask_month_per_day = (months_per_day == month)

            mean_activity_hours_per_day = (sum(activity_ph[mask_month_per_hour]) / sum(mask_month_per_day)) / 60
            activity_pm[month - 1] = mean_activity_hours_per_day

            mean_activity_hours_per_day_open = (sum(activity_open_ph[mask_month_per_hour]) / sum(mask_month_per_day)) / 60
            activity_open_pm[month - 1] = mean_activity_hours_per_day_open

            mean_activity_hours_per_day_shade = (sum(activity_shade_ph[mask_month_per_hour]) / sum(mask_month_per_day)) / 60
            activity_shade_pm[month - 1] = mean_activity_hours_per_day_shade

            if isinstance(self.lizard, Lizard_climbing):
                mean_activity_hours_per_day_open_tree = (sum(activity_open_tree_ph[mask_month_per_hour]) / sum(mask_month_per_day)) / 60
                activity_open_tree_pm[month - 1] = mean_activity_hours_per_day_open_tree

                mean_activity_hours_per_day_shaded_tree = (sum(activity_shaded_tree_ph[mask_month_per_hour]) / sum(mask_month_per_day)) / 60
                activity_shaded_tree_pm[month - 1] = mean_activity_hours_per_day_shaded_tree


        self.statistics_data.append(activity_pm)
        self.statistics_names.append("mean activity hours per day in different months (hours)")

        self.statistics_data.append(activity_open_pm)
        self.statistics_names.append("mean activity hours in the open per day in different months (hours)")

        self.statistics_data.append(activity_shade_pm)
        self.statistics_names.append("mean activity hours in the shade per day in different months (hours)")

        if isinstance(self.lizard, Lizard_climbing):
            self.statistics_data.append(activity_open_tree_pm)
            self.statistics_names.append("mean activity hours on an open tree per day in different months (hours)")

            self.statistics_data.append(activity_shaded_tree_pm)
            self.statistics_names.append("mean activity hours on a shaded tree per day in different months (hours)")

        # micro-climate counters

        SWDOWNs = np.array(self.climate.climate_data[p.SWDOWN, :])
        mask_daylight = np.array([False])
        mask_daylight = np.concatenate((mask_daylight, (SWDOWNs > 1)[:-1]))

        # burrow per month - day
        burrow_a = np.array(self.lizard.burrow_part_from_daytime_per_day)
        burrow = [0] * 12

        # shade per month - day
        spd_a = np.array(self.lizard.shade_part_from_daytime_per_day)
        spm = [0] * 12

        # open per month
        opd_a = np.array(self.lizard.open_part_from_daytime_per_day)
        opm = [0] * 12

        if isinstance(self.lizard, Lizard_climbing):
            # tree per month - open
            tpd_o_a = np.array(self.lizard.tree_open_part_from_daytime_per_day)
            tpm_o = [0] * 12

            # tree per month - shade
            tpd_s_a = np.array(self.lizard.tree_shade_part_from_daytime_per_day)
            tpm_s = [0] * 12

            # tree to get warm per month
            t_warm_pd_a = np.array(self.lizard.tree_to_warm_part_from_daytime_per_day)
            t_warm_pm = [0] * 12

            # tree to get cool per month
            t_cool_pd_a = np.array(self.lizard.tree_to_cool_part_from_daytime_per_day)
            t_cool_pm = [0] * 12

            # tree essential for activity per month - but not to warm or to cool
            t_ess_mixed_pd_a = np.array(self.lizard.tree_mixed_part_from_daytime_per_day)
            t_ess_mixed_pm = [0] * 12

            # tree essential for activity per month
            t_ess_pd_a = np.array(self.lizard.tree_ess_part_from_daytime_per_day)
            t_ess_pm = [0] * 12

        # burrow per month - night
        burrow_night_a = np.array(self.lizard.burrow_part_from_night_per_day)
        burrow_night = [0] * 12

        # shade per month - night
        spd_night_a = np.array(self.lizard.shade_part_from_night_per_day)
        spm_night = [0] * 12

        for month in range(1, 13):
            mask_month_per_day = (months_per_day == month)

            mean_hours_in_burrow_per_day = sum(burrow_a[mask_month_per_day]) / sum(mask_month_per_day)
            burrow[month - 1] = mean_hours_in_burrow_per_day

            mean_hours_in_shade_per_day = sum(spd_a[mask_month_per_day]) / sum(mask_month_per_day)
            spm[month - 1] = mean_hours_in_shade_per_day

            mean_hours_in_open_per_day = sum(opd_a[mask_month_per_day]) / sum(mask_month_per_day)
            opm[month - 1] = mean_hours_in_open_per_day

            mean_hours_in_burrow_per_day_night = sum(burrow_night_a[mask_month_per_day]) / sum(mask_month_per_day)
            burrow_night[month - 1] = mean_hours_in_burrow_per_day_night

            mean_hours_in_shade_per_day_night = sum(spd_night_a[mask_month_per_day]) / sum(mask_month_per_day)
            spm_night[month - 1] = mean_hours_in_shade_per_day_night

            if isinstance(self.lizard, Lizard_climbing):
                mean_hours_in_tree_open_per_day = sum(tpd_o_a[mask_month_per_day]) / sum(mask_month_per_day)
                tpm_o[month - 1] = mean_hours_in_tree_open_per_day

                mean_hours_in_tree_shade_per_day = sum(tpd_s_a[mask_month_per_day]) / sum(mask_month_per_day)
                tpm_s[month - 1] = mean_hours_in_tree_shade_per_day

                mean_hours_on_tree_to_warm_per_day = sum(t_warm_pd_a[mask_month_per_day]) / sum(mask_month_per_day)
                t_warm_pm[month - 1] = mean_hours_on_tree_to_warm_per_day

                mean_hours_on_tree_to_cool_per_day = sum(t_cool_pd_a[mask_month_per_day]) / sum(mask_month_per_day)
                t_cool_pm[month - 1] = mean_hours_on_tree_to_cool_per_day

                mean_hours_on_tree_mixed_per_day = sum(t_ess_mixed_pd_a[mask_month_per_day]) / sum(mask_month_per_day)
                t_ess_mixed_pm[month - 1] = mean_hours_on_tree_mixed_per_day

                mean_hours_on_tree_ess_per_day = sum(t_ess_pd_a[mask_month_per_day]) / sum(mask_month_per_day)
                t_ess_pm[month - 1] = mean_hours_on_tree_ess_per_day

        self.statistics_data.append(burrow)
        self.statistics_names.append("mean time in the burrow in different months (percentage from day time)")

        self.statistics_data.append(spm)
        self.statistics_names.append("mean time in the shade in different months (percentage from day time)")

        self.statistics_data.append(opm)
        self.statistics_names.append("mean time in the open in different months (percentage from day time)")

        if isinstance(self.lizard, Lizard_climbing):
            self.statistics_data.append(tpm_o)
            self.statistics_names.append("mean time on a open tree in different months (percentage from day time)")

            self.statistics_data.append(tpm_s)
            self.statistics_names.append("mean time on a shaded tree in different months (percentage from day time)")

            self.statistics_data.append(t_warm_pm)
            self.statistics_names.append(
                "mean time in which the lizard is climbing to get warm (percentage from day time) - in different months")

            self.statistics_data.append(t_cool_pm)
            self.statistics_names.append(
                "mean time in which the lizard is climbing to get cool (percentage from day time) - in different months")

            self.statistics_data.append(t_ess_mixed_pm)
            self.statistics_names.append(
                "mean time in which the lizard climbs not specifically to cool or warm - but still essential (percentage from day time) - in different months")

            self.statistics_data.append(t_ess_pm)
            self.statistics_names.append(
                "mean time in which the the tree was the only option for activity (percentage from day time) - in different months")

        self.statistics_data.append(burrow_night)
        self.statistics_names.append("mean time in the burrow in different months (percentage from night time)")

        self.statistics_data.append(spm_night)
        self.statistics_names.append("mean time in the shade in different months (percentage from night time)")

        """
        # too hot on tree for activity
        too_hot_for_tree_ph_a = np.array(self.lizard.too_hot_for_tree_per_hour)
        hours = np.array(self.climate.climate_data[p.hour,:])

        too_hot_for_tree_a = np.zeros((12,24), dtype= float)

        for month in range(1, 13):
            mask_m = (months == month)

            for hour in range(0,24):
                mask_h = (hours == hour)
                mask = np.logical_and(mask_m, mask_h)

                too_hot_for_tree_a[month - 1 , hour - 1] = np.mean(too_hot_for_tree_ph_a[mask])

        i = 1
        for month_row in too_hot_for_tree_a:
            self.statistics_data.append(list(month_row))
            self.statistics_names.append("mean minutes (over 20 years) in which the tree was too hot for activity (per month): " + str(i))
            i += 1

        # too cold on tree for activity
        too_cold_for_tree_ph_a = np.array(self.lizard.too_cold_for_tree_per_hour)

        too_cold_for_tree_a = np.zeros((12, 24), dtype=float)

        for month in range(1, 13):
            mask_m = (months == month)

            for hour in range(0, 24):
                mask_h = (hours == hour)
                mask = np.logical_and(mask_m, mask_h)
                too_cold_for_tree_a[month - 1, hour - 1] = np.mean(too_cold_for_tree_ph_a[mask])

        i = 1
        for month_row in too_cold_for_tree_a:
            self.statistics_data.append(list(month_row))
            self.statistics_names.append("mean minutes (over 20 years) in which the tree was too cold for activity (per month): " + str(i))
            i += 1
        """

        # activity
        activity_pd = self.lizard.activity_per_day

        # days with activity
        self.statistics_data.append(sum(activity_pd) / 20)
        #print(sum(activity_pd) / 20)
        self.statistics_names.append("mean days with activity per year")

        # days without activity
        without_activity_a = np.array(activity_pd) == False
        self.statistics_data.append(sum(without_activity_a) / 20)
        self.statistics_names.append("mean days without activity per year")


        # first julian day of activity
        activity_pd_a = np.array(activity_pd)
        activity_pd_a = np.reshape(activity_pd_a, (20, 365))
        
        #out_a = open("activity_pd_a", 'w')
        #i = 0
        #for row in activity_pd_a:
        #    for column in row:
        #        out_a.write(str(column) + ',')
        #    out_a.write('\n')
        #    i += 1
        #out_a.close()

        first_activity_days = []
        last_activity_days = []

        years_with_no_activity = []
        j = 1
        for year in activity_pd_a:
            if np.any(year) == False:
                print("year " + str(j) + " has no activity")
                years_with_no_activity.append(j)

            else:
                indices = np.nonzero(year)

                first_activity_days.append(indices[0][0] + 1)
                last_activity_days.append(indices[0][-1] + 1)

            j += 1

        self.statistics_data.append(sum(first_activity_days) / (20 - len(years_with_no_activity)))
        self.statistics_data.append(sum(last_activity_days) / (20 - len(years_with_no_activity)))

        self.statistics_names.append("mean first day of activity")
        self.statistics_names.append("mean last day of activity")


        activity_pd_a = np.array(activity_pd)
        activity_pd_a = np.reshape(activity_pd_a, (20, 365))

        years_with_no_activity = []
        j = 1
        for year in activity_pd_a:
            if np.any(year) == False:
                print("year " + str(j) + " has no activity")
                years_with_no_activity.append(j)
            j += 1

        self.statistics_data.append(years_with_no_activity)
        self.statistics_names.append("years with no activity:")

        """
        curr_i = 0
        count = 1
        gaps = {}

        for i in range(1, len(activity_pd)):
            if activity_pd[i] == False:
                if activity_pd[i - 1] == False:
                    count += 1
                else:
                    curr_i = i
                    count = 1
            else:
                if activity_pd[i - 1] == False:
                    gaps[curr_i] = count
                    curr_i = -1
                    count = -1

        years_with_activity = 20 - len(years_with_no_activity)

        sorted_keys_by_values = sorted(gaps, key=gaps.get, reverse=True)
        sorted_keys_by_keys = sorted(sorted_keys_by_values[0 : years_with_activity])

        activity_season_lengths = []

        for i in range(1, len(sorted_keys_by_keys)):
            first_day = sorted_keys_by_keys[i - 1] + gaps[sorted_keys_by_keys[i - 1]]
            last_day = sorted_keys_by_keys[i] - 1
            length = last_day - first_day

            activity_season_lengths.append(length)

        self.statistics_data.append(sum(activity_season_lengths) / (years_with_activity - 1))
        self.statistics_names.append("mean length of activity season")
        """
        burrow_ph_a = np.array(self.lizard.burrow_per_hour)
        sph_a = np.array(self.lizard.open_per_hour)
        oph_a = np.array(self.lizard.shade_per_hour)
        if isinstance(self.lizard, Lizard_climbing):
            tph_open_a = np.array(self.lizard.open_tree_per_hour)
            tph_shade_a = np.array(self.lizard.shaded_tree_per_hour)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)

            # micro-environments per hour in winter
            winter = np.logical_or(np.logical_or(months == 12, months == 1), months == 2)
            winter_daylight = mask_daylight[winter]
            winter_daylight_mat = np.reshape(winter_daylight, (-1, 24))

            # shade per hour in the winter
            winter_shade_a = sph_a[winter]
            winter_shade_a = np.reshape(winter_shade_a, (-1, 24))
            winter_shade_a = np.where(winter_daylight_mat, winter_shade_a, np.NaN)
            winter_shade_ph_a = np.nanmean(winter_shade_a, axis=0)
            winter_shade_ph_a[np.isnan(winter_shade_ph_a)] = 0

            self.statistics_data.append(list(winter_shade_ph_a))
            self.statistics_names.append("mean shade minutes per hour in the winter (Dec-Jan-Feb)")

            # open per hour in the winter
            winter_open_a = oph_a[winter]
            winter_open_a = np.reshape(winter_open_a, (-1, 24))
            winter_open_a = np.where(winter_daylight_mat, winter_open_a, np.NaN)
            winter_open_ph_a = np.nanmean(winter_open_a, axis=0)
            winter_open_ph_a[np.isnan(winter_open_ph_a)] = 0

            self.statistics_data.append(list(winter_open_ph_a))
            self.statistics_names.append("mean open minutes per hour in the winter (Dec-Jan-Feb)")

            # burrow per hour in the winter
            winter_burrow_a = burrow_ph_a[winter]
            winter_burrow_a = np.reshape(winter_burrow_a, (-1, 24))
            winter_burrow_a = np.where(winter_daylight_mat, winter_burrow_a, np.NaN)
            winter_burrow_ph_a = np.nanmean(winter_burrow_a, axis=0)
            winter_burrow_ph_a[np.isnan(winter_burrow_ph_a)] = 0

            self.statistics_data.append(list(winter_burrow_ph_a))
            self.statistics_names.append("mean burrow minutes per hour in the winter (Dec-Jan-Feb)")

            if isinstance(self.lizard, Lizard_climbing):
                # open tree per hour in the winter
                winter_tree_open_a = tph_open_a[winter]
                winter_tree_open_a = np.reshape(winter_tree_open_a, (-1, 24))
                winter_tree_open_a = np.where(winter_daylight_mat, winter_tree_open_a, np.NaN)
                winter_tree_open_ph_a = np.nanmean(winter_tree_open_a, axis=0)
                winter_tree_open_ph_a[np.isnan(winter_tree_open_ph_a)] = 0

                self.statistics_data.append(list(winter_tree_open_ph_a))
                self.statistics_names.append("mean open tree minutes per hour in the winter (Dec-Jan-Feb)")

                # shaded tree per hour in the winter
                winter_tree_shade_a = tph_shade_a[winter]
                winter_tree_shade_a = np.reshape(winter_tree_shade_a, (-1, 24))
                winter_tree_shade_a = np.where(winter_daylight_mat, winter_tree_shade_a, np.NaN)
                winter_tree_shade_ph_a = np.nanmean(winter_tree_shade_a, axis=0)
                winter_tree_shade_ph_a[np.isnan(winter_tree_shade_ph_a)] = 0

                self.statistics_data.append(list(winter_tree_shade_ph_a))
                self.statistics_names.append("mean shaded tree minutes per hour in the winter (Dec-Jan-Feb)")

            # micro-environments per hour in summer
            summer = np.logical_or(np.logical_or(months == 6, months == 7), months == 8)
            summer_daylight = mask_daylight[summer]
            summer_daylight_mat = np.reshape(summer_daylight, (-1, 24))

            # shade per hour in the summer
            summer_shade_a = sph_a[summer]
            summer_shade_a = np.reshape(summer_shade_a, (-1, 24))
            summer_shade_a = np.where(summer_daylight_mat, summer_shade_a, np.NaN)
            summer_shade_ph_a = np.nanmean(summer_shade_a, axis=0)
            summer_shade_ph_a[np.isnan(summer_shade_ph_a)] = 0

            self.statistics_data.append(list(summer_shade_ph_a))
            self.statistics_names.append("mean shade minutes per hour in the summer (Jun-Jul-Aug)")

            # open per hour in the summer
            summer_open_a = oph_a[summer]
            summer_open_a = np.reshape(summer_open_a, (-1, 24))
            summer_open_a = np.where(summer_daylight_mat, summer_open_a, np.NaN)
            summer_open_ph_a = np.nanmean(summer_open_a, axis=0)
            summer_open_ph_a[np.isnan(summer_open_ph_a)] = 0

            self.statistics_data.append(list(summer_open_ph_a))
            self.statistics_names.append("mean open minutes per hour in the summer (Jun-Jul-Aug)")

            # burrow per hour in the summer
            summer_burrow_a = burrow_ph_a[summer]
            summer_burrow_a = np.reshape(summer_burrow_a, (-1, 24))
            summer_burrow_a = np.where(summer_daylight_mat, summer_burrow_a, np.NaN)
            summer_burrow_ph_a = np.nanmean(summer_burrow_a, axis=0)
            summer_burrow_ph_a[np.isnan(summer_burrow_ph_a)] = 0

            self.statistics_data.append(list(summer_burrow_ph_a))
            self.statistics_names.append("mean burrow minutes per hour in the summer (Jun-Jul-Aug)")

            if isinstance(self.lizard, Lizard_climbing):
                # open tree per hour in the summer
                summer_tree_open_a = tph_open_a[summer]
                summer_tree_open_a = np.reshape(summer_tree_open_a, (-1, 24))
                summer_tree_open_a = np.where(summer_daylight_mat, summer_tree_open_a, np.NaN)
                summer_tree_open_ph_a = np.nanmean(summer_tree_open_a, axis=0)
                summer_tree_open_ph_a[np.isnan(summer_tree_open_ph_a)] = 0

                self.statistics_data.append(list(summer_tree_open_ph_a))
                self.statistics_names.append("mean open tree minutes per hour in the summer (Jun-Jul-Aug)")

                # shaded tree per hour in the summer
                summer_tree_shade_a = tph_shade_a[summer]
                summer_tree_shade_a = np.reshape(summer_tree_shade_a, (-1, 24))
                summer_tree_shade_a = np.where(summer_daylight_mat, summer_tree_shade_a, np.NaN)
                summer_tree_shade_ph_a = np.nanmean(summer_tree_shade_a, axis=0)
                summer_tree_shade_ph_a[np.isnan(summer_tree_shade_ph_a)] = 0

                self.statistics_data.append(list(summer_tree_shade_ph_a))
                self.statistics_names.append("mean shaded tree minutes per hour in the summer (Jun-Jul-Aug)")

                dict = {}
                for height in self.lizard.climbing_heights_when_essential:
                    if str(height) in dict:
                        dict[str(height)] += 1
                    else:
                        dict[str(height)] = 1

                self.statistics_data.append(self.lizard.heights)
                self.statistics_names.append("possible heights:")

                frequencies = []

                for height in self.lizard.heights:
                    if str(height) not in dict:
                        dict[str(height)] = 0

                    frequencies.append(dict[str(height)])

                self.statistics_data.append(frequencies)
                self.statistics_names.append(
                    "frequency of climbing to this height when climbing was essential (in dt units):")

        # print the statistics to an external csv file named 'statistics'
        file_name = ""
        if isinstance(self.lizard, Lizard_climbing):
            file_name = "climbing_"
        else:
            file_name = "not_climbing_"

        if self.lizard.emergence:
            file_name = file_name + "limited_emergence_"

        file_name = file_name + self.climate.inputfilename + "_statistics.csv"

        out = open(path + "/" + file_name, 'w')
        i = 0
        for row in self.statistics_data:
            out.write(self.statistics_names[i] + ',')
            i += 1
            if type(row) == list:
                for column in row:
                    out.write(str(np.round(column,3)) + ',')
                out.write('\n')
            else:
                out.write(str(np.round(row, 3)) + '\n')
        out.close()





















