#!/bin/bash
#SBATCH -p v4_256
#SBATCH -N 1
#SBATCH -n 32 
export PATH=/public1/home/pg2102/software/vasp.5.4.4/bin:$PATH
module load intel/18.0.2
module load mpi/intel/18.0.2 
srun vasp_std
