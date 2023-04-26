#!/usr/bin/env python
"""
This experiment class contains all necessary functions that we typically have to run an eye-tracking experiment.
It is not necessary to have such a class when working with PyGaze but it just makes things a bit easier.

Note that it is not a proper experiment and does not follow the typical experiment structure. It is just to show how
PyGaze works.

All of the PyGaze classes that we use in here then use the constants file and the values that we specified in there.
For example: we specified that the display type is 'psychopy' and the resolution is 1536x864. This is then used by the
Display class to set up the display.
"""
from __future__ import annotations

from pygaze.eyetracker import EyeTracker

import constants
from psychopy.monitors import Monitor
from pygaze import libtime
from pygaze.libinput import Keyboard
from pygaze.liblog import Logfile
from pygaze.libscreen import Display, Screen
from pygaze.libtime import get_time


class Experiment:
    # in order to work with PyGaze we need to set up a Display object
    # PyGaze docs: http://www.pygaze.org/documentation/libscreen/#Display
    _display: Display = Display(
        monitor=Monitor('myMonitor', width=53.0, distance=constants.SCREENDIST),
    )

    # we also need a Keyboard object to get input from the keyboard
    # we have the option to set the keys that we want to 'listen' to. It will only register those key that we specify
    # PyGaze docs: http://www.pygaze.org/documentation/libinput/#Keyboard
    _keyboard: Keyboard = Keyboard(
        keylist=['space', 'a', 'b', 'c'],
    )

    def __init__(
            self,
            welcome_screen_path: str,
            example_stimulus_text: str,
            date: str,
            participant_id: int,
            experiment_start_timestamp: int,
            exp_path: str,
    ):
        self.welcome_screen_path = welcome_screen_path
        self.example_stimulus_text = example_stimulus_text

        # Set up the EyeTracker object, we pass the display that we specified before
        # PyGaze docs: http://www.pygaze.org/documentation/eyetracker/#EyeTracker
        self._eye_tracker = EyeTracker(
            self._display,
            eyedatafile='eyedatafile',
            logfile='logfile',
        )

        # We set up another log fiel here to store additional information during the experiment
        self.log_file = Logfile(
            filename=f'{exp_path}/'
                     f'EXPERIMENT_LOGFILE_{participant_id}_{date}_{experiment_start_timestamp}',
        )

        self.log_file.write(
            [
                'timestamp', 'stimulus_timestamp',
                'keypress_timestamp', 'key_pressed', 'message',
            ]
        )

    def calibrate(self):
        # in dummy mode this line does not do anything
        # as soon as we have an actual eye-tracker connected it will start the calibration and validation
        self._eye_tracker.calibrate()

    def show_welcome_screen(self, milliseconds: int = 3000) -> None:
        # in order to show an image we first create a screen object
        # PyGaze docs: http://www.pygaze.org/documentation/libscreen/#Screen
        image_screen = Screen()

        # we need to explicitly draw something on the screen
        image_screen.draw_image(image=self.welcome_screen_path)

        # then we can add the screen to our display, note that it is not shown yet!
        self._display.fill(image_screen)

        # only when we call show on the display the screen will be shown
        self._display.show()

        # it is possible to add breaks once we show a screen
        # it does not change the screen content, but it just waits until the program proceeds
        libtime.pause(milliseconds)

    def run_experiment(self) -> None:
        # we want to show a text on our screen using the draw_text function
        # you can play around with this function and add some more parameters as found in the docs
        # http://www.pygaze.org/documentation/libscreen/#Screen.draw_text
        stimulus_screen = Screen()
        stimulus_screen.draw_text(
            text="This is a stimulus. The experiment will continue automatically. You don't have to press anything.",
            fontsize=constants.FONT_SIZE,
            font=constants.FONT,
        )

        # we first need to fill the display with the screen we specified and then show it
        self._display.fill(stimulus_screen)
        self._display.show()

        # it is possible to add breaks once we show a screen
        # it does not change the screen content, but it just waits until the program proceeds
        # this way we can show a screen for a specific amount of time
        milliseconds = 3000
        libtime.pause(milliseconds)

        # after the short break we can clear the screen and show it again on the display
        stimulus_screen.clear()
        self._display.fill(stimulus_screen)
        self._display.show()

        milliseconds = 3000
        libtime.pause(milliseconds)

        # what is really important is to add status messages and other messages to the eye-tracker log file
        # this is not the file that we specified earlier but one that is automatically written by the eye-tracker
        self._eye_tracker.status_msg(f'we have shown one stimulus screen')
        self._eye_tracker.log(f'stimulus screen 1 showing sentence "{self.example_stimulus_text}"')

        # but we can also write things to our own logfile
        self.log_file.write(
            [
                get_time(), '',
                '', '', f'showing stimulus "{self.example_stimulus_text}"',
            ],
        )

        # now we want to show the stimulus but actually record the eye-movements
        self._eye_tracker.start_recording()
        self._eye_tracker.status_msg(f'tracking eye movements for stimulus {self.example_stimulus_text}')
        self._eye_tracker.log(f'tracking eye movements for stimulus {self.example_stimulus_text}')

        # now we draw the text that we specified earlier
        stimulus_screen.draw_text(
            text=self.example_stimulus_text,
            fontsize=constants.FONT_SIZE,
        )

        self._display.fill(screen=stimulus_screen)

        # instead of just calling the function we assign it to a variable which gives us the timestamp
        stimulus_timestamp = self._display.show()

        # this time we want participants to press 'space' to continue which can be done with the keyboard object
        key_pressed_stimulus = ''
        keypress_timestamp = -1

        while key_pressed_stimulus not in ['space']:
            key_pressed_stimulus, keypress_timestamp = self._keyboard.get_key(flush=True)

        # now we can write all of that to the logfile again
        self.log_file.write(
            [
                get_time(), stimulus_timestamp,
                keypress_timestamp, key_pressed_stimulus, f'showing stimulus "{self.example_stimulus_text}"',
            ],
        )

        # stop eye tracking
        self._eye_tracker.stop_recording()
        self._eye_tracker.log(f'stop recording of "{self.example_stimulus_text}"')

        # we can also adapt the screen objects
        # for example: here we overwrite the default background color
        color_screen = Screen(bgc=(45, 45, 150))
        color_screen.draw_text("Press 'space', 'a', 'b' or 'c' to continue.", fontsize=constants.FONT_SIZE)

        self._display.fill(color_screen)
        self._display.show()

        # TODO: add more screens here that you then show. E.g. you can show a fixation cross on a screen.
        #  http://www.pygaze.org/documentation/libscreen/#Screen.draw_fixation

        # we again will only proceed if the participant presses a key, this time it can be any key that we specified
        # in the beginning
        self._keyboard.get_key()

        # we can also do a drift correction
        # Note that you need to hover with your mouse over the fixation target to trigger the drift correction and
        # then press space (in dummy mode)!
        self._eye_tracker.drift_correction()

        # end the experiment
        # we need to close all the logfiles, the eyetracker connection and the display
        self.log_file.close()
        self._eye_tracker.close()
        self._display.close()
        libtime.expend()
