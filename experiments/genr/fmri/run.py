import sys
import os
import datetime
from pathlib import Path
from unittest.mock import MagicMock

os.environ["PSYCHOPY_AUDIO_LIB"] = "sounddevice"
sys.modules['psychopy.sound.backend_ptb'] = MagicMock()

from psychopy import prefs, gui, core
prefs.hardware['audioLib'] = ['sounddevice']

import MultiTaskBattery.experiment_block as exp_block
import constants as const
import MultiTaskBattery.utils as ut
import MultiTaskBattery.task_file as tf


def main(subj_id):
    """ Main experiment function.
    Ensure the constants.py file is updated before running the experiment
    (e.g., experiment name, eye tracker, screen settings, etc.).

    Args:
        subj_id (str): Subject ID
    """
    # Generate a single session timestamp for this behavioral/scanning block
    session_timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Initialize Experiment, explicitly passing the timestamp down
    my_Exp = exp_block.Experiment(const, subj_id=subj_id, session_timestamp=session_timestamp)
    
    # Consolidate standard configuration paths using pure Pathlib syntax
    output_base = Path(my_Exp.const.exp_dir) / 'output'
    my_Exp.const.task_dir = output_base / 'task_files'
    const.data_dir = output_base
    
    # This run_dir matches the new subfolder architecture inside experiment_block
    const.run_dir = output_base / my_Exp.subj_id / session_timestamp / 'run_files'
    ut.dircheck(const.run_dir)

    # Experiment Configuration parameters
    tasks = ['finger_sequence', 'n_back', 'demand_grid', 'auditory_narrative', 'affective', 'action_observation', 'movie', 'rest']
    num_runs = 3  # Set this to change total target imaging runs seamlessly
    
    # Pre-generate task matrix run schedules for this session block
    for r in range(1, num_runs + 1):
        tfiles = [f'{task}_{r:02d}.tsv' for task in tasks]
        T = tf.make_run_file(tasks, tfiles)
        T.to_csv(const.run_dir / f'run_{r:02d}.tsv', sep='\t', index=False)
        
    # Open GUI input interface to capture participant details
    my_Exp.confirm_run_info_genr()
    
    # Setup standard pause window infrastructure for scanner intervals
    pause_dialog = gui.Dlg(title="Pause")
    pause_dialog.addText("Prep scans in progress. Press OK to continue...")

    # Consolidated, dynamic run execution block
    for run_idx in range(1, num_runs + 1):
        print(f"\n--- Initializing Imaging Run {run_idx:02d} ---")
        
        # Update experiment tracker settings dynamically
        my_Exp.run_number = run_idx
        my_Exp.run_filename = f'run_{run_idx:02d}.tsv'
        
        # Initialize paths and execute the active multi-task trial list
        my_Exp.init_run_genr()
        my_Exp.run()
        
        # Hold execution between functional scans, omitting after the final block
        if run_idx < num_runs:
            print('Scanning paused for anatomical/prep scan intervals.')
            pause_dialog.show()
            
            if not pause_dialog.OK:
                print('Session execution aborted manually by operator.')
                core.quit()
                sys.exit(0)

    print("\nExperiment execution cycle complete.")
    return


if __name__ == "__main__":
    main('R')
