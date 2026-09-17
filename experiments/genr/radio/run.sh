#!/bin/bash

# 1. Source the central config file from the parent directory
source ../config.sh

# 2. Set task to the current folder name automatically (e.g., 'fmri')
task=$(basename "$PWD")

# 3. Activate the python virtual environment
source "${uvDir}/bin/activate"

# 4. Append directories to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${mdtbDir}:${mdtbDir}/MultiTaskBattery"

# 5. Run the experiment
python3 "${expDir}/${task}/run.py"
