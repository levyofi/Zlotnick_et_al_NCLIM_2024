import os as os
import pandas as pd

try:
    os.mkdir("deep_data//results_np_gb")
    os.mkdir("deep_data//results_np_gb//daytime_np_gb")
    os.mkdir("deep_data//results_np_gb//daytime_np_gb//seasons")
    
    os.mkdir("deep_data//results_np_gb//night_np_gb")
    os.mkdir("deep_data//results_np_gb//night_np_gb//seasons")

except FileExistsError:
    pass

# old files
mta_day_winter_file = open("deep_data//results_np//daytime_np//seasons//day_winter.csv", 'r')
mta_day_spring_file = open("deep_data//results_np//daytime_np//seasons//day_spring.csv", 'r')
mta_day_summer_file = open("deep_data//results_np//daytime_np//seasons//day_summer.csv", 'r')
mta_day_autumn_file = open("deep_data//results_np//daytime_np//seasons//day_autumn.csv", 'r')

mta_night_winter_file = open("deep_data//results_np//night_np//seasons//night_winter.csv", 'r')
mta_night_spring_file = open("deep_data//results_np//night_np//seasons//night_spring.csv", 'r')
mta_night_summer_file = open("deep_data//results_np//night_np//seasons//night_summer.csv", 'r')
mta_night_autumn_file = open("deep_data//results_np//night_np//seasons//night_autumn.csv", 'r')

# new files
gb_day_winter_file = open("deep_data//results_np_gb//daytime_np_gb//seasons//day_winter.csv", 'w')
gb_day_spring_file = open("deep_data//results_np_gb//daytime_np_gb//seasons//day_spring.csv", 'w')
gb_day_summer_file = open("deep_data//results_np_gb//daytime_np_gb//seasons//day_summer.csv", 'w')
gb_day_autumn_file = open("deep_data//results_np_gb//daytime_np_gb//seasons//day_autumn.csv", 'w')

gb_night_winter_file = open("deep_data//results_np_gb//night_np_gb//seasons//night_winter.csv", 'w')
gb_night_spring_file = open("deep_data//results_np_gb//night_np_gb//seasons//night_spring.csv", 'w')
gb_night_summer_file = open("deep_data//results_np_gb//night_np_gb//seasons//night_summer.csv", 'w')
gb_night_autumn_file = open("deep_data//results_np_gb//night_np_gb//seasons//night_autumn.csv", 'w')

day_names = ["id", "time", "julian_day", "hour", "burrow", "open", "shade", "open_tree", "shaded_tree", "ess_open_tree", "ess_shaded_tree", "season", "pod", "mta"]
night_names = ["id", "time", "julian_day", "hour", "burrow", "shade", "mta"]

mta_day_winter_df = pd.read_csv("deep_data//results_np//daytime_np//seasons//day_winter.csv", index_col = False)
mta_day_winter_df.astype({'julian_day' : 'int32', 'burrow' : 'float', 'open' : 'float', 'shade' : 'float', 'open_tree' : 'float', 'shaded_tree' : 'float', 'ess_open_tree' : 'float', 'ess_shaded_tree' : 'float'})
gb_day_winter_df = mta_day_winter_df.groupby(["id", "time", "julian_day", "pod", "mean_ta"]).agg({'burrow' : 'mean', 'open' : 'mean', 'shade' : 'mean', 'open_tree' : 'mean', 'shaded_tree' : 'mean', 'ess_open_tree' : 'mean', 'ess_shaded_tree' : 'mean'})
gb_day_winter_df = gb_day_winter_df.reset_index()
gb_day_winter_df.to_csv("deep_data//results_np_gb//daytime_np_gb//seasons//day_winter.csv")

mta_day_spring_df = pd.read_csv("deep_data//results_np//daytime_np//seasons//day_spring.csv", index_col = False)
mta_day_spring_df.astype({'julian_day' : 'int32', 'burrow' : 'float', 'open' : 'float', 'shade' : 'float', 'open_tree' : 'float', 'shaded_tree' : 'float', 'ess_open_tree' : 'float', 'ess_shaded_tree' : 'float'})
gb_day_spring_df = mta_day_spring_df.groupby(["id", "time", "julian_day", "pod", "mean_ta"]).agg({'burrow' : 'mean', 'open' : 'mean', 'shade' : 'mean', 'open_tree' : 'mean', 'shaded_tree' : 'mean', 'ess_open_tree' : 'mean', 'ess_shaded_tree' : 'mean'})
gb_day_spring_df = gb_day_spring_df.reset_index()
gb_day_spring_df.to_csv("deep_data//results_np_gb//daytime_np_gb//seasons//day_spring.csv")

mta_day_summer_df = pd.read_csv("deep_data//results_np//daytime_np//seasons//day_summer.csv", index_col = False)
mta_day_summer_df.astype({'julian_day' : 'int32', 'burrow' : 'float', 'open' : 'float', 'shade' : 'float', 'open_tree' : 'float', 'shaded_tree' : 'float', 'ess_open_tree' : 'float', 'ess_shaded_tree' : 'float'})
gb_day_summer_df = mta_day_summer_df.groupby(["id", "time", "julian_day", "pod", "mean_ta"]).agg({'burrow' : 'mean', 'open' : 'mean', 'shade' : 'mean', 'open_tree' : 'mean', 'shaded_tree' : 'mean', 'ess_open_tree' : 'mean', 'ess_shaded_tree' : 'mean'})
gb_day_summer_df = gb_day_summer_df.reset_index()
gb_day_summer_df.to_csv("deep_data//results_np_gb//daytime_np_gb//seasons//day_summer.csv")

mta_day_autumn_df = pd.read_csv("deep_data//results_np//daytime_np//seasons//day_autumn.csv", index_col = False)
mta_day_autumn_df.astype({'julian_day' : 'int32', 'burrow' : 'float', 'open' : 'float', 'shade' : 'float', 'open_tree' : 'float', 'shaded_tree' : 'float', 'ess_open_tree' : 'float', 'ess_shaded_tree' : 'float'})
gb_day_autumn_df = mta_day_autumn_df.groupby(["id", "time", "julian_day", "pod", "mean_ta"]).agg({'burrow' : 'mean', 'open' : 'mean', 'shade' : 'mean', 'open_tree' : 'mean', 'shaded_tree' : 'mean', 'ess_open_tree' : 'mean', 'ess_shaded_tree' : 'mean'})
gb_day_autumn_df = gb_day_autumn_df.reset_index()
gb_day_autumn_df.to_csv("deep_data//results_np_gb//daytime_np_gb//seasons//day_autumn.csv")

#night
mta_night_winter_df = pd.read_csv("deep_data//results_np//night_np//seasons//night_winter.csv", index_col = False)
mta_night_winter_df.astype({'julian_day' : 'int32', 'burrow' : 'float', 'shade' : 'float'})
gb_night_winter_df = mta_night_winter_df.groupby(["id", "time", "julian_day", "mean_ta"]).agg({'burrow' : 'mean', 'shade' : 'mean'})
gb_night_winter_df = gb_night_winter_df.reset_index()
gb_night_winter_df.to_csv("deep_data//results_np_gb//night_np_gb//seasons//night_winter.csv")

mta_night_spring_df = pd.read_csv("deep_data//results_np//night_np//seasons//night_spring.csv", index_col = False)
mta_night_spring_df.astype({'julian_day' : 'int32', 'burrow' : 'float', 'shade' : 'float'})
gb_night_spring_df = mta_night_spring_df.groupby(["id", "time", "julian_day", "mean_ta"]).agg({'burrow' : 'mean', 'shade' : 'mean'})
gb_night_spring_df = gb_night_spring_df.reset_index()
gb_night_spring_df.to_csv("deep_data//results_np_gb//night_np_gb//seasons//night_spring.csv")

mta_night_summer_df = pd.read_csv("deep_data//results_np//night_np//seasons//night_summer.csv", index_col = False)
mta_night_summer_df.astype({'julian_day' : 'int32', 'burrow' : 'float', 'shade' : 'float'})
gb_night_summer_df = mta_night_summer_df.groupby(["id", "time", "julian_day", "mean_ta"]).agg({'burrow' : 'mean', 'shade' : 'mean'})
gb_night_summer_df = gb_night_summer_df.reset_index()
gb_night_summer_df.to_csv("deep_data//results_np_gb//night_np_gb//seasons//night_summer.csv")

mta_night_autumn_df = pd.read_csv("deep_data//results_np//night_np//seasons//night_autumn.csv", index_col = False)
mta_night_autumn_df.astype({'julian_day' : 'int32', 'burrow' : 'float', 'shade' : 'float'})
gb_night_autumn_df = mta_night_autumn_df.groupby(["id", "time", "julian_day", "mean_ta"]).agg({'burrow' : 'mean', 'shade' : 'mean'})
gb_night_autumn_df = gb_night_autumn_df.reset_index()
gb_night_autumn_df.to_csv("deep_data//results_np_gb//night_np_gb//seasons//night_autumn.csv")




# old files
mta_day_winter_file.close()
mta_day_spring_file.close()
mta_day_summer_file.close()
mta_day_autumn_file.close()

mta_night_winter_file.close()
mta_night_spring_file.close()
mta_night_summer_file.close()
mta_night_autumn_file.close()

# new files
gb_day_winter_file.close()
gb_day_spring_file.close()
gb_day_summer_file.close()
gb_day_autumn_file.close()

gb_night_winter_file.close()
gb_night_spring_file.close()
gb_night_summer_file.close()
gb_night_autumn_file.close()












