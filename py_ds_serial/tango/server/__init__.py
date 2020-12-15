# -*- coding: utf-8 -*-
#
# This file is part of the ALBA Python Serial DeviceServer project
#
# Copyright (c) 2020 Alberto López Sánchez
# Distributed under the GNU General Public License v3. See LICENSE for more info.

"""Tango server module for ALBA Python Serial DeviceServer."""

from .py_ds_serial import Py_ds_serial


def main():
    import sys
    import logging
    import tango.server
    args = ['Py_ds_serial'] + sys.argv[1:]
    fmt = '%(asctime)s %(threadName)s %(levelname)s %(name)s %(message)s'
    logging.basicConfig(level=logging.INFO, format=fmt)
    tango.server.run((Py_ds_serial,), args=args, green_mode=tango.GreenMode.Asyncio)
