from Lizard_climbing import Lizard_climbing
from Lizard_energy import Lizard_energy
from Climate import Climate

import numpy as np
import Parameters as p

class Day_summary:
    def __init__(self):
        self.day_stats_data = []
        self.day_stats_names = []

    def calculate_day_statistics(self, climate, lizard, wanted_day, path, description = ""):

        heat_analysis = False

        num_of_heights = len(lizard.heights)

        daylight = []
        shade_lying = []
        shade_standing = []
        open_lying = []
        open_standing = []
        tree_shade_lying = np.empty((num_of_heights,24))
        tree_shade_standing = np.empty((num_of_heights,24))
        tree_open_lying = np.empty((num_of_heights,24))
        tree_open_standing = np.empty((num_of_heights,24))
        burrow = []
        chosen_temperature = []
        chosen_micro_environment = []
        time_in_burrow = []
        time_in_shade = []
        time_in_open = []
        time_on_shaded_tree = []
        time_on_open_tree = []
        active = []
        active_open = []
        active_shade = []
        active_open_tree = []
        active_shaded_tree = []
        foraging = []
        energy_lost = []
        DE = []
        J_gut = []
        cmax = []
        energy_gain = 0

        for i in range(24):
            lizard.mini_step(climate.current_climate, climate.time_step, i, heat_analysis)
            print(climate.time_step)

            # is daylight? (row 1)
            daylight.append(climate.current_climate[p.SWDOWN] > 1)

            # body temperature in shade - lying (row 2)
            shade_lying.append(lizard.temp_shade_lying)

            if climate.current_climate[p.SWDOWN] < 1:
                shade_standing.append(np.NaN)
                open_lying.append(np.NaN)
                open_standing.append(np.NaN)

                for j in range(num_of_heights):
                    tree_shade_lying[j, i] = np.NaN
                    tree_shade_standing[j, i] = np.NaN
                    tree_open_lying[j, i] = np.NaN
                    tree_open_standing[j, i] = np.NaN

            else:
                # body temperature in shade - standing (row 3)
                shade_standing.append(lizard.temp_shade_standing)

                # body temperature in open - lying (row 4)
                open_lying.append(lizard.temp_open_lying)

                # body temperature in open - standing (row 5)
                open_standing.append(lizard.temp_open_standing)

                # body temperature in shaded tree, at all heights - lying (rows 6-24)
                for j in range(num_of_heights):
                    tree_shade_lying[j, i] = lizard.TeT[0, j, 0]

                # body temperature in shaded tree, at all heights - standing (rows 25-43)
                for j in range(num_of_heights):
                    tree_shade_standing[j, i] = lizard.TeT[0, j, 1]

                # body temperature in open tree, at all heights - lying (rows 44-62)
                for j in range(num_of_heights):
                    tree_open_lying[j, i] = lizard.TeT[1, j, 0]

                # body temperature in open tree, at all heights - standing (rows 63-81)
                for j in range(num_of_heights):
                    tree_open_standing[j, i] = lizard.TeT[1, j, 1]

            # body temperature in burrow (row 82)
            burrow.append(climate.current_climate[p.Tsoil100_12cm] - p.zero_K)

            # final body temperature in chosen micro-environment (row 83)
            chosen_temperature.append(lizard.To)

            # last micro-environment in the current hour (row 84)
            chosen_micro_environment.append(lizard.last_micro_environment)

            # time in burrow during the last hour (row 85)
            if daylight[-1]:
                time_in_burrow.append(lizard.burrow_per_hour[-1])
            else:
                time_in_burrow.append(lizard.burrow_per_hour_night[-1])

            # time in shade during the last hour (row 86)
            if daylight[-1]:
                time_in_shade.append(lizard.shade_per_hour[-1])
            else:
                time_in_shade.append(lizard.shade_per_hour_night[-1])

            # time in the open during the last hour (row 87)
            time_in_open.append(lizard.open_per_hour[-1])

            # time on a shaded tree during the last hour (row 88)
            time_on_shaded_tree.append(lizard.shaded_tree_per_hour[-1])

            # time on an open tree during the last hour (row 89)
            time_on_open_tree.append(lizard.open_tree_per_hour[-1])

            # minutes of activity in the last hour (row 90)
            active.append(lizard.active_per_hour[-1])

            # minutes of activity in the open in the last hour (row 91)
            active_open.append(lizard.active_in_open_per_hour[-1])

            # minutes of activity in the shade in the last hour (row 92)
            active_shade.append(lizard.active_in_shade_per_hour[-1])

            # minutes of activity on an open tree in the last hour (row 93)
            active_open_tree.append(lizard.active_on_open_tree_per_hour[-1])

            # minutes of activity on a shaded tree in the last hour (row 94)
            active_shaded_tree.append(lizard.active_on_shaded_tree_per_hour[-1])

            # is foraging? (row 95)
            foraging.append(lizard.is_foraging)

            # energy lost in the current hour (row 96)
            if (lizard.is_foraging):
                e_lost = lizard.ep
            else:
                e_lost = lizard.ew

            energy_lost.append(e_lost)

            # digestion efficiency (row 97)
            DE.append(lizard.DE)

            # energy restored in the gut (row 98)
            J_gut.append(lizard.J_gut)

            # cmax of the current hour (row 99)
            cmax.append(lizard.cmax)

            climate.step()

        # energy gained over the current day (row 100)
        energy_gain = lizard.energy_gain_per_day[-1]

        # energy balance for today (row 101)
        energy_balance = energy_gain - sum(energy_lost)

        self.day_stats_data.append(daylight)
        self.day_stats_names.append("daylight?")

        self.day_stats_data.append(shade_lying)
        self.day_stats_names.append("temp in shade while lying")

        self.day_stats_data.append(shade_standing)
        self.day_stats_names.append("temp in shade while standing")

        self.day_stats_data.append(open_lying)
        self.day_stats_names.append("temp in open while lying")

        self.day_stats_data.append(open_standing)
        self.day_stats_names.append("temp in open while standing")

        for k in range(num_of_heights):
            self.day_stats_data.append(list(tree_shade_lying[k,:]))
            self.day_stats_names.append("temp on shaded tree while lying at the height of: " + str(lizard.heights[k]) + " cm")

        for k in range(num_of_heights):
            self.day_stats_data.append(list(tree_shade_standing[k,:]))
            self.day_stats_names.append("temp on shaded tree while standing at the height of: " + str(lizard.heights[k]) + " cm")

        for k in range(num_of_heights):
            self.day_stats_data.append(list(tree_open_lying[k, :]))
            self.day_stats_names.append("temp on open tree while lying at the height of: " + str(lizard.heights[k]) + " cm")

        for k in range(num_of_heights):
            self.day_stats_data.append(list(tree_open_standing[k, :]))
            self.day_stats_names.append("temp on open tree while standing at the height of: " + str(lizard.heights[k]) + " cm")

        self.day_stats_data.append(burrow)
        self.day_stats_names.append("temp in the burrow")

        self.day_stats_data.append(chosen_temperature)
        self.day_stats_names.append("temp in chosen micro-environment")

        self.day_stats_data.append(chosen_micro_environment)
        self.day_stats_names.append("last micro-environment in the current hour")

        self.day_stats_data.append(time_in_burrow)
        self.day_stats_names.append("time in the burrow in the current hour")

        self.day_stats_data.append(time_in_shade)
        self.day_stats_names.append("time in the shade in the current hour")

        self.day_stats_data.append(time_in_open)
        self.day_stats_names.append("time in the open in the current hour")

        self.day_stats_data.append(time_on_shaded_tree)
        self.day_stats_names.append("time on a shaded tree in the current hour")

        self.day_stats_data.append(time_on_open_tree)
        self.day_stats_names.append("time on an open tree in the current hour")

        self.day_stats_data.append(active)
        self.day_stats_names.append("minutes active")

        self.day_stats_data.append(active_open)
        self.day_stats_names.append("minutes active in the open")

        self.day_stats_data.append(active_shade)
        self.day_stats_names.append("minutes active in the shade")

        self.day_stats_data.append(active_open_tree)
        self.day_stats_names.append("minutes active on an open tree")

        self.day_stats_data.append(active_shaded_tree)
        self.day_stats_names.append("minutes active on a shaded tree")

        self.day_stats_data.append(foraging)
        self.day_stats_names.append("is foraging?")

        self.day_stats_data.append(energy_lost)
        self.day_stats_names.append("energy_lost in the current hour")

        self.day_stats_data.append(DE)
        self.day_stats_names.append("digesting efficiency")

        self.day_stats_data.append(J_gut)
        self.day_stats_names.append("energy stored in the gut")

        self.day_stats_data.append(cmax)
        self.day_stats_names.append("maximum energy that can be stored in the gut")

        self.day_stats_data.append(energy_gain)
        self.day_stats_names.append("energy gained today")

        self.day_stats_data.append(energy_balance)
        self.day_stats_names.append("energy balance for today")

        if wanted_day != "":
            date_str = str(int(wanted_day[0])) + "." + str(int(wanted_day[1])) + "." + str(int(wanted_day[2]))
            self.day_stats_data.append(date_str)
            self.day_stats_names.append("day:")

        if lizard.emergence:
            emergence = "limited_emergence_"
        else:
            emergence = ""

        file_name = "climbing_" + emergence + climate.inputfilename + "_" + description + "_day_statistics.csv"

        out = open(path + "/" + file_name, 'w')
        i = 0
        for row in self.day_stats_data:
            out.write(self.day_stats_names[i] + ',')
            i += 1
            if type(row) == list:
                for column in row:
                    out.write(str(column) + ',')
                out.write('\n')
            else:
                out.write(str(row) + '\n')
        out.close()

        
        # heat parameters

        if heat_analysis:
        
            hours = range(24)
            heights = lizard.heights
            postures = ["lying", "standing"]
            shades = ["shade", "open"]
            parameters_lst = ["dQe", "solar", "IR", "meta", "cond", "conv"]

            heat_table = [] 

            for i_hour in range(len(hours)):
                for i_posture in range(len(postures)):
                    for i_shade in range(len(shades)):

                        ground_row_pars = list(lizard.heat_par_ground[i_hour, i_posture, i_shade, :])
                        ground_row = [hours[i_hour], postures[i_posture], None, shades[i_shade]] + ground_row_pars

                        heat_table.append(ground_row)

                        for i_height in range(len(heights)):

                            tree_row_pars = list(lizard.heat_par_tree[i_hour, i_posture, i_height, i_shade, :])
                            tree_row = [hours[i_hour], postures[i_posture], heights[i_height], shades[i_shade]] + tree_row_pars

                            heat_table.append(tree_row)        

            file_name_heat = "climbing_" + emergence + climate.inputfilename + "_" + description + "_heat_pars.csv"
            out_heat = open(path + "/" + file_name_heat, 'w')

            headers = ["hour", "posture", "height", "shade_level"] + parameters_lst


            for cell in headers:
                out_heat.write(str(cell) + ',')
            
            for row in heat_table:
                out_heat.write('\n')
                for cell in row:
                    out_heat.write(str(cell) + ',')
                
            out_heat.close()

            



















































