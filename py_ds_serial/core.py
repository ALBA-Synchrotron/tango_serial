# -*- coding: utf-8 -*-
#
# This file is part of the ALBA Python Serial DeviceServer project
#
# Copyright (c) 2020 Alberto López Sánchez
# Distributed under the GNU General Public License v3. See LICENSE for more
# info.
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
import io


class Py_ds_serial:
    """The central Py_ds_serial"""

    def __init__(self, serialline: str, baudrate: int, charlength: int,
                 newline: int, parity: str, timeout: int, stopbits: int):
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
            End of message Character used in particular by the DevSerReadLine
            command Default = 13
        parity : str
            The parity used with the serial line protocol. The possibilities are
            none = empty, even or odd.
        timeout : float
            The timout value in seconds for for answers of requests send to the
            serial line.
        stopbits : int
            The number of stop bits used with the serial line protocol. The
            possibilities are 1 or 2 stop bits.

        """
        self._serialline = serialline
        self._baudrate = baudrate
        self._timeout = timeout / 1000.0  # Convert ms to s.
        self._newline = newline

        if charlength == 5:
            self._charlength = serial.FIVEBITS
        elif charlength == 6:
            self._charlength = serial.SIXBITS
        elif charlength == 7:
            self._charlength = serial.SEVENBITS
        elif charlength == 8:
            self._charlength = serial.EIGHTBITS
        else:
            raise ValueError(
                "charlength has to be 5, 6, 7 or 8 bits. "
                "passed {}".format(charlength))

        parity = parity.lower()
        assert parity in ['none', 'empty', 'even', 'odd']
        if parity == 'none' or parity == 'empty':
            self._parity = serial.PARITY_NONE
        elif parity == 'even':
            self._parity = serial.PARITY_EVEN
        elif parity == 'odd':
            self._parity = serial.PARITY_ODD
        else:
            raise ValueError(
                "parity has to be 'none', 'empty', 'even', 'odd'. "
                "passed {}".format(parity))

        if stopbits == 1:
            self._stopbits = serial.STOPBITS_ONE
        elif stopbits == 2:
            self._stopbits = serial.STOPBITS_TWO
        elif stopbits == 1.5:
            self._stopbits = serial.STOPBITS_ONE_POINT_FIVE
        else:
            raise ValueError("stopbits has to be 1, 2 or 1.5. "
                             "passed: {}".format(stopbits))

    def connect(self):
        self._sl = serial.serial_for_url(
            self._serialline, timeout=self._timeout, baudrate=self._baudrate,
            bytesize=self._charlength, parity=self._parity,
            stopbits=self._stopbits)

        self._sio = io.TextIOWrapper(
            io.BufferedReader(self._sl), newline=self._newline)

    def write_string(self, string: bytes) -> int:
        """
        Write a string of characters to a serial line and return the number of
        characters written.
        """
        return self._sl.write(string)

    def clear_buff(self, option=1):
        if option == 1:
            self._sl.flush
        elif option == 2:
            self._sl.reset_input_buffer()
        elif option == 3:
            self._sl.flush()
            self._sl.reset_input_buffer()
        else:
            raise ValueError('Option {} not valid'.format(option))

    def readline(self) -> bytes:
        self._sio.readline()

    def readall(self) -> bytes:
        return self._sl.read_all()

    def read_until(self, size: int) -> bytes:
        return self._sl.read_until(self._sl._newline, size)
