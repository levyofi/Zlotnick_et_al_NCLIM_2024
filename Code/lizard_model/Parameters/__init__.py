import numpy as np

# rows in the climate_data matrix:

hour = 0
day = 1
month = 2
year = 3
TAH = 4
SWDOWN = 5
solar_trunk_beam = 6        # direct solar radiation on trunk
solar_trunk_diffuse = 7     # scattered solar radiation on trunk
diffuse_ratio = 8           # part of diffused radiation (scattered) from all solar radiation
GLW = 9
Tsurface = 10
Tsurface100 = 11
Tsoil100_12cm = 12

Ta_3cm = 13
Ta_6cm = 14
Ta_9cm = 15
Ta_12cm = 16
Ta_15cm = 17
Ta_18cm = 18
Ta_21cm = 19
Ta_24cm = 20
Ta_27cm = 21
Ta_30cm = 22
Ta_48cm = 23
Ta_66cm = 24
Ta_84cm = 25
Ta_102cm = 26
Ta_120cm = 27
Ta_138cm = 28
Ta_156cm = 29
Ta_174cm = 30
Ta_198cm = 31
Ta100_3cm = 32
Ta100_6cm = 33
Ta100_9cm = 34
Ta100_12cm = 35
Ta100_15cm = 36
Ta100_18cm = 37
Ta100_21cm = 38
Ta100_24cm = 39
Ta100_27cm = 40
Ta100_30cm = 41
Ta100_48cm = 42
Ta100_66cm = 43
Ta100_84cm = 44
Ta100_102cm = 45
Ta100_120cm = 46
Ta100_138cm = 47
Ta100_156cm = 48
Ta100_174cm = 49
Ta100_198cm = 50

Ta50 = 51

WV_3cm = 52
WV_6cm = 53
WV_9cm = 54
WV_12cm = 55
WV_15cm = 56
WV_18cm = 57
WV_21cm = 58
WV_24cm = 59
WV_27cm = 60
WV_30cm = 61
WV_48cm = 62
WV_66cm = 63
WV_84cm = 64
WV_102cm = 65
WV_120cm = 66
WV_138cm = 67
WV_156cm = 68
WV_174cm = 69
WV_198cm = 70

Ttrunk_3cm = 71
Ttrunk_6cm = 72
Ttrunk_9cm = 73
Ttrunk_12cm = 74
Ttrunk_15cm = 75
Ttrunk_18cm = 76
Ttrunk_21cm = 77
Ttrunk_24cm = 78
Ttrunk_27cm = 79
Ttrunk_30cm = 80
Ttrunk_48cm = 81
Ttrunk_66cm = 82
Ttrunk_84cm = 83
Ttrunk_102cm = 84
Ttrunk_120cm = 85
Ttrunk_138cm = 86
Ttrunk_156cm = 87
Ttrunk_174cm = 88
Ttrunk_198cm = 89
Ttrunk100_3cm = 90
Ttrunk100_6cm = 91
Ttrunk100_9cm = 92
Ttrunk100_12cm = 93
Ttrunk100_15cm = 94
Ttrunk100_18cm = 95
Ttrunk100_21cm = 96
Ttrunk100_24cm = 97
Ttrunk100_27cm = 98
Ttrunk100_30cm = 99
Ttrunk100_48cm = 100
Ttrunk100_66cm = 101
Ttrunk100_84cm = 102
Ttrunk100_102cm = 103
Ttrunk100_120cm = 104
Ttrunk100_138cm = 105
Ttrunk100_156cm = 106
Ttrunk100_174cm = 107
Ttrunk100_198cm = 108

Air_density = 109




# aditional parameters:

nest_location = 0
oviposition_year = 1
oviposition_month = 2
oviposition_jul_day = 3
hatchling_svl = 4
maturity_svl = 5
from_clutch = 6
number_of_inherited_values = 7

# positions = [Tsoil_3cm, Tsoil_6cm, Tsoil_9cm, Tsoil_12cm, Tsoil25_3cm, Tsoil25_6cm, Tsoil25_9cm, Tsoil25_12cm, Tsoil50_3cm, Tsoil50_6cm, Tsoil50_9cm, Tsoil50_12cm, Tsoil75_3cm, Tsoil75_6cm, Tsoil75_9cm, Tsoil75_12cm, Tsoil100_3cm, Tsoil100_6cm, Tsoil100_9cm, Tsoil100_12cm]
positions_names = ['Tsoil_3cm,' 'Tsoil_6cm', 'Tsoil_9cm', 'Tsoil_12cm', 'Tsoil25_3cm', 'Tsoil25_6cm', 'Tsoil25_9cm', 'Tsoil25_12cm', 'Tsoil50_3cm', 'Tsoil50_6cm', 'Tsoil50_9cm', 'Tsoil50_12cm', 'Tsoil75_3cm', 'Tsoil75_6cm', 'Tsoil75_9cm', 'Tsoil75_12cm', 'Tsoil100_3cm', 'Tsoil100_6cm', 'Tsoil100_9cm', 'Tsoil100_12cm']
positions_shade = [0., 0., 0., 0., 25., 25., 25., 25., 50., 50., 50., 50., 75., 75., 75., 75., 100., 100., 100., 100.]
positions_depth = [3, 6, 9, 12, 3, 6, 9, 12, 3, 6, 9, 12, 3, 6, 9, 12]

ovipositions_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
decades = [8, 9]
num_of_non_layer_vars = 17
num_of_shade_levels = 5
num_of_layers_to_read = 4
num_of_inherited_nest_locations = 3
num_of_inherited_hatchling_svl = 3
num_of_inherited_maturity_svl = 3

sigma = 5.67*(10.**(-8))    #stefan-bolzman constant (w * m^-2 * k^-4)
zero_K = 273.15             # 0K = 273.15 Celsius

lean_mass_energetic_content = 17700     #(J/g) - Schmidt-Nielson book, page 171
decimal_percents_of_dry_mass = 0.25
fat_energetic_content = 39300   #(J/g) - Schmidt-Nielson book, page 171

# for Summary_module:

# to add a variable:
# 1) if this variable is a mean variable across time (e.g., climate)
#   a) add enums to both enums. preferbly at the beginning since both enums should have the same value.
#   b) add parameters in "main" package at the call to summary_step
#   c) update summary_step
# 2) if this variable is a lizards summary variable (e.g., energy gain)
#   a) add to the first enum - preferably at the end (before last)
#   b) update the clutch / lizard module to calculate the value of this variable and add to summary array
#   c) add to the Factory print statistics subroutine parameters

# at both cases: update the write netcdf_file names, units, and long_names arrays and make sure you update at
# the right index on the arrays according to the first enum!

enum_mean_temperature = 0
enum_mean_winter_temperature = 1
enum_mean_summer_temperature = 2
enum_sd_temperature = 3
enum_sd_winter_temperature = 4
enum_sd_summer_temperature = 5
enum_days_with_oviposition = 6       # from lizard_calib_module
enum_days_with_activity = 7          # from lizard_calib module
enum_min_julian_day_activity = 8     # from lizard_calib module
enum_max_julian_day_activity = 9     # from lizard_calib module
enum_hours_with_activity = 10        # from lizard_calib module
enum_energy_balance = 11             # from lizard_calib module
enum_growth_rate = 12                # from lizard_calib module
enum_activity_per_julian_day = 13
enum_last = 14

def get_array_index(arr, target_value):
    num_elements = len(arr)
    i = 0
    while i < num_elements:
        if arr[i] == target_value:
            return i
        i += 1
    return -1

#def get_position_index(m_position):
#    return get_array_index(positions, m_position)

def get_month_index(m_month):
    return get_array_index(ovipositions_months, m_month)

def get_decade_index(m_year):
    decade = (m_year % 100) / 10
    return get_array_index(decades, decade)
