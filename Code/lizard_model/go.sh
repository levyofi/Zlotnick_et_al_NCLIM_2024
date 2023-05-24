#!/bin/bash

#PBS -e output.err
#PBS -o output.log
##PBS -l walltime=240:00:00
#PBS -l nodes=compute-0-330:ppn=36
##PBS -l select=1:ncpus=36:mpiprocs=36:host=compute-0-329+1:ncpus=36:mpiprocs=36:host=compute-0-331
##PBS -l select=2:ncpus=72:mpiprocs=72
#PBS -M omerzlotnick@mail.tau.ac.il
#PBS -q levyofir

##qsub -I -l select=1:ncpus=36:mpiprocs=36:host=compute-0-330+1:ncpus=36:mpiprocs=36:host=compute-0-328 -q levyofir

module load python/python-anaconda_3.7
module load intel/parallel_studio_xe_2018
#module load intel/parallel_studio_xe_2020.0
#source /powerapps/share/intel/l_mkl_2020.0.166/bin/iccvars.sh -arch intel64 -platform linux
#source /powerapps/share/intel/l_mkl_2020.0.166/parallel_studio_xe_2020.0.088/bin/psxevars.sh
source activate trunk
export MPICC=$(which mpicc)
export PYTHONPATH=""
cd /ofir/omer/final_model/final_model/Main
mpiexec -np 36 python -m mpi4py __init__.py -a 0 -b 0

##qsub go.sh
##qstat | grep id q levyofir
