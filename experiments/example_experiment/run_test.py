# Main Script for an example experiment
import sys
import MultiTaskBattery.experiment_block as exp_block
import constants as const

def main(subj_id):
    """ Main experiment function.
    Ensure the constants.py file is updated before running the experiment
    (e.g., experiment name, eye tracker, screen settings, etc.).

    Args:
        subj_id (str): Subject ID
    """
    my_Exp = exp_block.Experiment(const, subj_id=subj_id)
    my_Exp.run_filename = 'run_01.tsv'
    while True:
        my_Exp.confirm_run_info_genr()
        my_Exp.init_run_genr()
        my_Exp.run()
    return

if __name__ == "__main__":
    main('subject-00')
