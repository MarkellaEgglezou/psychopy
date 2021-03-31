#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Example of performing eye tracker validation using ioHub Common Eye Tracker interface
and the ValidationProcedure utility class.
"""
import time
from psychopy import visual
from psychopy.iohub import launchHubServer

from validationroutine import TargetStim, ValidationProcedure

if __name__ == "__main__":
    # Create a default PsychoPy Window
    # monitor *must* be the name of a valid PsychoPy Monitor config file.
    win = visual.Window((1920, 1080), fullscr=True, allowGUI=False, monitor='55w_60dist')

    exp_code = 'validation_demo'
    sess_code = 'S_{0}'.format(int(time.mktime(time.localtime())))

    # Create ioHub Server config settings....
    iohub_config = dict()
    iohub_config['experiment_code'] = exp_code
    iohub_config['session_code'] = sess_code
    # Add an eye tracker device
    et_interface_name = 'eyetracker.hw.mouse.EyeTracker'
    iohub_config[et_interface_name] = dict(name='tracker')

    # Start the ioHub process.
    io = launchHubServer(window=win, **iohub_config)

    # Get the keyboard and mouse devices for future access.
    keyboard = io.devices.keyboard
    tracker = io.devices.tracker
    experiment = io.devices.experiment

    # Run eyetracker calibration
    r = tracker.runSetupProcedure()

    # ValidationProcedure setup

    # Create a TargetStim instance
    target_stim = TargetStim(win, radius=0.025, fillcolor=[.5, .5, .5], edgecolor=[-1, -1, -1], edgewidth=2,
                        dotcolor=[1, -1, -1], dotradius=0.005, units='norm', colorspace='rgb')

    # target_positions: Provide your own list of validation positions,
    # or use the PositionGrid class to generate a set.
    target_positions = [(0.0, 0.0), (0.85, 0.85), (-0.85, 0.0), (0.85, 0.0), (0.85, -0.85), (-0.85, 0.85),
                 (-0.85, -0.85), (0.0, 0.85), (0.0, -0.85)]

    # Create a validation procedure
    validation_proc = ValidationProcedure(win,
                                          target=target_stim,
                                          positions=target_positions,
                                          target_animation_params=dict(velocity=1.0,
                                                                       expandedscale=3.0,
                                                                       expansionduration=0.2,
                                                                       contractionduration=0.4),
                                          accuracy_period_start=0.550,
                                          accuracy_period_stop=.150,
                                          show_intro_screen=True,
                                          intro_text='Validation procedure is now going to be performed.',
                                          show_results_screen=True,
                                          results_in_degrees=False,
                                          randomize_positions=False,
                                          toggle_gaze_cursor_key='g',
                                          terminate_key='escape')

    # Run the validation procedure. run() does not return until the validation is complete.
    validation_results =  validation_proc.run()

    io.quit()
