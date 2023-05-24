import numpy as np
import Parameters as p
from Climate import Climate

class Lizard:

    def __init__(self, limited_emergence = True):

        # limited emergence
        self.emergence = limited_emergence

        # CTmin and CTmax according to Angilletta 2002
        self.emergence_min_To = 11.4
        self.emergence_max_To = 40.4

        # information based on previous research
        self.svl = 67.0
        self.mass = 18.4 #self.svl ** 3.0 * 3.55 * 10 ** (-5.0)
        self.ref_period = 30
        self.energy_per_egg = 3125.0

        # central 80% of FBT from Angilletta 2001, Ecology
        # central 50% would be 35.1 C
        self.Vtmax = 36.3

        # central 80% of FBT from Angilletta 2001, Ecology
        # central 50% would be 32.0 C
        self.Vtmin = 29.4

        # preferred body temperature from Ehrenberger's data (unpublished)
        self.Vtmean = 33.1
        
        # thermal absorptivity, Bartlett & Gates 1967
        self.alpha_L_direct = 0.885
        self.alpha_L_scattered = 0.9
        
        # information calculated in the model
        self.min_Te = -100.0
        self.max_Te = -100.0
        self.min_TeS = -100.0
        self.max_TeS = -100.0
        self.To = self.Vtmean

        self.h_L = -100.0
        self.h_L_S = -100.0

        self.ew = 0.0
        self.ep = 0.0
        self.cmax = 0.0

        self.last_micro_environment = "shade"
        self.initial_To = self.Vtmean
        self.final_To = self.Vtmean
        self.temp_change_in_former_hour = 0.0

        self.age = 0
        self.age_year = 1
        self.days_with_activity = 0
        self.days_without_activity = 0

        self.is_active = False
        self.was_active_today = False
        self.hibernating = False
        self.hibernated_this_year = False
        
        self.too_hot_outside = False
        self.too_cold_outside = False


        # information for statistics
        self.daylight_hours_of_today = 0
        self.daylight_hours_per_day = []	#
        self.daylight_per_hour = [False]
        self.activity_per_day = []	#
        self.activity_hours_per_day = []	#
        self.activity_days_per_year = []	#
        self.min_julian_day_for_activity = []	#
        self.max_julian_day_for_activity = []	#

        self.open_per_hour = [0]	#
        self.shade_per_hour = [0]	#
        self.burrow_per_hour = [0]	#

        self.shade_per_hour_night = [60]
        self.burrow_per_hour_night = [0]

        self.active_per_hour = [0]
        self.active_in_open_per_hour = [0]
        self.active_in_shade_per_hour = [0]

        self.open_part_from_daytime_per_day = []	#
        self.shade_part_from_daytime_per_day = []	#
        self.burrow_part_from_daytime_per_day = []	#

        self.shade_part_from_night_per_day = []
        self.burrow_part_from_night_per_day = []

        self.active_part_from_daytime_per_day = []  #
        self.active_open_part_from_daytime_per_day = []  #
        self.active_shade_part_from_daytime_per_day = []  #

    def step(self, current_climate, time_step):
        if current_climate[p.hour] == 0:
            self.end_day(time_step)
            self.daylight_hours_of_today = 0

            # last hour of model
            if (current_climate[p.day] == 1) and (current_climate[p.month] == 1) and ((current_climate[p.year] == 2100) or (current_climate[p.year] == 2000)):
                if current_climate[p.SWDOWN] > 1:
                    self.daylight_hours_of_today += 1
                return

            if (current_climate[p.month] == 1) and (current_climate[p.day] == 1):
                self.age_year = self.age_year + 1

        if current_climate[p.SWDOWN] > 1:
            self.daylight_hours_of_today += 1
            self.daylight_per_hour.append(True)
        else:
            self.daylight_per_hour.append(False)
        
        self.initial_To = self.To
        self.calculate_tb(current_climate)
        self.final_To = self.To
        self.temp_change_in_former_hour = self.final_To - self.initial_To
        
        self.check_activity(current_climate)

    def check_activity(self, current_climate):

        self.is_active = self.active_per_hour[-1] > 0

        if self.is_active == True:
            # if first time active today
            if (self.was_active_today == False):
                self.was_active_today = True

    def end_day(self,time_step):

        self.age = self.age + 1

        if self.was_active_today == True:
            
            activity_length = len(self.active_per_hour)

            real_activity_day = sum(self.active_per_hour[activity_length - 24 : activity_length]) >= 60

            if real_activity_day == True:
                self.days_without_activity = 0
                self.days_with_activity = self.days_with_activity + 1
                self.activity_per_day.append(True)

            else:
                self.days_with_activity = 0
                self.days_without_activity = self.days_without_activity + 1
                self.activity_per_day.append(False)
        else:
            self.days_with_activity = 0
            self.days_without_activity = self.days_without_activity + 1
            self.activity_per_day.append(False)

        self.was_active_today = False


        self.open_part_from_daytime_per_day.append(((sum(self.open_per_hour[time_step - 23 : time_step + 1]) / 60) / self.daylight_hours_of_today) * 100)
        self.shade_part_from_daytime_per_day.append(((sum(self.shade_per_hour[time_step - 23 : time_step + 1]) / 60) / self.daylight_hours_of_today) * 100)
        self.burrow_part_from_daytime_per_day.append(((sum(self.burrow_per_hour[time_step - 23 : time_step + 1]) / 60) / self.daylight_hours_of_today) * 100)

        self.shade_part_from_night_per_day.append(((sum(self.shade_per_hour_night[time_step - 23 : time_step + 1]) / 60) / (24 - self.daylight_hours_of_today)) * 100)
        self.burrow_part_from_night_per_day.append(((sum(self.burrow_per_hour_night[time_step - 23: time_step + 1]) / 60) / (24 - self.daylight_hours_of_today)) * 100)

        self.active_part_from_daytime_per_day.append(((sum(self.active_per_hour[time_step - 23: time_step + 1]) / 60) / self.daylight_hours_of_today) * 100)
        self.active_open_part_from_daytime_per_day.append(((sum(self.active_in_open_per_hour[time_step - 23: time_step + 1]) / 60) / self.daylight_hours_of_today) * 100)
        self.active_shade_part_from_daytime_per_day.append(((sum(self.active_in_shade_per_hour[time_step - 23: time_step + 1]) / 60) / self.daylight_hours_of_today) * 100)

        self.daylight_hours_per_day.append(self.daylight_hours_of_today)

    def calculate_tb(self, current_climate):
        
        if (self.mass > 20):
            dt = 180
        elif (self.mass > 10):
            dt = 120
        else:
            dt = 60

        temp_time_steps_num = 3600 // dt

        # set the number of possible postures - if night (i.e., not active) then only lying is possible
        if (current_climate[p.SWDOWN] < 1):     # night

            self.active_per_hour.append(0)
            self.active_in_open_per_hour.append(0)
            self.active_in_shade_per_hour.append(0)

            # if it's too cold or the lizard has already been in burrow - burrow
            if (current_climate[p.Ta100_3cm] < p.zero_K) or (self.last_micro_environment == "burrow"):  # go underground if it's too cold
                self.To = current_climate[p.Tsoil100_12cm] - p.zero_K
                self.last_micro_environment = "burrow"

                self.open_per_hour.append(0)
                self.shade_per_hour.append(0)
                self.burrow_per_hour.append(0)

                self.shade_per_hour_night.append(0)
                self.burrow_per_hour_night.append(60)
                
                if current_climate[p.Ta100_3cm] < p.zero_K:
                    self.too_cold_outside = True
                    
                return

            # not too cold & lizard wasn't in the burrow
            else:
                self.h_L_S = self.calculate_h_L(current_climate[p.Ta100_3cm], current_climate[p.WV_3cm],
                                                current_climate[p.Air_density])

                for i in range(temp_time_steps_num):
                    self.calculate_tb_dt(dt, current_climate, i, night_outside = True)

                    self.To = self.max_TeS
                    self.last_micro_environment = "shade"

                self.open_per_hour.append(0)
                self.shade_per_hour.append(0)
                self.burrow_per_hour.append(0)

                self.shade_per_hour_night.append(60)
                self.burrow_per_hour_night.append(0)
                return

        else:       # day

            time_in_the_open = 0
            time_in_the_shade = 0
            time_in_the_burrow = 0

            time_active = 0
            time_active_in_open = 0
            time_active_in_shade = 0

            self.h_L = self.calculate_h_L(current_climate[p.Ta_3cm], current_climate[p.WV_3cm], current_climate[p.Air_density])
            self.h_L_S = self.calculate_h_L(current_climate[p.Ta100_3cm], current_climate[p.WV_3cm],
                                   current_climate[p.Air_density])

            for i in range(temp_time_steps_num):

                self.calculate_tb_dt(dt, current_climate, i)

                # choose best temperature in the shade
                if abs(self.max_TeS - self.Vtmean) < abs(self.min_TeS - self.Vtmean):
                    best_shade_To = self.max_TeS
                else:
                    best_shade_To = self.min_TeS

                # choose best temperature in the open
                if (abs(self.max_Te - self.Vtmean) < abs(self.min_Te - self.Vtmean)):
                    best_open_To = self.max_Te
                else:
                    best_open_To = self.min_Te

                # limited_emergence
                can_emerge = self.check_emergence()

                if not can_emerge:      # cannot emerge
                    self.To = current_climate[p.Tsoil100_12cm] - p.zero_K
                    time_in_the_burrow = time_in_the_burrow + (dt / 60)
                    self.last_micro_environment = "burrow"

                else:       # can emerge
                    open_abs = abs(best_open_To - self.Vtmean)
                    shade_abs = abs(best_shade_To - self.Vtmean)

                    temp_in_range = False

                    if open_abs == min(open_abs, shade_abs):
                        if (best_open_To < self.emergence_max_To) and (best_open_To > self.emergence_min_To):
                            temp_in_range = True
                            self.To = best_open_To
                            time_in_the_open = time_in_the_open + (dt/60)
                            self.last_micro_environment = "open"

                    elif shade_abs == min(open_abs, shade_abs):
                        if (best_shade_To < self.emergence_max_To) and (best_shade_To > self.emergence_min_To):
                            temp_in_range = True
                            self.To = best_shade_To
                            time_in_the_shade = time_in_the_shade + (dt/60)
                            self.last_micro_environment = "shade"

                    if not temp_in_range:
                        self.To = current_climate[p.Tsoil100_12cm] - p.zero_K
                        time_in_the_burrow = time_in_the_burrow + (dt / 60)
                        self.last_micro_environment = "burrow"

                        if best_shade_To > self.emergence_max_To:
                            self.too_hot_outside = True
                        elif best_open_To < self.emergence_min_To:
                            self.too_cold_outside = True

                    else:
                        # perfect thermoregulation
                        if (self.Vtmean < max(best_open_To, best_shade_To)) and (self.Vtmean > min(best_open_To, best_shade_To)):
                            self.To = self.Vtmean

                        if (self.To > self.Vtmin) and (self.To < self.Vtmax):
                            time_active = time_active + (dt / 60)

                            if self.last_micro_environment == "open":
                                time_active_in_open = time_active_in_open + (dt / 60)
                            else:
                                time_active_in_shade = time_active_in_shade + (dt / 60)

            # updating time counters
            self.open_per_hour.append(time_in_the_open)
            self.shade_per_hour.append(time_in_the_shade)
            self.burrow_per_hour.append(time_in_the_burrow)

            self.shade_per_hour_night.append(0)
            self.burrow_per_hour_night.append(0)

            self.active_per_hour.append(time_active)
            self.active_in_open_per_hour.append(time_active_in_open)
            self.active_in_shade_per_hour.append(time_active_in_shade)

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

        A_L = 0.00758 # 0.0314 * 3.14159 * (Mb_total ** (2 / 3))  # surface area (in m2)
        To = self.To + p.zero_K  # current body temperature in kelvin

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

        lying = 0
        standing = 1

        A_downs = [0.0] * current_num_of_postures
        A_contacts = [0.0] * current_num_of_postures
        Te = [0.0] * current_num_of_postures
        TeS = [0.0] * current_num_of_postures

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

            #A_down = A_downs[i_posture]  # area of the skin facing toward the ground - lying lizard
            #A_up = Aee #0.6 * A_L  # area of the skin facing toward the sky

            A_contact = A_contacts[i_posture]  # area lizards contacts with the ground
            A_down = A_downs[i_posture]
            Aee = 0.89 * (A_L - A_contact)
            Aair = A_L - A_contact  # skin area that is exposed to air

            #### shade ####

            # solar radiation
            SdQ_solar = alpha_L_scattered * Aee * diff * current_climate[p.SWDOWN]

            # IR radiation
            SdQ_IR = (epsilon_lizard * p.sigma * A_down * current_climate[p.Tsurface100] ** 4) + (epsilon_lizard * p.sigma * A_up * current_climate[p.TAH] ** 4) - (epsilon_lizard * p.sigma * Aair * To ** 4)

            # conduction
            SdQ_cond = (A_contact * K_lizard * (current_climate[p.Tsurface100] - To)) / (0.5 * lambda_lizard)

            # convection
            SdQ_conv = self.h_L_S * Aair * (current_climate[p.Ta100_3cm] - To)

            # energy balance calculation
            SdQe = SdQ_solar + SdQ_IR + dQ_meta + SdQ_cond + SdQ_conv
            SdTe = SdQe / (((self.mass) / 1000) * c_lizard)

            TeS[i_posture] = To + (SdTe * dt) - p.zero_K


            if not night_outside:

                #### open ####

                # solar radiation
                dQ_solar = alpha_L_direct * A_p * ((1 - diff) * current_climate[p.SWDOWN]) + alpha_L_scattered * Aee * diff * current_climate[p.SWDOWN]

                # IR radiation
                dQ_IR =  (epsilon_lizard * p.sigma * A_down * current_climate[p.Tsurface] ** 4) + (epsilon_lizard * A_up * current_climate[p.GLW]) - (epsilon_lizard * p.sigma * Aair * To ** 4)

                # conduction
                dQ_cond = (A_contact * K_lizard * (current_climate[p.Tsurface] - To)) / (0.5 * lambda_lizard)

                # convection
                dQ_conv = self.h_L * Aair * (current_climate[p.Ta_3cm] - To)

                # energy balance calculation
                dQe = dQ_solar + dQ_IR + dQ_meta + dQ_cond + dQ_conv
                dTe = dQe / (((self.mass) / 1000) * c_lizard)

                Te[i_posture] = To + (dTe * dt) - p.zero_K

            #if (current_climate[p.day] == 15) and (current_climate[p.month] == 9) and (current_climate[p.year] == 1981):
            #    if ((i+1) == 3600 / dt) :
            #        print("stop")

        # find the two extremes from all shade / open * lying / standing positions

        self.max_TeS = max(TeS)
        self.min_TeS = min(TeS)

        if not night_outside:
            self.max_Te = max(Te)
            self.min_Te = min(Te)

    # Tair_k - air temperature (Kelvin) , vel - wind velocity (m/s), air_density - kg/m3
    def calculate_h_L(self, Tair_k, vel, air_density):
        #press = 101325  # air pressure(Pa)

        Tair = Tair_k - p.zero_K

        air_thcond = 0.02425 + (7.038 * (10 ** -5) * Tair)  # air thermal conductivity, W/(m.K)
        air_visdyn = (1.8325 * (10 ** -5) * ((296.16 + 120) / ((Tair + p.zero_K) + 120))) * (
                    ((Tair + p.zero_K) / 296.16) ** 1.5)  # dynamic viscosity of air, kg/(m.s)

        lizard_density = 932  # animal density (kg/m3)
        volume = (self.mass / 1000) / lizard_density  # volume, m3
        L = volume ** (1 / 3)  # characteristic dimension, m

        Re = air_density * vel * L / air_visdyn  # Reynolds number
        PR = 1005.7 * air_visdyn / air_thcond  # Prandlt number

        # calculating forced convection coefficient
        NUfor = 0.35 * (Re ** 0.6)
        h_conv_forced = NUfor * air_thcond / L  # convection coefficent, forced

        # calculating free convection coefficient - self.To + 0.1 = T_skin (from NicheMapR)
        GR = abs((air_density ** 2) * (1 / (Tair + p.zero_K)) * 9.80665 * (L ** 3) * (self.To + 0.1 - Tair) / (
                    air_visdyn ** 2))  # Grashof number
        Raylei = GR * PR  # Rayleigh number

        # get Nusselt for Free Convection
        if Raylei < 1.0e-05:
            NUfre = 0.4
        elif Raylei < 0.1:
            NUfre = 0.976 * (Raylei ** 0.0784)
        elif Raylei < 100:
            NUfre = 1.1173 * (Raylei ** 0.1344)
        elif Raylei < 10000.0:
            NUfre = 0.7455 * (Raylei ** 0.2167)
        elif Raylei < 1.0e+09:
            NUfre = 0.5168 * (Raylei ** 0.2501)
        elif Raylei < 1.0e+12:
            NUfre = 0.5168 * (Raylei ** 0.2501)
        else:
            NUfre = 0.5168 * (Raylei ** 0.2501)

        h_conv_free = NUfre * air_thcond / L  # convection coefficent, free

        if (vel < 0.5):
            return h_conv_free
        else:
            return h_conv_forced

    def check_emergence(self):
        can_emerge = True
        if self.emergence:
            if (self.last_micro_environment == "burrow"):
                if self.too_cold_outside:
                    if ((self.To < self.emergence_min_To) or (self.temp_change_in_former_hour < 0.1)):
                        can_emerge = False

                elif self.too_hot_outside:
                    if ((self.To > self.emergence_max_To) or (self.temp_change_in_former_hour > -0.1)):
                        can_emerge = False
  
        if can_emerge:
            self.too_cold_outside = False
            self.too_hot_outside = False

        return(can_emerge)

    def sensitivity_analysis(self, var, change):
        if var != "0":
            if var == "mass":
                self.mass = self.mass * change

            if var == "mass_value":
                self.mass = change
            
            if var == "emergence_min":
                self.emergence_min_To = self.emergence_min_To * change

            if var == "emergence_min_value":
                self.emergence_min_To = change
            
            if var == "activity_temp_range":
                middle = (self.Vtmin + self.Vtmax) / 2
                diff = self.Vtmax - self.Vtmin
                new_diff = diff * change

                self.Vtmin = middle - (new_diff / 2)
                self.Vtmax = middle + (new_diff / 2)

            if var == "lizard_color":
                self.alpha_L_direct = self.alpha_L_direct * change
                self.alpha_L_scattered = self.alpha_L_scattered * change

            if var == "lizard_color_value":
                self.alpha_L_direct = change
                self.alpha_L_scattered = change
            




