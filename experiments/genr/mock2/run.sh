#!/bin/bash

# Define the absolute base path to the repository folder
mdtbDir="/Users/rmuetzel/OneDrive - Erasmus MC/software/MDTB"

#task
task=mock2

# 1. Activate the python virtual environment safely using quotes
source "${mdtbDir}/.venv/bin/activate"

# 2. Append both the root directory and inner directory to PYTHONPATH
# This prevents absolute/relative module import errors inside the tasks
export PYTHONPATH="${PYTHONPATH}:${mdtbDir}:${mdtbDir}/MultiTaskBattery"

# 3. Run the optimized experiment script (Fixed the typo from 'mdtnDir' to 'mdtbDir')
python3 "${mdtbDir}/MultiTaskBattery/experiments/genr/${task}/run.py"
