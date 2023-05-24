import sys
sys.path.append("../")

from Summary import Summary
from Lizard import Lizard
from Lizard_climbing import Lizard_climbing
from Lizard_climbing_13 import Lizard_climbing_13
from Lizard_energy import Lizard_energy
from Climate import Climate
from Day_summary import Day_summary
import Parameters as p
import numpy as np
import time
from mpi4py import MPI
import argparse

import random

def get_input_files(num_of_proc):
    input_names_past = open("../past_climate_files.txt", 'r')
    input_names_future = open("../future_climate_files.txt", 'r')

    input_names_past_lst = input_names_past.readlines()
    input_names_future_lst = input_names_future.readlines()

    num_of_coor = len(input_names_past_lst)
    
    lst = [input_names_past_lst, input_names_future_lst]
    input_files_mat = [ [] for k in range(num_of_proc)]

    for j in range(num_of_proc):
        for curr_lst in lst:
            for inputfilename in curr_lst:
                i = curr_lst.index(inputfilename) 
                
                mod = i % num_of_proc
                if mod == j:
                    input_files_mat[j].append(inputfilename.strip())
    
    return input_files_mat, num_of_coor

# for sensitivity analysis    
ap = argparse.ArgumentParser()

ap.add_argument("-a", "--var", required = True, help = "variable")
ap.add_argument("-b", "--change", required = True, help = "change rate")

args = vars(ap.parse_args())
var = str(args['var'])
change = float(args['change'])

# start running
start_time = time.time()

# print("split file names to processes...")
num_of_proc = 120
input_files_mat, num_of_coor = get_input_files(num_of_proc)


comm = MPI.COMM_WORLD
        
rank = comm.Get_rank()
process_lst = input_files_mat[rank]
"""
if rank == 0:
    import os
    try:
        os.makedirs("climbing_info_files")

    except OSError:
        print("directory was created earlier, model keeps running...")
        pass
"""
print("process " + str(rank) + " is running...")
process_summary_mat = []



for inputfilename in process_lst:
    climate = Climate()
    climate.load_data(inputfilename)

    nc_lizard = Lizard_energy()
    c_lizard = Lizard_climbing_13()
    
    # for sensitivity analysis
    nc_lizard.sensitivity_analysis(var, change)
    c_lizard.sensitivity_analysis(var, change)

    # for check
    print("mass of nc lizard: " + str(nc_lizard.mass))
    print("mass of c lizard: " + str(c_lizard.mass))
    print("emergence_min_To of nc lizard: " + str(nc_lizard.emergence_min_To))
    print("emergence_min_To c lizard: " + str(c_lizard.emergence_min_To))
    print("Vtmin of nc lizard: " + str(nc_lizard.Vtmin))
    print("Vtmin of c lizard: " + str(c_lizard.Vtmin))
    print("Vtmax of nc lizard: " + str(nc_lizard.Vtmax))
    print("Vtmax of c lizard: " + str(c_lizard.Vtmax))
    print("alpha_L_direct of nc lizard: " + str(nc_lizard.alpha_L_direct))
    print("alpha_L_direct of c lizard: " + str(c_lizard.alpha_L_direct))
    print("alpha_L_scattered of nc lizard: " + str(nc_lizard.alpha_L_scattered))
    print("alpha_L_scattered of c lizard: " + str(c_lizard.alpha_L_scattered))
    print("ground_insect_abundance of nc lizard: " + str(nc_lizard.ground_insect_abundance))
    print("ground_insect_abundance of c lizard: " + str(c_lizard.ground_insect_abundance))
    print("tree_insect_abundance of c lizard: " + str(c_lizard.tree_insect_abundance))

    for time_step in range(climate.number_of_steps):	
        nc_lizard.step(climate.current_climate, climate.time_step)	#
        c_lizard.step(climate.current_climate, climate.time_step)	#
        climate.step()

    nc_summary = Summary(climate, nc_lizard)
    nc_sum = nc_summary.calculate_statistics()
    process_summary_mat.append(nc_sum)

    c_summary = Summary(climate, c_lizard)
    c_sum = c_summary.calculate_statistics()
    process_summary_mat.append(c_sum)

    print(inputfilename + " is done!")

process_summary_mat_a = np.array(process_summary_mat).flatten()



num_of_parameters = 29

#print("building 'all_sums'...")
if rank == 0:
    all_sums = np.zeros((num_of_coor * 4 * num_of_parameters), dtype = np.float64)
    #all_sums = np.zeros((12), dtype = np.float64)
    # create directory - use only in the beginning of new run!
    
else:
    all_sums = None


#print("calculating displacments...")
rdispls = [0]
for proc in range(1,num_of_proc):
    rdispls.append(rdispls[proc-1] + (len(input_files_mat[proc-1]) * 2 * num_of_parameters))

counts = []
for proc in range(num_of_proc):
    counts.append(len(input_files_mat[proc]) * 2 * num_of_parameters)

rdispls = tuple(rdispls)
#print(rdispls)
counts = tuple(counts)
#print(counts)

print("working on gatherv!")
sendbuf = [process_summary_mat_a, counts[rank]]
recvbuf = [all_sums, counts, rdispls, MPI.DOUBLE]
comm.Gatherv(process_summary_mat_a, recvbuf, root = 0)
comm.Barrier()

if rank == 0:
    nrows = len(all_sums) // num_of_parameters
    #print(nrows)
    all_sums = all_sums.reshape((nrows, num_of_parameters))
    #print(all_sums)

    file_name = "sums_" + str(var) + "_" + str(change) + ".csv"

    print("exporting to file...")
    out = open(file_name, 'w')
    for row in all_sums:
        for column in row:
            out.write(str(column) + ',')
        out.write('\n')
    out.close()



# running time calculation
running_time = time.time() - start_time     # in seconds
hours = running_time // 3600
minutes = (running_time % 3600) // 60
seconds = (running_time % 60)
print("Running time: " + str(hours) + " hours, " + str(minutes) + " minutes, " + str(seconds) + " seconds")




