# Main Script for an example experiment
import sys
import MultiTaskBattery.experiment_block as exp_block
import constants as const
import os
import MultiTaskBattery.utils as ut
import MultiTaskBattery.task_file as tf
from pathlib import Path
from psychopy import gui


#audio issues RLM
os.environ["PSYCHOPY_AUDIO_LIB"] = "sounddevice"
import sys
from unittest.mock import MagicMock

# Intercept PsychoPy before it can load the broken Psychtoolbox library
sys.modules['psychopy.sound.backend_ptb'] = MagicMock()

# Explicitly set sounddevice as the preferred backup choice
from psychopy import prefs
prefs.hardware['audioLib'] = ['sounddevice']



task_dir = ''
def main(subj_id):
    """ Main experiment function.
    Ensure the constants.py file is updated before running the experiment
    (e.g., experiment name, eye tracker, screen settings, etc.).

    Args:
        subj_id (str): Subject ID
    """
    my_Exp = exp_block.Experiment(const, subj_id=subj_id)
    pause_dialog = gui.Dlg(title="Pause")
    # Add a text message (optional)
    pause_dialog.addText("Press OK to continue...")

    while True:
        #my_Exp.confirm_run_info()
        my_Exp.confirm_run_info_genr()
        my_Exp.run_filename = 'run_01.tsv'
        my_Exp.const.task_dir = Path(os.path.join(my_Exp.const.exp_dir, 'output', 'task_files'))
        print(my_Exp.run_number)
        print(my_Exp.run_filename)
        subj_dir = os.path.join(const.exp_dir, 'output', my_Exp.subj_id)
        const.run_dir = Path(os.path.join(subj_dir, 'run_files'))
        tasks = ['finger_sequence', 'n_back', 'demand_grid', 'auditory_narrative', 'affective', 'action_observation', 'movie', 'rest']
        num_runs = 3  # Number of imaging runs
        # Ensure task and run directories exist
        ut.dircheck(const.run_dir)
        # Generate run and task files
        for r in range(1, num_runs+1):
            tfiles = [f'{task}_{r:02d}.tsv' for task in tasks]
            T = tf.make_run_file(tasks, tfiles)
            T.to_csv(os.path.join(const.run_dir, f'run_{r:02d}.tsv'), sep='\t', index=False)
        my_Exp.init_run_genr()
        const.data_dir = const.exp_dir / 'output'
        my_Exp.run()
        print('scanning paused for prep scans')
        pause_dialog.show()
        if not pause_dialog.OK:
            print('user indicated prep scans complete')
            core.quit()
        my_Exp.run_number = 2
        my_Exp.run_filename = 'run_02.tsv'
        my_Exp.init_run_genr()
        my_Exp.run()
        print('scanning paused for prep scans')
        pause_dialog.show()
        if not pause_dialog.OK:
            print('user indicated prep scans complete')
            core.quit()
        my_Exp.run_number = 3
        my_Exp.run_filename = 'run_03.tsv'
        my_Exp.init_run_genr()
        my_Exp.run()
    return

if __name__ == "__main__":
    main('subject-00')
