#!/bin/bash

#
# For SLURM
#
#SBATCH --nodes=1				#	Number of requested nodes per task
#SBATCH --account=ucb204_summit1		#	Account
#SBATCH --time=4-00:00:00				#	Max wall time
#SBATCH --qos=long				#	Specify QOS
#SBATCH --partition=shas		#	Specify Summit haswell nodes
#SBATCH --ntasks=1				#	Number of tasks per job
#SBATCH --job-name=spinup			#	Job submission name
#SBATCH --output=./sbatch_out_files/%x.%j.out	#	Output file name with Job ID
#SBATCH --mail-type=ALL
#SBATCH --mail-user=eric.keenan@colorado.edu
#SBATCH --array=1-100

#
# Check for job arrays:
#
if [ -n "${SLURM_ARRAY_TASK_ID}" ]; then
	command1=$(sed -n ${SLURM_ARRAY_TASK_ID}p to_exec.lst)
elif [ -n "${PBS_ARRAY_INDEX}" ]; then
	command1=$(sed -n ${PBS_ARRAY_INDEX}p to_exec.lst)
else
	command1=""
fi

#
# Execute job
#
if [ -n "${command1}" ]; then
	# Case using job arrays with a job manager
	eval ${command1}
	echo ${command1} >> finished.lst
else
	# Other cases
	bash to_exec.lst
fi
