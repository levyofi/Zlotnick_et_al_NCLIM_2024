import Parameters as p
import netCDF4
import numpy as np

# defines the class "climate", which holds all the micro-climatic information.

class Climate:
    def __init__(self):

        self.time_step = 0  # sets the time steps to zero

        # sets all class variables to be None
        self.is_loaded = None  # an indicator for loading data
        self.julian_day = None
        self.climate_data = None
        self.current_climate = None
        self.lat = None
        self.lon = None
        self.number_of_steps = None

        self.mean_ta_year = None
        self.mean_ta_winter = None
        self.mean_ta_summer = None
        self.sd_ta_year = None
        self.sd_ta_winter = None
        self.sd_ta_summer = None

        self.mean_first_daylight_summer = None
        self.mean_last_daylight_summer = None
        self.mean_first_daylight_winter = None
        self.mean_last_daylight_winter = None

        self.inputfilename = None

        self.month_per_day = []

    # loads the micro-climatic information to the object from external netCDF files
    # 'inputfilename' = includes the location id and the year. being used to collect the matching netCDF files

    def load_data(self, inputfilename):

        self.is_loaded = False
        self.inputfilename = inputfilename

        if not endswith(inputfilename, ".nc"):
            inputfilename = inputfilename + ".nc"

        path = '../netcdf_files'            # path to location of micro-climate files

        # creates the full files locations (in the computer) using the given 'inputfilename'
        SWDOWN_nc_file = path+'/SWDOWN_' + inputfilename
        GLW_nc_file = path+'/GLW_' + inputfilename
        TAH_nc_file = path+'/TAH_' + inputfilename
        Tsurface_nc_file = path+'/Tsurface_' + inputfilename
        Tair_nc_file = path+'/Tair_' + inputfilename
        Tsoil_nc_file = path+'/Tsoil_' + inputfilename
        WV_nc_file = path+'/WIND10_' + inputfilename
        Ttrunk_nc_file = path+'/trunk_' + inputfilename
        RHOAIR_nc_file = path+'/RHOAIR_' + inputfilename

        # sets all file variables to 'None' so an error in loading files can be detected later
        # and closing files will be done correctly

        SWDOWN_ncid = None
        GLW_ncid = None
        TAH_ncid = None
        Tsurface_ncid = None
        Tair_ncid = None
        Tsoil_ncid = None
        WV_ncid = None
        Ttrunk_ncid = None
        RHOAIR_ncid = None

        try:
            # loads all netCDF files to their matching variables
            SWDOWN_ncid = netCDF4.Dataset(SWDOWN_nc_file, 'r')
            GLW_ncid = netCDF4.Dataset(GLW_nc_file, 'r')
            TAH_ncid = netCDF4.Dataset(TAH_nc_file, 'r')
            Tsurface_ncid = netCDF4.Dataset(Tsurface_nc_file, 'r')
            Tair_ncid = netCDF4.Dataset(Tair_nc_file, 'r')
            Tsoil_ncid = netCDF4.Dataset(Tsoil_nc_file, 'r')
            WV_ncid = netCDF4.Dataset(WV_nc_file, 'r')
            Ttrunk_ncid = netCDF4.Dataset(Ttrunk_nc_file, 'r')
            RHOAIR_ncid = netCDF4.Dataset(RHOAIR_nc_file, 'r')

            # get lat and lon   lat = latitude line     lon = longitude line
            self.lon = float(SWDOWN_ncid.variables['lon'][0])
            self.lat = float(SWDOWN_ncid.variables['lat'][0])

            # get the number of time points to be checked (number of hours)
            time = SWDOWN_ncid.variables['time']
            self.number_of_steps = len(time)

            # creates big numpy 2-dimentional array, currently full with zeroes (later will be filled with data)
            self.climate_data = np.zeros((110, self.number_of_steps), float)

            # create time variables
            # time is loaded for the file to a numpy array (time_a)
            # from this array we derive 4 different arrays,
            # including in each position the year, month, day or hour for a specific time point
            # (each array has one dimension, and includes 'number of rows' cells, each refers to one time point)
            # the objects in the 'time_a' array are int objects, given in the format: yyyymmddhh
            time_a = np.array(time)
            years_a = time_a // 1000000
            months_a = (time_a % 1000000) // 10000
            days_a = (time_a % 10000) // 100
            hours_a = time_a % 100

            # converting the time arrays to list objects
            years = list(years_a)
            months = list(months_a)
            days = list(days_a)
            hours = list(hours_a)

            # adding time variables to big mat (rows 1-4)
            self.climate_data[p.hour] = hours
            self.climate_data[p.day] = days
            self.climate_data[p.month] = months
            self.climate_data[p.year] = years

            # in each of the following variables, the data is being loaded from the file to a variable,
            # then being added to the 'self.climate_data'

            # reading TAH (canopy air temperature) and adding to big mat (row 5)
            TAHs = TAH_ncid.variables["TAH"]
            self.climate_data[p.TAH] = list(np.array(TAHs))

            # reading SWDOWN (visible radiation flux) and adding to big mat (row 6)
            SWDOWNs = SWDOWN_ncid.variables["SWDOWN"]
            self.climate_data[p.SWDOWN] = list(np.array(SWDOWNs))

            # reading solar_trunk_beam (direct solar radiation on trunk) and adding to big mat (row 7)
            total_solar_trunk_beams = Ttrunk_ncid.variables["solar_trunk_beam"]
            total_solar_trunk_beams_a = np.array(total_solar_trunk_beams)

            solar_trunk_diffuses = Ttrunk_ncid.variables["solar_trunk_diffuse"]
            solar_trunk_diffuses_a = np.array(solar_trunk_diffuses)

            solar_trunk_beams_a = total_solar_trunk_beams_a - solar_trunk_diffuses_a

            solar_trunk_beams_lst = list(solar_trunk_beams_a)
            solar_trunk_beams_lst[0] = 0
            self.climate_data[p.solar_trunk_beam] = solar_trunk_beams_lst

            # reading solar_trunk_diffuse (scattered solar radiation on trunk) and adding to big mat (row 8)
            solar_trunk_diffuses_lst = list(solar_trunk_diffuses_a)
            solar_trunk_diffuses_lst[0] = 0
            self.climate_data[p.solar_trunk_diffuse] = list(np.array(solar_trunk_diffuses_lst))

            # reading diffuse_ratio (the part of scattered radiation from all solar radiation) and adding to big mat (row 9)
            diffuse_ratios = Ttrunk_ncid.variables["diffuse_ratio"]
            diffuse_ratios_a = np.array(diffuse_ratios)
            mask_nan = np.isnan(diffuse_ratios_a)
            diffuse_ratios_a = np.where(mask_nan, 0, diffuse_ratios_a)
            diffuse_ratios_lst = list(diffuse_ratios_a)
            self.climate_data[p.diffuse_ratio] = list(np.array(diffuse_ratios_lst))

            # reading GLW (near-IR radiation) and adding to big mat (row 10)
            GLWs = GLW_ncid.variables["GLW"]
            self.climate_data[p.GLW] = list(np.array(GLWs))

            # reading Tsurface (ground temperatures in 2 different shade levels) and adding to big mat (rows 11-12)
            num_of_shade_levels = 2
            Tsurfaces = Tsurface_ncid.variables["Tsurface"]
            Tsurfaces_n = list(np.array(Tsurfaces[0]))
            self.climate_data[p.Tsurface] = Tsurfaces_n
            Tsurfaces_n100 = list(np.array(Tsurfaces[-1]))
            self.climate_data[p.Tsurface100] = Tsurfaces_n100

            # reading Tsoil in 100% shade, at 12cm depth and adding to big mat (row 13)
            Tsoils = Tsoil_ncid.variables["Tsoil"]
            Tsoils_n = list(np.array(Tsoils[3,-1,:]))
            self.climate_data[p.Tsoil100_12cm] = Tsoils_n

            # reading Tair (air temperature in different shade levels and different heights) and adding to big mat (rows 14-52)
            Tairs = Tair_ncid.variables["Tair"]
            Tairs_n = list(np.array(Tairs[:,0,:]))
            self.climate_data[p.Ta_3cm: p.Ta_198cm + 1] = Tairs_n
            Tairs_n100 = list(np.array(Tairs[:,-1, :]))
            self.climate_data[p.Ta100_3cm: p.Ta100_198cm + 1] = Tairs_n100
            Tairs_n50 = list(np.array(Tairs[0,2,:]))
            self.climate_data[p.Ta50] = Tairs_n50

            # reading WV (wind velocity in different heights) and adding to big mat (rows 53-71)
            WVs = WV_ncid.variables["WIND10"]
            WVs_n = list(np.array(WVs))
            self.climate_data[p.WV_3cm : p.WV_198cm + 1] = WVs_n

            # reading Ttrunk (trunk temperature in different heights and different shade levels)
            # and adding to big mat (rows 72-109)
            Ttrunks = Ttrunk_ncid.variables["Ttrunk"]
            Ttrunks_n = list(np.array(Ttrunks[:, 0, :]))
            self.climate_data[p.Ttrunk_3cm: p.Ttrunk_198cm + 1] = Ttrunks_n
            Ttrunks_n100 = list(np.array(Ttrunks[:, -1, :]))
            self.climate_data[p.Ttrunk100_3cm: p.Ttrunk100_198cm + 1] = Ttrunks_n100

            # reading the air density and adding to big mat (row 110)
            Air_densitys = RHOAIR_ncid.variables["RHOAIR"]
            self.climate_data[p.Air_density] = list(np.array(Air_densitys))

            self.is_loaded = True

            # print 'climate_data' to an external csv file named 'out'
            #out = open('climate_data.csv', 'w')
            #for row in self.climate_data:
            #    for column in row:
            #        out.write(str(column) + ',')
            #    out.write('\n')
            #out.close()

        # detects errors in file loading and prints the matching error message
        except ZeroDivisionError:
            if SWDOWN_ncid == None:
                print("Error in opening SWDOWN file")
            if GLW_ncid == None:
                print("Error in opening GLW file")
            if TAH_ncid == None:
                print("Error in opening TAH file")
            if Tsurface_ncid == None:
                print("Error in opening Tsurface file")
            if Tair_ncid == None:
                print("Error in opening Tair file")
            if Tsoil_ncid == None:
                print("Error in opening Tsoil file")
            if WV_ncid == None:
                print("Error in opening WV file")
            if Ttrunk_ncid == None:
                print("Error in opening Ttrunk file")
            if RHOAIR_ncid == None:
                print("Error in opening RHOAIR file")

        # closes each file that has been successfully opened
        finally:
            if SWDOWN_ncid != None:
                SWDOWN_ncid.close()
            if GLW_ncid != None:
                GLW_ncid.close()
            if TAH_ncid != None:
                TAH_ncid.close()
            if Tsurface_ncid != None:
                Tsurface_ncid.close()
            if Tair_ncid != None:
                Tair_ncid.close()
            if Tsoil_ncid != None:
                Tsoil_ncid.close()
            if WV_ncid != None:
                WV_ncid.close()
            if Ttrunk_ncid != None:
                Ttrunk_ncid.close()
            if RHOAIR_ncid != None:
                RHOAIR_ncid.close()


        # sets 'current_climate' to be an array that includes the matching data for the first time step
        # and 'julian_day' to be the first day of the year
        self.current_climate = self.climate_data[:, self.time_step]
        self.julian_day = 1

        # calculates 'mean_ta' to be the mean air temperature in 50% shade of all time points
        mean_ta = sum(self.climate_data[p.Ta50, :]) / self.number_of_steps

        # calculate mean and sd for winter and summer + mean daylight hours
        # use the approach suggested in http://mathcentral.uregina.ca/QQ/database/QQ.09.02/carlos1.html
        # to avoid looping twice through the data
        # also see "The Art of Computer Programming, Volume 2: Seminumerical Algorithms", section 4.2.2.
        # and B.P. Welford, Technometrics, 4, (1962), 419-420.
        # code adapted from http://en.wikipedia.org/wiki/Algorithms_for_calculating_varience
        # (function online_variance(data))

        isummer = 0
        iwinter = 0
        iyear = 0

        iwinter_days = 1
        isummer_days = 1

        self.mean_ta_summer = 0
        self.mean_ta_winter = 0
        self.mean_ta_year = 0
        sd_ta_summer = 0
        sd_ta_winter = 0
        sd_ta_year = 0

        self.mean_first_daylight_summer = 0
        self.mean_last_daylight_summer = 0
        self.mean_first_daylight_winter = 0
        self.mean_last_daylight_winter = 0

        for i in range(self.number_of_steps):
            imonth = self.climate_data[p.month, i]
            ihour = self.climate_data[p.hour, i]
            tair = self.climate_data[p.Ta50, i]

            # calculating mean temperature in winter (December - February)
            if (imonth == 12) or (imonth == 1) or (imonth == 2):
                iwinter += 1
                delta = tair - self.mean_ta_winter
                self.mean_ta_winter = self.mean_ta_winter + delta / iwinter
                sd_ta_winter = sd_ta_winter + delta * (tair - self.mean_ta_winter)

                # calculating mean first and last hur of daylight during the winter
                if (i != self.number_of_steps - 1):

                    if ihour == 0:
                        iwinter_days += 1

                    if self.climate_data[p.SWDOWN, i] > 1 and self.climate_data[p.SWDOWN, i - 1] <= 1:
                        curr_hour = self.climate_data[p.hour, i]
                        if curr_hour < 6:
                            curr_hour = curr_hour + 24

                        delta_first_hour_winter = curr_hour - self.mean_first_daylight_winter
                        self.mean_first_daylight_winter = self.mean_first_daylight_winter + delta_first_hour_winter / iwinter_days

                    if self.climate_data[p.SWDOWN, i] > 1 and self.climate_data[p.SWDOWN, i + 1] <= 1:
                        curr_hour = self.climate_data[p.hour, i]
                        if curr_hour < 6:
                            curr_hour = curr_hour + 24

                        delta_last_hour_winter = curr_hour - self.mean_last_daylight_winter
                        self.mean_last_daylight_winter = self.mean_last_daylight_winter + delta_last_hour_winter / iwinter_days

            # calculating mean temperature in summer (June - August)
            if (imonth >= 6) and (imonth <= 8):
                isummer += 1
                delta = tair - self.mean_ta_summer
                self.mean_ta_summer = self.mean_ta_summer + delta / isummer
                sd_ta_summer = sd_ta_summer + delta * (tair - self.mean_ta_summer)

                # calculating mean first and last hur of daylight during the summer
                if (i != self.number_of_steps - 1):

                    if ihour == 0:
                        isummer_days += 1

                    if self.climate_data[p.SWDOWN, i] > 1 and self.climate_data[p.SWDOWN, i - 1] <= 1:
                        curr_hour = self.climate_data[p.hour, i]
                        if curr_hour < 6:
                            curr_hour = curr_hour + 24

                        delta_first_hour_summer = curr_hour - self.mean_first_daylight_summer
                        self.mean_first_daylight_summer = self.mean_first_daylight_summer + delta_first_hour_summer / isummer_days

                    if self.climate_data[p.SWDOWN, i] > 1 and self.climate_data[p.SWDOWN, i + 1] <= 1:
                        curr_hour = self.climate_data[p.hour, i]
                        if curr_hour < 6:
                            curr_hour = curr_hour + 24

                        delta_last_hour_summer = curr_hour - self.mean_last_daylight_summer
                        self.mean_last_daylight_summer = self.mean_last_daylight_summer + delta_last_hour_summer / isummer_days

            iyear += 1
            delta = tair - self.mean_ta_year
            self.mean_ta_year = self.mean_ta_year + delta / iyear
            sd_ta_year = sd_ta_year + delta * (tair - self.mean_ta_year)

            # building a list of month per days
            if self.climate_data[p.hour, i] == 1:
                self.month_per_day.append(self.climate_data[p.month, i])

        self.sd_ta_winter = np.sqrt(sd_ta_winter / float(iwinter - 1))
        self.sd_ta_summer = np.sqrt(sd_ta_summer / float(isummer - 1))
        self.sd_ta_year = np.sqrt(sd_ta_year / float (iyear - 1))

        #print("the average air temperature during summer is: " + str(self.mean_ta_summer) + " Kelvin")
        #print("the average air temperature during winter is: " + str(self.mean_ta_winter) + " Kelvin")
        #print("the average air temperature: " + str(self.mean_ta_year) + " Kelvin")

        if self.mean_first_daylight_winter > 24:
            self.mean_first_daylight_winter = self.mean_first_daylight_winter - 24

        if self.mean_last_daylight_winter > 24:
            self.mean_last_daylight_winter = self.mean_last_daylight_winter - 24

        if self.mean_first_daylight_summer > 24:
            self.mean_first_daylight_summer = self.mean_first_daylight_summer - 24

        if self.mean_last_daylight_summer > 24:
            self.mean_last_daylight_summer = self.mean_last_daylight_summer - 24

        #print("the average first hour of daylight during the winter is: " + str(self.mean_first_daylight_winter))
        #print("the average last hour of daylight during the winter is: " + str(self.mean_last_daylight_winter))
        #print("the average first hour of daylight during the summer is: " + str(self.mean_first_daylight_summer))
        #print("the average last hour of daylight during the summer is: " + str(self.mean_last_daylight_summer))

    # sets 'current_climate' to be the column in 'climate_data' mat of the first hour of a given date
    def go_to_date(self, m_day, m_month, m_year):
        current_time_step = self.time_step
        # print("current date: " + str(int(self.current_climate[p.day])) + '/' + str(int(self.current_climate[p.month])) + '/' + str(int(self.current_climate[p.year])))

        # go to the beginning of the time period
        self.time_step = 0
        self.current_climate = self.climate_data[ : , self.time_step]

        while self.time_step < self.number_of_steps:
            self.step()
            if (self.current_climate[p.year] == m_year) and (self.current_climate[p.month] == m_month) and (self.current_climate[p.day] == m_day):
                print("The new current date is:" + str(int(self.current_climate[p.day])) + "/" + str(int(self.current_climate[p.month])) + "/" + str(int(self.current_climate[p.year])))
                return

        # if date wasn't found - sets 'current_climate' to be what it was before the search
        print("The date: " + str(m_day) + "/" + str(m_month) + "/" + str(m_year) + " was not found")
        self.time_step = current_time_step
        self.current_climate = self.climate_data[:, self.time_step]

    def return_hottest_day(self):
        air_temp_a = np.array(self.climate_data[p.Ta50])
        hottest_hour_index = np.argmax(air_temp_a)

        m_day = self.climate_data[p.day, hottest_hour_index]
        m_month = self.climate_data[p.month, hottest_hour_index]
        m_year = self.climate_data[p.year, hottest_hour_index]

        return (m_day, m_month, m_year)

    def return_coldest_day(self):
        air_temp_a = np.array(self.climate_data[p.Ta50])
        coldest_hour_index = np.argmin(air_temp_a)

        m_day = self.climate_data[p.day, coldest_hour_index]
        m_month = self.climate_data[p.month, coldest_hour_index]
        m_year = self.climate_data[p.year, coldest_hour_index]

        return (m_day, m_month, m_year)

    # write to file the climatic data of one day
    def data_for_day(self, m_day, m_month, m_year):
        self.go_to_date(m_day, m_month, m_year)
        
        data_for_day_mat = []
        parameters_list = ["hour", "day", "month", "year", "TAH", "SWDOWN", "solar_trunk_beam", "solar_trunk_diffuse", "diffuse_ratio", "GLW", "Tsurface", "Tsurface100", "Tsoil100_12cm", "Ta_3cm", "Ta_6cm", "Ta_9cm", "Ta_12cm", "Ta_15cm", "Ta_18cm", "Ta_21cm", "Ta_24cm", "Ta_27cm", "Ta_30cm", "Ta_48cm", "Ta_66cm", "Ta_84cm", "Ta_102cm", "Ta_120cm", "Ta_138cm", "Ta_156cm", "Ta_174cm", "Ta_198cm", "Ta100_3cm", "Ta100_6cm", "Ta100_9cm", "Ta100_12cm", "Ta100_15cm", "Ta100_18cm", "Ta100_21cm", "Ta100_24cm", "Ta100_27cm", "Ta100_30cm", "Ta100_48cm", "Ta100_66cm", "Ta100_84cm", "Ta100_102cm", "Ta100_120cm", "Ta100_138cm", "Ta100_156cm", "Ta100_174cm", "Ta100_198cm", "Ta50", "WV_3cm", "WV_6cm", "WV_9cm", "WV_12cm", "WV_15cm", "WV_18cm", "WV_21cm", "WV_24cm", "WV_27cm", "WV_30cm", "WV_48cm", "WV_66cm", "WV_84cm", "WV_102cm", "WV_120cm", "WV_138cm", "WV_156cm", "WV_174cm", "WV_198cm", "Ttrunk_3cm", "Ttrunk_6cm", "Ttrunk_9cm", "Ttrunk_12cm", "Ttrunk_15cm", "Ttrunk_18cm", "Ttrunk_21cm", "Ttrunk_24cm", "Ttrunk_27cm", "Ttrunk_30cm", "Ttrunk_48cm", "Ttrunk_66cm", "Ttrunk_84cm", "Ttrunk_102cm", "Ttrunk_120cm", "Ttrunk_138cm", "Ttrunk_156cm", "Ttrunk_174cm", "Ttrunk_198cm", "Ttrunk100_3cm", "Ttrunk100_6cm", "Ttrunk100_9cm", "Ttrunk100_12cm", "Ttrunk100_15cm", "Ttrunk100_18cm", "Ttrunk100_21cm", "Ttrunk100_24cm", "Ttrunk100_27cm", "Ttrunk100_30cm", "Ttrunk100_48cm", "Ttrunk100_66cm", "Ttrunk100_84cm", "Ttrunk100_102cm", "Ttrunk100_120cm", "Ttrunk100_138cm", "Ttrunk100_156cm", "Ttrunk100_174cm", "Ttrunk100_198cm", "Air_density"]
        
        data_for_day_mat.append(parameters_list)
        
        for i in range(24):
            data_for_day_mat.append([i] + list(self.current_climate))
            self.step()

        data_for_day_a = np.transpose(np.array(data_for_day_mat))

        # print 'data_for_day_mat' to an external csv file
        out = open('climate_data_for_day.csv', 'w')
        for row in data_for_day_a:
            for column in row:
                out.write(str(column) + ',')
            out.write('\n')
        out.close()

    # sets 'current_climate' to be that of the following day
    # corrects 'julian_day' at the end of the year
    def step(self):
        self.time_step = self.time_step + 1
        if self.time_step >= self.number_of_steps:
            self.current_climate = None
        else:
            if self.climate_data[p.year, self.time_step] > self.current_climate[p.year]:
                self.julian_day = 0

            self.current_climate = self.climate_data[:, self.time_step]
            if self.current_climate[p.hour] == 0:
                self.julian_day = self.julian_day + 1

    # allows user to get indication for the loading status of the climate data
    def loading_status(self):
        if self.is_loaded == None:
            print("Loading never started")
        if self.is_loaded == True:
            print("Loading ended successfully")
        if self.is_loaded == False:
            print("Loading started but did not end successfully")
        return self.is_loaded

    # if loading has started - initialize all variables to be 'None'

    def initialize(self):
        status = self.loading_status()
        if (status == True) or (status == False):
            for var in [self.is_loaded, self.current_climate, self.time_step, self.climate_data,
                        self.julian_day, self.number_of_steps, self.lat, self.lon, self.mean_ta_year, self.mean_ta_summer, self.mean_ta_winter, self.sd_ta_year, self.sd_ta_summer, self.sd_ta_winter, self.inputfilename, self.mean_first_daylight_summer,self.mean_last_daylight_summer, self.mean_first_daylight_winter,self.mean_last_daylight_winter]:
                var = None


#path = "2013_MIC_CLIM_36_past_33.832_-111.502"
#climate = Climate()
#climate.load_data(path)
#climate.data_for_day(1,7,1982)
