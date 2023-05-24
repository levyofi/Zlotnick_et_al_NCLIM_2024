import numpy as np
import Parameters as p
from Lizard import Lizard


class Lizard_energy(Lizard):

    def __init__(self, limited_emergence = True):

        # calls the implementation of the __init__ method in the parent class 'lizard'
        Lizard.__init__(self, limited_emergence)

        # energy information

        # hourly energy intake from insects in a 30m radius,
        # assume catch 50% of insects and that 76% of the energy available
        # in an insect is in a form that could be assimilated by a lizard,
        # multiple by insect abundance (0.005 insects m-1 s-1),
        # multiplied by the number of seconds in an hour (3600)

        self.ground_insect_abundance = 0.005
        
        #self.ground_available_energy_from_insects = 0.76 * 30.2 * 0.5 * 0.005 * 3600

        self.J_gut = 0.0
        self.J_gut_hourly = 0.0
        self.DE = 0.0
        self.DE_correction = 1.0  # for sensitivity analysis

        self.e_lost = 0.0
        self.e_gained = 0.0
        self.e_current_balance = 0.0
        self.e_daily_gained = 0.0
        self.e_yearly_balance = 0.0

        self.hours_below_15 = 0
        self.hours_below_2 = 0

        self.is_foraging = False

        self.energy_balance_per_day = []	#
        self.energy_gain_per_day = []	#
        self.energy_gain_per_year = []	#
        self.growth_rate_per_year = []	#

    def step(self, current_climate, time_step):

        if current_climate[p.hour] == 0:
            if (current_climate[p.month] == 1) and (current_climate[p.day] == 1):
                self.end_year()

            self.end_day(time_step, current_climate)
            self.daylight_hours_of_today = 0

            # last hour of model
            if (current_climate[p.day] == 1) and (current_climate[p.month] == 1) and (
                    (current_climate[p.year] == 2100) or (current_climate[p.year] == 2000)):
                if current_climate[p.SWDOWN] > 1:
                    self.daylight_hours_of_today += 1
                return

        # for daylight count
        if current_climate[p.SWDOWN] > 1:
            self.daylight_hours_of_today += 1
            self.daylight_per_hour.append(True)
        else:
            self.daylight_per_hour.append(False)

        self.initial_To = self.To
        self.calculate_tb(current_climate)
        self.final_To = self.To
        self.temp_change_in_former_hour = self.final_To - self.initial_To
    
        """
        if self.To < 15:
            self.hours_below_15 = self.hours_below_15 + 1
        else:
            self.hours_below_15 = 0

        if self.To < 2:
            self.hours_below_2 = self.hours_below_2 + 1
        else:
            self.hours_below_2 = 0
        """

        self.calculate_metabolic_rate()
        self.check_activity(current_climate)
        self.digestion()

    def mini_step(self, current_climate, time_step, i, heat_analysis):

        if (current_climate[p.hour] == 0 and i != 0):
            self.end_day(time_step, current_climate)
            self.daylight_hours_of_today = 0

            # last hour of model
            if (current_climate[p.day] == 1) and (current_climate[p.month] == 1) and (
                    (current_climate[p.year] == 2100) or (current_climate[p.year] == 2000)):
                return

        # for daylight count
        if current_climate[p.SWDOWN] > 1:
            self.daylight_hours_of_today += 1

        if heat_analysis:
            self.calculate_tb_heat_par(current_climate)
        else:
            self.calculate_tb(current_climate)


        if self.To < 15:
            self.hours_below_15 = self.hours_below_15 + 1
        else:
            self.hours_below_15 = 0

        if self.To < 2:
            self.hours_below_2 = self.hours_below_2 + 1
        else:
            self.hours_below_2 = 0

        self.calculate_metabolic_rate()
        self.check_activity(current_climate)
        self.digestion()

    def check_activity(self, current_climate):
        Lizard.check_activity(self, current_climate)

        self.is_foraging = False

        if (self.is_active == True):
            if (self.check_gut_space() == True):
                self.is_foraging = True
                self.do_foraging()

        #setting the energy lost
        if (self.is_foraging):
            activity_part_of_hour = (60 - self.burrow_per_hour[-1]) / 60
            self.e_lost = self.ep * activity_part_of_hour + self.ew * (1- activity_part_of_hour)
        else:
            self.e_lost = self.ew

        #if self.hibernation():
        #    self.e_lost = self.ew - 0.33 * self.ew

        self.e_current_balance = self.e_current_balance - self.e_lost
        self.e_daily_gained = self.e_daily_gained - self.e_lost

        self.e_lost = 0.0

    def end_day(self, time_step, current_climate):
        Lizard.end_day(self, time_step)

        self.foraged_today = False

        self.e_gained = (self.DE_correction * self.DE / 24) * self.J_gut
        #print("e.gained: "+str(self.e_gained))

        self.DE = 0.0
        self.J_gut = self.J_gut - self.e_gained
        #print("end of day J_gut:"+str(self.J_gut))

        self.e_current_balance = self.e_current_balance + self.e_gained
        self.e_daily_gained = self.e_daily_gained + self.e_gained
        #print("current_balance:"+str(self.e_current_balance))
        #print("daily_gained:"+str(self.e_daily_gained))

        self.energy_balance_per_day.append(self.e_current_balance)
        self.energy_gain_per_day.append(self.e_daily_gained)
        self.e_yearly_balance = self.e_yearly_balance + self.e_daily_gained

        self.e_gained = 0.0
        self.e_daily_gained = 0.0

    def end_year(self):
        # growth rate calculation
        Mu = 197.26 * (10 ** -5) *365
        m = 2.78 * (10 ** -5)

        r0 = m * self.e_yearly_balance - Mu
        self.growth_rate_per_year.append(r0)

        self.energy_gain_per_year.append(self.e_yearly_balance)

        self.e_yearly_balance = 0.0
        r0 = None

    def calculate_metabolic_rate(self):

        self.calculate_ew()
        self.ep = self.ew * 3.0 / 1.5  # written self.ew / 1.5 * 3.0 - need to check if I got it right
        #print("energy ew:" + str(self.ew)) 

    def calculate_ew(self):

        # ew is given in (J h-1)
        # from data in Angilletta et al. 2001 PBZ.  Buckley 2008:
        # exp(-10.0 + 0.51 * log(mr.individuals.mass) + 0.115 * mr.individuals.To) * 1.5 * 60 * 60,
        # the 1.5 factor is to take into account ths SDA (Roe et al, 2005)
        self.ew = 10. ** (-0.7 + 0.51 * np.log10(self.mass) + 0.043 * self.To) * 1.5

        # originally was hidden - need to check if relevant.
        #if (self.hours_below_15 > (24 * 7)) and (self.hours_below_2 < 24):
        #   self.ew = self.ew / 2

    def calculate_cmax(self):

        # Maximum consumption from Angilletta 2001 in Joules/day
        if (self.To <= 20):
            self.cmax = 94.0
        elif (self.To > 20) and (self.To <= 30):
            self.cmax = 94.0 + (270.0 - 94.0) / 10.0 * (self.To - 20.0)
        elif (self.To > 30) and (self.To <= 33):
            self.cmax = 270.0 + (511.0 - 270.0) / 3.0 * (self.To - 30.0)
        elif (self.To > 33) and (self.To <= 36):
            self.cmax = 511.0 - (511.0 - 421.0) / 3.0 * (self.To - 33.0)
        else:
            self.cmax = 421.0

        self.cmax = self.cmax * self.mass

    def check_gut_space(self):
        self.calculate_cmax()
        check_gut_space = self.J_gut < self.cmax
        return check_gut_space

    def do_foraging(self):

        vmax = 10.0 ** (0.044 + 0.2 * np.log10(self.mass)) * 0.7

        if (self.To > 28.4):
            vfact = 95.0 + (40.3 - 28.4) / 5.0 * (self.To - 28.4)
        else:
            vfact = 80.0 + (28.4 - 23.03) / 15.0 * (self.To - 23.03)

        vtot = vmax * (vfact / 100.0)
        
        self.ground_available_energy_from_insects = 0.76 * 30.2 * 0.5 * self.ground_insect_abundance * 3600
        
        ground_energy_gain = self.ground_available_energy_from_insects * vtot * ((self.open_per_hour[-1] + self.shade_per_hour[-1]) / 60)

        potential_energy = self.J_gut + ground_energy_gain
        self.J_gut = min(potential_energy, self.cmax)
        #print("hourly J_gut:"+str(self.J_gut))

    def digestion(self):

        arcde = 85.34 - 0.5 * self.To + 0.000074 * self.To ** 3

        self.DE = self.DE + (np.sin(np.pi / 180 * arcde)) ** 2  


    def hibernation(self):

        if (self.days_without_activity > 7):
            if (self.hibernating == False):
                self.hibernating = True
                self.hibernated_this_year = True
                self.J_gut_hourly = 0.0
                self.J_gut = 0.0
        elif (self.hibernating == True):
            self.hibernating = False

    def sensitivity_analysis(self, var, change):
        Lizard.sensitivity_analysis(self, var, change)
        
        if var != "0":
            if var == "food_supply":
                self.ground_insect_abundance = self.ground_insect_abundance * change

            if var == "food_supply_value":
                self.ground_insect_abundance = change
            
            if var == "ground_food_supply":
                self.ground_insect_abundance = self.ground_insect_abundance * change

            if var == "ground_food_supply_value":
                self.ground_insect_abundance = change
                
        


