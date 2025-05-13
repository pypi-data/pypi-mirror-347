# -*- coding: utf-8 -*-
"""
Created by chiesa

Copyright Alpes Lasers SA, Switzerland
"""
__author__ = 'chiesa'
__copyright__ = "Copyright Alpes Lasers SA"

import itertools
import os
from argparse import ArgumentParser
from datetime import datetime
from time import sleep
from copy import deepcopy

import requests

from glider_client.commands import SteppingPoiDataset, STEPPING_POI_S2_TRIGGER_MODE_INT_CONTINUOUS
from glider_client.glider import Glider
from glider_client.scripts.stepping_poi_plot import stepping_poi_plot
from glider_client.utils.alparser import _positive_float, _positive_int, _strict_positive_int
from glider_client.utils.mcu_registers import ADC_SAMPLING_TIMES
from glider_client.utils.ping import ping
from glider_client.utils.ssrv import store_stepping_poi


def run():

    glider_client = Glider(hostname='localhost',
                           port=5000)
    glider_status = glider_client.get_status()
    glider_client.initialize()

    wavenumbers = []

    for cp in glider_status.config.profiles[1].cavityProfiles.values():
        wavenumbers.append(min(cp.calibWnInvCm) + 1)
        wavenumbers.append(max(cp.calibWnInvCm) - 1)


    poi_list = [{'wavenumber': x,
                 'laserDwellMs': 0,
                 'postDwellMs': 0,
                 'numberOfPulses': 10,
                 'analog1PGA': 4,
                 'analog2PGA': 4,
                 } for x in sorted(wavenumbers)]

    use_analog1 = True
    use_analog2 = True

    parameters = {'poi': poi_list,
                  'tuned_window_invcm': 1,
                  'stable_time_in_poi_ms': 1,
                  'use_analog1': use_analog1,
                  'use_analog2': use_analog2,
                  'analog1_delay_s2m_trigger_ns': 200,
                  'analog1_oversampling': 3,
                  'analog1_oversampling_shift': 2,
                  'analog1_sampling_time_ns': 9,
                  'analog2_delay_s2m_trigger_ns': 200,
                  'analog2_oversampling': 3,
                  'analog2_oversampling_shift': 2,
                  'analog2_sampling_time_ns': 9,
                  's2_trigger_mode': STEPPING_POI_S2_TRIGGER_MODE_INT_CONTINUOUS,
                  }
    while True:
        command_proxy = glider_client.execute_command(SteppingPoiDataset(**parameters))

if __name__ == '__main__':
    run()
