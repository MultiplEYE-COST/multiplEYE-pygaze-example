#!/usr/bin/env python
"""
This file is used to start the experiment and triggers all actions that we execute during the experiment.
"""

from __future__ import annotations

import datetime
import os

import constants
from experiment import Experiment
from pygaze.libtime import get_time
from pygaze.logfile import Logfile


def run_experiment(
        welcome_screen_path: str,
        example_stimulus_text: str,
        participant_id: int,
        date: str,

) -> None:

    exp_path = f'{constants.RESULT_FOLDER_PATH}/{participant_id}'

    # we want to write some results and therefore create a result folder with the participant ID
    if not os.path.isdir(exp_path):
        os.makedirs(exp_path)

    # it is always helpful to have timestamps of important events in the logfile
    experiment_start_timestamp = int(datetime.datetime.now().timestamp())

    # PyGaze has a Logfile class that can be used to write to a logfile
    general_log_file = Logfile(
        filename=f'{exp_path}/'
                 f'GENERAL_LOGFILE_{participant_id}_{date}_{experiment_start_timestamp}',
    )

    # we just write the header of the logfile
    general_log_file.write(['timestamp', 'message'])

    # PyGaze has a time module included. We can use it to get the time from the experiment start!
    # As soon as pygaze is imported, the time starts counting from 0. It is not the same as the experiment start time
    # which is the actual time!
    # the get_time() function returns the time from the start in milliseconds
    general_log_file.write(
        [get_time(), f'EXP_START_TIMESTAMP_{experiment_start_timestamp}'],
    )
    general_log_file.write([get_time(), f'PARTICIPANT_ID_{participant_id}'])

    general_log_file.write([get_time(), 'START'])

    # we create our experiment class initialized with all the information we got
    experiment = Experiment(
        welcome_screen_path=welcome_screen_path,
        example_stimulus_text=example_stimulus_text,
        date=date,
        participant_id=participant_id,
        experiment_start_timestamp=experiment_start_timestamp,
        exp_path=exp_path,
    )

    # Whenever we call a function in this file we can write a message to the logfile
    general_log_file.write([get_time(), 'show welcome screen'])
    # as we have configured a welcome screen we can show it now for a specified time
    experiment.show_welcome_screen(milliseconds=4000)

    # note that if we are in dummy mode the calibration will not be executed! As soon as we have an eye-tracker and
    # change the settings in the constants file, the calibration will be executed
    experiment.calibrate()

    # now we actually run the experiment where we also include eye-tracking
    general_log_file.write([get_time(), 'start experiment'])
    experiment.run_experiment()
    general_log_file.write([get_time(), 'finished experiment'])

    general_log_file.write([get_time(), 'END'])

    # IMPORTANT: close the logfile
    general_log_file.close()


if __name__ == '__main__':

    # Typically we would have some command line arguments here to provide e.g. data files or information on the exp
    # We skip this for now and hardcode all the parameters here

    # add a path to an image that we later want to show
    welcome_screen_path = 'data/welcome_screen.png'

    # We provide a stimulus text here that we want to show on the screen. We could also read it from a file.
    example_stimulus_text = "This is an example stimulus. We can easily show text on the screen with PyGaze. " \
                            "We can change the font, the size and other settings.\n\n" \
                            "Press space to continue."

    # Very important, in an actual experiment we need to specify the participant id and typically also a session ID
    participant_ID = 12

    today = str(datetime.date.today())

    run_experiment(welcome_screen_path, example_stimulus_text, participant_ID, today)
