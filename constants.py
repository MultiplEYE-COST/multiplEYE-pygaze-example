#!/usr/bin/env python
"""
This file will automatically be loaded by pygaze. We can define default values here that will automatically be used
More on what default values there are can be found in the pygaze git repo:
https://github.com/esdalmaijer/PyGaze/blob/master/pygaze/defaults.py
"""
import os

DUMMY_MODE = True
TRACKERTYPE = 'dummy'

# TRACKERTYPE = 'eyelink' # or whatever eye-tracker your using
# TRACKERTYPE = 'tobii'
# TRACKERSERIALNUMBER = 'TPFC2-010202524041'

# Display resolution in pixels as (width,height). Needs to be integers!
# NOTE that sometimes this is referred to as RESOLUTION in the pygaze code!
DISPSIZE = (1536, 864)

# Distance between the eye and the display in centimeters. Float.
SCREENDIST = 90.0

# Physical display size in centimeters as (width,height). Can be floats.
SCREENSIZE = (33.8, 27.1)

##############################################################################################################
# BELOW WE SPECIFY THOSE VARIABLES THAT ARE THE SAME ACROSS ALL LANGUAGES AND DEVICES; DO NOT CHANGE THESE ###
##############################################################################################################

RESULT_FOLDER_PATH = 'results'
DATA_ROOT_PATH = os.getcwd() + '/data/'

FULLSCREEN = True

# background color
BGC = (220, 220, 220)

# foreground color (i.e. font color)
FGC = (0, 0, 0)

DISPTYPE = 'psychopy'
FONT = 'Courier New'
FONT_SIZE = 22
