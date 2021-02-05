# -*- coding: utf-8 -*-
#
# This file is part of the Meadowlark D5020 project
#
# Copyright (c) 2021 Alberto López Sánchez
# Distributed under the GNU General Public License v3. See LICENSE for more info.

"""
.. code-block:: yaml

    devices:
    - class: serial
      package: tangods_serialline.simulator
      transports:
        - type: serial
        url: /tmp/meadowlark_d5020
A simple *nc* client can be used to connect to the instrument:

    $ nc 0 5000
    *IDN?
    GE,Pace5000,204683,1.01A
"""

from sinstruments.simulator import BaseDevice


class SerialEcho(BaseDevice):

    def handle_message(self, line):
        print("RECV:", line)

        pass
