# -*- coding: utf-8 -*-
#
# This file is part of the ALBA Python Serial DeviceServer project
#
# Copyright (c) 2020 Alberto López Sánchez
# Distributed under the GNU General Public License v3. See LICENSE for more info.

"""
Core Py_ds_serial module.

It can receive an asynchronous connection object. Example::

    from connio import connection_for_url
    from py_ds_serial.core import Py_ds_serial

    async def main():
        tcp = connection_for_url("tcp://py_ds_serial.acme.org:5000")
        py_ds_serial = Py_ds_serial(tcp)

        idn = await py_ds_serial.get_idn()
        print(idn)

    asyncio.run(main())
"""


class Py_ds_serial:
    """The central Py_ds_serial"""

    def __init__(self, conn):
        self._conn = conn

    # The following code is simply an example. Replace with your own code

    def get_idn(self):
        # example returning the coroutine back to who calling function
        return self._conn.write_readline(b"*IDN?\n")

    async def get_pressure(self):
        # example processing the result
        data = await self._conn.write_readline(b"SENS1:PRES?\n")
        return float(data)

    async def get_pressure_setpoint(self):
        # example processing the result
        data = await self._conn.write_readline(b"PRES1:SP?\n")
        return float(data)

    def set_pressure_setpoint(self, value):
        # example returning the coroutine back to the calling function
        return self._conn.write(f"PRES1:SP {value}\n".encode())

    def turn_on(self):
        # example returning the coroutine back to who calling function
        return self._conn.write(b"SENS1:PRES 1\n")
