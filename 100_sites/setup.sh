#!/bin/bash

# Load modules
module purge
ml intel; ml proj; ml netcdf

# Load conda environment
source /projects/erke2265/miniconda/etc/profile.d/conda.sh
conda activate alpine3d

# Clear old data
rm smet/*
rm log/*
rm sbatch_out_files/*
rm output/*
rm current_snow/*
rm to_exec.lst
rm finished.lst

# Make sub-directories if they don't already exist
mkdir -p smet
mkdir -p log
mkdir -p profiles
mkdir -p sbatch_out_files
mkdir -p output

# Collect 100 random sites
ls /pl/active/icesheetsclimate/IDS_Antarctica/smet | sort -R | tail -100 | while read file; do
    cp /pl/active/icesheetsclimate/IDS_Antarctica/smet/${file} smet/ # Copy smet file
    python3 get_RF_ratio.py smet/${file} # Add RF ratio to smet file
done

# Initialize SNOWPACK
bash run_snowpack.sh

# Submit job
sbatch job.sbatch
