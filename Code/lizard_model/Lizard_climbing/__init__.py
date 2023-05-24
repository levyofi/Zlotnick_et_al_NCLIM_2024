from Lizard_energy import Lizard_energy
import numpy as np
import Parameters as p

class Lizard_climbing(Lizard_energy):

    def __init__(self, limited_emergence = True):
        Lizard_energy.__init__(self, limited_emergence)

        self.min_TeT = None
        self.max_TeT = None
        self.best_tree_open_To = None
        self.best_tree_shade_To = None
        # self.preferred_tree_height = -1.0

        self.tree_insect_abundance = 0.005

        # information for statistics
        self.open_tree_per_hour = [0]	    #
        self.shaded_tree_per_hour = [0]	    #
        self.essential_climbing_per_hour = [0]	    #
        self.climbing_to_warm_per_hour = [0]	    #
        self.climbing_to_cool_per_hour = [0]	    #
        self.climbing_mixed = [0]
        self.essential_climbing_on_open_tree = [0]
        self.essential_climbing_on_shaded_tree = [0]	       #
        #self.too_hot_for_tree_per_hour = [0]
        #self.too_cold_for_tree_per_hour = [0]

        self.active_on_open_tree_per_hour = [0]
        self.active_on_shaded_tree_per_hour = [0]

        self.climbing_heights_when_essential = []	    #
        self.climbing_heights_when_essential_open_tree = []
        self.climbing_heights_when_essential_shaded_tree = []
        self.heights = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 48, 66, 84, 102, 120, 138, 156, 174, 198]
        self.heights_indexes = range(len(self.heights))

        self.tree_open_part_from_daytime_per_day = []	#
        self.tree_shade_part_from_daytime_per_day = []	#
        self.tree_to_warm_part_from_daytime_per_day = []	#
        self.tree_to_cool_part_from_daytime_per_day = []	#
        self.tree_mixed_part_from_daytime_per_day = []	#
        self.tree_ess_part_from_daytime_per_day = []	#

        self.active_tree_open_part_from_daytime_per_day = []
        self.active_tree_shade_part_from_daytime_per_day = []

        # for day analysis
        self.temp_open_lying = 0
        self.temp_shade_lying = 0
        self.temp_open_standing = 0
        self.temp_shade_standing = 0

        self.TeT = np.empty((2,len(self.heights),2))
        self.TeT.fill(np.NaN)

        self.heat_par_ground = np.empty((24, 2, 2, 6))
        self.heat_par_tree = np.empty((24,2,len(self.heights),2,6))

        self.chosen_microenvironment = ""

    def calculate_tb(self,current_climate):
        
        if (self.mass > 20):
            dt = 180
        elif (self.mass > 10):
            dt = 120
        else:
            dt = 60

        temp_time_steps_num = 3600 // dt

        #print(current_climate[p.SWDOWN] > 1)

        # set the number of possible postures - if night (i.e., not active) then only lying is possible
        if (current_climate[p.SWDOWN] < 1):     # night
            #print("night")
            self.active_per_hour.append(0)
            self.active_in_open_per_hour.append(0)
            self.active_in_shade_per_hour.append(0)
            self.active_on_open_tree_per_hour.append(0)
            self.active_on_shaded_tree_per_hour.append(0)

            # if it's too cold or the lizard has already been in burrow - burrow
            if (current_climate[p.Ta100_3cm] < p.zero_K) or (self.last_micro_environment == "burrow"):
                #print("too cold")
                self.To = current_climate[p.Tsoil100_12cm] - p.zero_K
                self.last_micro_environment = "burrow"

                self.open_per_hour.append(0)
                self.shade_per_hour.append(0)
                self.open_tree_per_hour.append(0)
                self.shaded_tree_per_hour.append(0)
                self.burrow_per_hour.append(0)

                self.shade_per_hour_night.append(0)
                self.burrow_per_hour_night.append(60)

                self.essential_climbing_per_hour.append(0)
                self.climbing_to_cool_per_hour.append(0)
                self.climbing_to_warm_per_hour.append(0)
                self.climbing_mixed.append(0)
                self.essential_climbing_on_open_tree.append(0)
                self.essential_climbing_on_shaded_tree.append(0)

                if current_climate[p.Ta100_3cm] < p.zero_K:
                    self.too_cold_outside = True

                return

            # not too cold & lizard wasn't in the burrow
            else:
                #print("not too cold")
                self.h_l_mat = np.empty((2, len(self.heights)))
                self.h_l_mat[0,0] = self.calculate_h_L(current_climate[p.Ta100_3cm], current_climate[p.WV_3cm], current_climate[p.Air_density])

                for i in range(temp_time_steps_num):
                    self.calculate_tb_dt(dt, current_climate, i, night_outside = True)

                    self.To = self.max_TeS
                    self.last_micro_environment = "shade"

                self.open_per_hour.append(0)
                self.shade_per_hour.append(0)
                self.open_tree_per_hour.append(0)
                self.shaded_tree_per_hour.append(0)
                self.burrow_per_hour.append(0)

                self.shade_per_hour_night.append(60)
                self.burrow_per_hour_night.append(0)

                self.essential_climbing_per_hour.append(0)
                self.climbing_to_cool_per_hour.append(0)
                self.climbing_to_warm_per_hour.append(0)
                self.climbing_mixed.append(0)
                self.essential_climbing_on_open_tree.append(0)
                self.essential_climbing_on_shaded_tree.append(0)

                return

        else:       # day
            #print("day")
            current_num_of_postures = 2
            current_num_of_shade_levels = 2

            time_in_the_open = 0
            time_in_the_shade = 0
            time_on_an_open_tree = 0
            time_on_a_shaded_tree = 0
            time_in_the_burrow = 0

            time_active = 0
            time_active_in_open = 0
            time_active_in_shade = 0
            time_active_on_open_tree = 0
            time_active_on_shaded_tree = 0

            essential_time_on_a_tree = 0
            tree_to_get_warm = 0
            tree_to_get_cool = 0
            tree_mixed = 0
            essential_climbing_on_open_tree = 0
            essential_climbing_on_shaded_tree = 0

            best_open_To = 0.0
            best_shade_To = 0.0

            self.h_l_mat = np.empty((2,len(self.heights)))
            for i_shade in range(current_num_of_shade_levels):
                for i_height in range(len(self.heights)):
                    Tair = current_climate[p.Ta100_3cm + (-1 * i_shade * 19) + self.heights_indexes[i_height]]
                    wind_vel = current_climate[p.WV_3cm + self.heights_indexes[i_height]]

                    self.h_l_mat[i_shade,i_height] = self.calculate_h_L(Tair, wind_vel,current_climate[p.Air_density])
            #if (current_climate[p.day] == 1) and (current_climate[p.month] == 6) and (current_climate[p.year] == 1990):
                #print(current_climate[p.hour])
                #print("SWDOWN")
                #print(current_climate[p.SWDOWN])
                #print("solar_trunk_beam")
                #print(current_climate[p.solar_trunk_beam])
                #print("solar_trunk_diffuse")
                #print(current_climate[p.solar_trunk_diffuse])
                #if current_climate[p.hour] == 20:
                    #print(current_climate[p.SWDOWN])
                    #print("convection coefficient (shade)")
                    #print(self.h_l_mat[0])
                    #print("air temp (shade)")
                    #print(current_climate[p.Ta100_3cm:p.Ta100_198cm+1])
                    #print("wind velocity")
                    #print(current_climate[p.WV_3cm:p.WV_198cm+1])
                    #print("trunk temp (shade)")
                    #print(current_climate[p.Ttrunk100_3cm:p.Ttrunk100_198cm+1])

            for i in range(temp_time_steps_num):

                self.calculate_tb_dt(dt, current_climate, i)

                # choose best temperature in the shade
                if (abs(self.max_TeS - self.Vtmean) < abs(self.min_TeS - self.Vtmean)):
                    best_shade_To = self.max_TeS
                else:
                    best_shade_To = self.min_TeS

                # choose best temperature in the open
                if (abs(self.max_Te - self.Vtmean) < abs(self.min_Te - self.Vtmean)):
                    best_open_To = self.max_Te
                else:
                    best_open_To = self.min_Te

                """
                # check when activity is not possible while climbing
                if (self.best_tree_open_To > self.Vtmax) and (self.best_tree_shade_To > self.Vtmax):
                    too_hot_for_tree = too_hot_for_tree + (dt / 60)
                elif (self.best_tree_open_To < self.Vtmin) and (self.best_tree_shade_To < self.Vtmin):
                    too_cold_for_tree = too_cold_for_tree + (dt / 60)
                """
                #print("limited emergence check")
                # limited emergence
                can_emerge = self.check_emergence()

                if not can_emerge:      # cannot emerge
                    self.To = current_climate[p.Tsoil100_12cm] - p.zero_K
                    time_in_the_burrow = time_in_the_burrow + (dt/60)
                    self.last_micro_environment = "burrow"

                else:       # can emerge

                    open_abs = abs(best_open_To - self.Vtmean)
                    shade_abs = abs(best_shade_To - self.Vtmean)
                    tree_open_abs = abs(self.best_tree_open_To - self.Vtmean)
                    tree_shade_abs = abs(self.best_tree_shade_To - self.Vtmean)

                    temp_in_range = False

                    # choose the best habitat (is it open?)
                    if open_abs == min(open_abs, shade_abs, tree_open_abs, tree_shade_abs):
                        if (best_open_To < self.emergence_max_To) and (best_open_To > self.emergence_min_To):
                            temp_in_range = True
                            self.To = best_open_To
                            self.is_climbing = False
                            time_in_the_open = time_in_the_open + (dt / 60)
                            self.last_micro_environment = "open"

                    # choose the best habitat (is it shade?)
                    elif shade_abs == min(open_abs, shade_abs, tree_open_abs, tree_shade_abs):
                        if (best_shade_To < self.emergence_max_To) and (best_shade_To > self.emergence_min_To):
                            temp_in_range = True
                            self.To = best_shade_To
                            self.is_climbing = False
                            time_in_the_shade = time_in_the_shade + (dt / 60)
                            self.last_micro_environment = "shade"

                    elif tree_open_abs == min(open_abs, shade_abs, tree_open_abs, tree_shade_abs):
                        if (self.best_tree_open_To < self.emergence_max_To) and (self.best_tree_open_To > self.emergence_min_To):
                            temp_in_range = True
                            self.To = self.best_tree_open_To
                            self.is_climbing = True
                            time_on_an_open_tree = time_on_an_open_tree + (dt / 60)
                            self.last_micro_environment = "open tree"
                            height = self.heights[self.best_temp_prop_open[1]]

                    elif tree_shade_abs == min(open_abs, shade_abs, tree_open_abs, tree_shade_abs):
                        if (self.best_tree_shade_To < self.emergence_max_To) and (self.best_tree_shade_To > self.emergence_min_To):
                            temp_in_range = True
                            self.To = self.best_tree_shade_To
                            self.is_climbing = True
                            time_on_a_shaded_tree = time_on_a_shaded_tree + (dt / 60)
                            self.last_micro_environment = "shaded tree"
                            height = self.heights[self.best_temp_prop_shade[1]]


                    if not temp_in_range:
                        self.To = current_climate[p.Tsoil100_12cm] - p.zero_K
                        time_in_the_burrow = time_in_the_burrow + (dt / 60)
                        self.last_micro_environment = "burrow"

                        if best_shade_To > self.emergence_max_To:
                            self.too_hot_outside = True
                        elif best_open_To < self.emergence_min_To:
                            self.too_cold_outside = True

                    else:
                        # is active?
                        if (self.To > self.Vtmin) and (self.To < self.Vtmax):
                            is_active = True
                        else:
                            is_active = False

                        if self.is_climbing and is_active:
                            # check if climbing is essential for activity
                            if ((best_open_To < self.Vtmin) or (best_open_To > self.Vtmax)) and ((best_shade_To < self.Vtmin) or (best_shade_To > self.Vtmax)):
                                essential_time_on_a_tree = essential_time_on_a_tree + (dt / 60)

                                if ((best_open_To < self.Vtmin) and (best_shade_To < self.Vtmin)):
                                    tree_to_get_warm = tree_to_get_warm + (dt / 60)
                                elif ((best_open_To > self.Vtmax) and (best_shade_To > self.Vtmax)):
                                    tree_to_get_cool = tree_to_get_cool + (dt / 60)
                                else:
                                    tree_mixed = tree_mixed + (dt / 60)

                                self.climbing_heights_when_essential.append(height)

                                if self.last_micro_environment == "open tree":
                                    essential_climbing_on_open_tree = essential_climbing_on_open_tree + (dt / 60)
                                    self.climbing_heights_when_essential_open_tree.append(height)

                                elif self.last_micro_environment == "shaded tree":
                                    essential_climbing_on_shaded_tree = essential_climbing_on_shaded_tree + (dt / 60)
                                    self.climbing_heights_when_essential_shaded_tree.append(height)

                        # perfect thermoregulation
                        if (self.Vtmean < max(best_open_To, best_shade_To, self.best_tree_open_To, self.best_tree_shade_To)) and (self.Vtmean > min(best_open_To, best_shade_To, self.best_tree_open_To,self.best_tree_shade_To)):
                            self.To = self.Vtmean

                        if is_active:
                            time_active = time_active + (dt/60)

                            if self.last_micro_environment == "open":
                                time_active_in_open = time_active_in_open + (dt/60)
                            elif self.last_micro_environment == "shade":
                                time_active_in_shade = time_active_in_shade + (dt/60)
                            elif self.last_micro_environment == "open tree":
                                time_active_on_open_tree = time_active_on_open_tree + (dt/60)
                            elif self.last_micro_environment == "shaded tree":
                                time_active_on_shaded_tree = time_active_on_shaded_tree + (dt/60)

            #print("day arrays")
            self.open_per_hour.append(time_in_the_open)
            self.shade_per_hour.append(time_in_the_shade)
            self.open_tree_per_hour.append(time_on_an_open_tree)
            self.shaded_tree_per_hour.append(time_on_a_shaded_tree)
            self.burrow_per_hour.append(time_in_the_burrow)

            self.shade_per_hour_night.append(0)
            self.burrow_per_hour_night.append(0)

            self.active_per_hour.append(time_active)
            self.active_in_open_per_hour.append(time_active_in_open)
            self.active_in_shade_per_hour.append(time_active_in_shade)
            self.active_on_open_tree_per_hour.append(time_active_on_open_tree)
            self.active_on_shaded_tree_per_hour.append(time_active_on_shaded_tree)

            self.essential_climbing_per_hour.append(essential_time_on_a_tree)
            self.climbing_to_cool_per_hour.append(tree_to_get_cool)
            self.climbing_to_warm_per_hour.append(tree_to_get_warm)
            self.climbing_mixed.append(tree_mixed)

            self.essential_climbing_on_open_tree.append(essential_climbing_on_open_tree)
            self.essential_climbing_on_shaded_tree.append(essential_climbing_on_shaded_tree)

            #self.too_hot_for_tree_per_hour.append(too_hot_for_tree)
            #self.too_cold_for_tree_per_hour.append(too_cold_for_tree)

            #print(self.active_per_hour[-1])

    def calculate_tb_dt(self, dt, current_climate, i, night_outside = False):

        # thermal absorptivity, Bartlett & Gates 1967
        alpha_L_direct = self.alpha_L_direct
        alpha_L_scattered = self.alpha_L_scattered

        # convective heat transfer coefficient (W m-2 K-1) (Fei et al. 2012, J Ther Biol, 37: 56-64, Porter et al. 1973)
        # h_L = 10.45

        # emissivity of lizard's skin
        epsilon_lizard = 0.95

        # thermal conductivity (W K-1 m-1)
        K_lizard = 0.5

        # lizard mean thickness in meters (diameter)
        lambda_lizard = 0.02

        # specific heat capacity (J kg-1)
        c_lizard = 3762

        Mb_total = (self.mass) / 1000  # in kg

        A_L = 0.00758  # 0.0314 * 3.14159 * (Mb_total ** (2 / 3))  # surface area (in m2)
        To = self.To + p.zero_K  # current body temperature in kelvin

        # solar radiation
        # projected lizard area for direct and scattered solar radiation
        A_p = 0.4 * A_L

        # Surface area that can absorb longwave radiation from above
        A_up = 0.6 * A_L

        diff = current_climate[p.diffuse_ratio]

        # posture related data
        if night_outside:
            current_num_of_postures = 1
        else:
            current_num_of_postures = 2

        current_num_of_shade_levels = current_num_of_postures

        lying = 0
        standing = 1

        A_downs = [0.0] * current_num_of_postures
        A_contacts = [0.0] * current_num_of_postures

        Te = [0.0] * current_num_of_postures
        TeS = [0.0] * current_num_of_postures
        TeT = np.empty((current_num_of_shade_levels,len(self.heights),current_num_of_postures))

        # set projected lizard area for radiation from the ground
        A_downs[lying] = 0.0 * A_L
        if not night_outside:
            A_downs[standing] = 0.4 * A_L

        # set projected lizard area that contacts the ground
        A_contacts[lying] = 0.35 * A_L
        if not night_outside:
            A_contacts[standing] = 0.05 * A_L

        # metabolism
        dQ_meta = self.ew / 3600  # metabolic rate (j/s)

        for i_posture in range(current_num_of_postures):

            A_contact = A_contacts[i_posture]  # area lizards contacts with the ground
            A_down = A_downs[i_posture]     # Surface area that can absorb longwave radiation from the ground
            Aee = 0.89 * (A_L - A_contact)
            Aair = A_L - A_contact  # 0.9 * A_L  # skin area that is exposed to air

            ####### temperature on the ground ######

            #### shade ####

            # solar radiation
            SdQ_solar = alpha_L_scattered * Aee * diff * current_climate[p.SWDOWN]

            # IR radiation
            SdQ_IR = (epsilon_lizard * p.sigma * A_down * current_climate[p.Tsurface100] ** 4) + (
                        epsilon_lizard * p.sigma * A_up * current_climate[p.TAH] ** 4) - (
                                 epsilon_lizard * p.sigma * Aair * To ** 4)

            # conduction
            SdQ_cond = (A_contact * K_lizard * (current_climate[p.Tsurface100] - To)) / (0.5 * lambda_lizard)

            # convection
            self.h_l_S = self.h_l_mat[0, 0]
            SdQ_conv = self.h_l_S * Aair * (current_climate[p.Ta100_3cm] - To)

            # energy balance calculation
            SdQe = SdQ_solar + SdQ_IR + dQ_meta + SdQ_cond + SdQ_conv
            SdTe = SdQe / (((self.mass) / 1000) * c_lizard)

            TeS[i_posture] = To + (SdTe * dt) - p.zero_K

            #if (current_climate[p.day] == 15) and (current_climate[p.month] == 9) and (current_climate[p.year] == 1981):
            #    if ((i + 1) == 3600 / dt):
            #        print("stop")

            if not night_outside:       # day
                #### open ####

                # solar radiation
                dQ_solar = alpha_L_direct * A_p * (
                            (1 - diff) * current_climate[p.SWDOWN]) + alpha_L_scattered * Aee * diff * current_climate[
                               p.SWDOWN]

                # IR radiation
                dQ_IR = (epsilon_lizard * p.sigma * A_down * current_climate[p.Tsurface] ** 4) + (
                            epsilon_lizard * A_up * current_climate[p.GLW]) - (
                                    epsilon_lizard * p.sigma * Aair * To ** 4)

                # conduction
                dQ_cond = (A_contact * K_lizard * (current_climate[p.Tsurface] - To)) / (0.5 * lambda_lizard)

                # convection
                self.h_l = self.h_l_mat[1,0]
                dQ_conv = self.h_l * Aair * (current_climate[p.Ta_3cm] - To)

                # energy balance calculation
                dQe = dQ_solar + dQ_IR + dQ_meta + dQ_cond + dQ_conv
                dTe = dQe / (((self.mass) / 1000) * c_lizard)

                Te[i_posture] = To + (dTe * dt) - p.zero_K

                #if (current_climate[p.day] == 15) and (current_climate[p.month] == 9) and (current_climate[p.year] == 1981):
                #    if ((i+1) == 3600 / dt) :
                #        print("stop")

                #######    end of temperature on the ground   ######

                #######    temperature on the a tree trunk   ######

                for j_shade_level in range(current_num_of_shade_levels):
                    for j_height in range(len(self.heights)):

                        trunk_temperature = current_climate[p.Ttrunk100_3cm + (-1 * j_shade_level * 19) + self.heights_indexes[j_height]]
                        air_temperature = current_climate[p.Ta100_3cm + (-1 * j_shade_level * 19) + self.heights_indexes[j_height]]
                        #wind_velocity = current_climate[p.WV_3cm + self.heights_indexes[j_height]]

                        # conduction
                        TdQ_cond = (A_contact * K_lizard * (trunk_temperature - To)) / (0.5 * lambda_lizard)

                        # convection
                        h_l_T = self.h_l_mat[j_shade_level, j_height]
                        TdQ_conv = h_l_T * Aair * (air_temperature - To)

                        if (j_shade_level == 0):        # in the shade
                            # solar radiation
                            TSdQ_solar = alpha_L_scattered * Aee * current_climate[p.solar_trunk_diffuse]

                            # IR radiation
                            TSdQ_IR = (epsilon_lizard * p.sigma * A_down * trunk_temperature ** 4) + (0.5 * epsilon_lizard * p.sigma * A_up * current_climate[p.TAH] ** 4) + (0.5 * epsilon_lizard * p.sigma * A_up * current_climate[p.Tsurface100] ** 4) - (epsilon_lizard * p.sigma * Aair * To ** 4)

                            TSdQe = TSdQ_solar + TSdQ_IR + dQ_meta + TdQ_cond + TdQ_conv
                            TSdTe = TSdQe / (((self.mass) / 1000) * c_lizard)

                            #if (current_climate[p.day] == 15) and (current_climate[p.month] == 9) and (
                            #        current_climate[p.year] == 1981):
                            #    if ((i + 1) == 3600 / dt):
                            #        if (j_height == 1) or (j_height == 12):
                            #            print("stop")

                            TeT[j_shade_level, j_height, i_posture] = To + (TSdTe * dt) - p.zero_K
                        
                        elif (j_shade_level == 1):        # in the open
                            # solar radiation
                            TdQ_solar = alpha_L_direct * A_p * current_climate[p.solar_trunk_beam] + alpha_L_scattered * Aee * current_climate[p.solar_trunk_diffuse]

                            # IR radiation
                            TdQ_IR = (epsilon_lizard * p.sigma * A_down * trunk_temperature ** 4) + (0.5 * epsilon_lizard * A_up * current_climate[p.GLW]) + (0.5 * epsilon_lizard * p.sigma * A_up * current_climate[p.Tsurface] ** 4) - (epsilon_lizard * p.sigma * Aair * To ** 4)

                            TdQe = TdQ_solar + TdQ_IR + dQ_meta + TdQ_cond + TdQ_conv
                            TdTe = TdQe / (((self.mass) / 1000) * c_lizard)

                            #if (current_climate[p.day] == 15) and (current_climate[p.month] == 9) and (
                            #        current_climate[p.year] == 1981):
                            #    if ((i + 1) == 3600 / dt):
                            #        if (j_height == 1) or (j_height == 12):
                            #            print("stop")

                            TeT[j_shade_level, j_height, i_posture] = To + (TdTe * dt) - p.zero_K

        # find the two extremes from all shade q open * lying / standing positions
        self.max_TeS = np.max(TeS)
        self.min_TeS = np.min(TeS)

        if not night_outside:
            self.max_Te = np.max(Te)
            self.min_Te = np.min(Te)

            self.max_TeT = np.max(TeT)
            self.min_TeT = np.min(TeT)

            # find the best temperatures on the tree
            TeT_mask = abs(TeT - self.Vtmean)

            self.best_temp_prop_shade = np.unravel_index(np.argmin(TeT_mask[0,:,:], axis = None), TeT_mask.shape)
            self.best_tree_shade_To = TeT[0, self.best_temp_prop_shade[1], self.best_temp_prop_shade[2]]


            self.best_temp_prop_open = np.unravel_index(np.argmin(TeT_mask[1,:,:], axis = None), TeT_mask.shape)
            self.best_tree_open_To = TeT[1, self.best_temp_prop_open[1], self.best_temp_prop_open[2]]


        # for day analysis
        
        self.temp_shade_lying = TeS[0]
        
        if not night_outside:
            self.temp_open_lying = Te[0]
            self.temp_open_standing = Te[1]
            self.temp_shade_standing = TeS[1]

        self.TeT = TeT

    def end_day(self, time_step, current_climate):
        Lizard_energy.end_day(self, time_step, current_climate)

        self.tree_open_part_from_daytime_per_day.append(((sum(self.open_tree_per_hour[time_step - 23: time_step + 1]) / 60) / self.daylight_hours_of_today) * 100)
        self.tree_shade_part_from_daytime_per_day.append(((sum(self.shaded_tree_per_hour[time_step - 23: time_step + 1]) / 60) / self.daylight_hours_of_today) * 100)
        self.tree_to_warm_part_from_daytime_per_day.append(((sum(self.climbing_to_warm_per_hour[time_step - 23: time_step + 1]) / 60) / self.daylight_hours_of_today) * 100)
        self.tree_to_cool_part_from_daytime_per_day.append(((sum(self.climbing_to_cool_per_hour[time_step - 23: time_step + 1]) / 60) / self.daylight_hours_of_today) * 100)
        self.tree_mixed_part_from_daytime_per_day.append(((sum(self.climbing_mixed[time_step - 23: time_step + 1]) / 60) / self.daylight_hours_of_today) * 100)
        self.tree_ess_part_from_daytime_per_day.append(((sum(self.essential_climbing_per_hour[time_step - 23: time_step + 1]) / 60) / self.daylight_hours_of_today) * 100)

    def assign_att_from_dict(self, dict):
        for key in dict:
            setattr(self, key, dict[key])

    def do_foraging(self):

        vmax = 10.0 ** (0.044 + 0.2 * np.log10(self.mass)) * 0.7

        if (self.To > 28.4):
            vfact = 95.0 + (40.3 - 28.4) / 5.0 * (self.To - 28.4)
        else:
            vfact = 80.0 + (28.4 - 23.03) / 15.0 * (self.To - 23.03)

        vtot = vmax * (vfact / 100.0)
        
        self.ground_available_energy_from_insects = 0.76 * 30.2 * 0.5 * self.ground_insect_abundance * 3600
        self.tree_available_energy_from_insects = 0.76 * 30.2 * 0.5 * self.tree_insect_abundance * 3600
        
        ground_energy_gain = self.ground_available_energy_from_insects * vtot * ((self.open_per_hour[-1] + self.shade_per_hour[-1]) / 60)
        tree_energy_gain = self.tree_available_energy_from_insects * vtot * ((self.open_tree_per_hour[-1] + self.shaded_tree_per_hour[-1]) / 60)

        potential_energy = self.J_gut + ground_energy_gain + tree_energy_gain
        self.J_gut = min(potential_energy, self.cmax)
        #print("hourly J_gut:"+str(self.J_gut))

    def sensitivity_analysis(self, var, change):
        Lizard_energy.sensitivity_analysis(self, var, change)
        
        if var != "0":
            if var == "food_supply":
                self.tree_insect_abundance = self.tree_insect_abundance * change

            if var == "food_supply_value":
                self.tree_insect_abundance = change
            
            if var == "tree_food_supply":
                self.tree_insect_abundance = self.tree_insect_abundance * change

            if var == "tree_food_supply_value":
                self.tree_insect_abundance = change

