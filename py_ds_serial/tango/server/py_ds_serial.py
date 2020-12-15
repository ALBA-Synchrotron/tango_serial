# -*- coding: utf-8 -*-
#
# This file is part of the ALBA Python Serial DeviceServer project
#
# Copyright (c) 2020 Alberto López Sánchez
# Distributed under the GNU General Public License v3. See LICENSE for more info.

"""Tango server class for Py_ds_serial"""

import asyncio
import urllib.parse

from connio import connection_for_url
from tango import GreenMode
from tango.server import Device, attribute, command, device_property

import py_ds_serial.core


class Py_ds_serial(Device):

    green_mode = GreenMode.Asyncio

    url = device_property(dtype=str)

    async def init_device(self):
        await super().init_device()
        self.connection = connection_for_url(self.url, concurrency="async")
        self.py_ds_serial = py_ds_serial.core.Py_ds_serial(self.connection)

    @attribute(dtype=str, label="ID")
    def idn(self):
        return self.py_ds_serial.get_idn()

    @attribute(dtype=float, unit="bar", label="Pressure")
    async def pressure(self):
        # example processing the result
        pressure = await self.py_ds_serial.get_pressure()
        return pressure / 1000

    @attribute(dtype=float, unit="bar", label="Pressure set point")
    async def pressure_setpoint(self):
        # example processing the result
        setpoint = await self.py_ds_serial.get_pressure_setpoint()
        return setpoint / 1000

    @pressure_setpoint.setter
    def pressure_setpoint(self, value):
        # example returning the coroutine back to tango
        return self.py_ds_serial.get_pressure_setpoint(value * 1000)

    @command
    def turn_on(self):
        # example returning the coroutine back to who calling function
        return self.py_ds_serial.turn_on()


if __name__ == "__main__":
    import logging
    fmt = "%(asctime)s %(levelname)s %(name)s %(message)s"
    logging.basicConfig(level="DEBUG", format=fmt)
    Py_ds_serial.run_server()
