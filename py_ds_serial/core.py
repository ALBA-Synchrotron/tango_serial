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

import serial

class Py_ds_serial:
    """The central Py_ds_serial"""

    def __init__(self, serialline :str, baudrate :int, charlength :int, newline :int,
     parity: str, timeout: int, stopbits: int):
        """
        Class constructor.

        Parameters
        ----------
        serialline : str
            The path and name of the serial line device to be used.
        baudrate : int
            The communication speed in baud used with the serial line protocol.
        charlength : int
            The character length used with the serial line protocol.
            The possibilities are 8, 7, 6 or 5 bits per character.
        newline : int
            End of message Character used in particular by the DevSerReadLine command Default = 13
        parity : str
            The parity used with the serial line protocol. The possibilities are none = empty, even or odd.
        timeout : float
            The timout value in seconds for for answers of requests send to the serial line.
        stopbits : int
            The number of stop bits used with the serial line protocol. The possibilities are 1 or 2 stop bits.

        """
        self._serialline = serialline
        self._baudrate = baudrate
        self._timeout = timeout / 1000.0 # Convert ms to s.
        self._newline = newline

        assert charlength in [5,6,8,8]
        if charlength == 5:
            self._charlength = serial.FIVEBITS
        elif charlength == 6:
            self._charlength = serial.SIXBITS
        elif charlength == 7:
            self._charlength = serial.SEVENBITS
        elif charlength == 8:
            self._charlength = serial.EIGHTBITS

        assert parity in ['none', 'empty', 'even', 'odd']
        if parity == 'none' or parity == 'empty':
            self._parity = serial.PARITY_NONE
        elif parity == 'even':
            self._parity = serial.PARITY_EVEN
        elif parity == 'odd':
            self_parity = serial.PARITY_ODD


        assert stopbits in [1,2]
        if stopbits == 1:
            self._stopbits = serial.STOPBITS_ONE
        elif stopbits == 2:
            self._stopbits = serial.STOPBITS_TWO

    def connect(self):
        self._sl = serial.serial_for_url(self._serialline, timeout=self._timeout,
            baudrate=self._baudrate, bytesize=self._charlength,
            parity=self._parity, stopbits=self._stopbits)



