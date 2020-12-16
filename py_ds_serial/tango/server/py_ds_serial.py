# -*- coding: utf-8 -*-
#
# This file is part of the ALBA Python Serial DeviceServer project
#
# Copyright (c) 2020 Alberto López Sánchez
# Distributed under the GNU General Public License v3. See LICENSE for more
# info.

"""Tango server class for Py_ds_serial"""

from tango import GreenMode
from tango.server import Device, command, device_property

import py_ds_serial.core


class Py_ds_serial(Device):

    green_mode = GreenMode.Asyncio

    # The path and name of the serial line device to be used.
    serialline = device_property(dtype=str, doc='')

    # The communication speed in baud used with the serial line protocol.
    baudrate = device_property(dtype=int, default_value=9600)

    # The character length used with the serial line protocol.
    # The possibilities are 8, 7, 6 or 5 bits per character.
    charlength = device_property(dtype=int, default_value=8)

    # End of message Character used in particular by the DevSerReadLine
    # command Default = 13
    newline = device_property(dtype=int, default_value=13)

    # The parity used with the serial line protocol. The possibilities
    # are none = empty, even or odd.
    # TODO: Assert the possibilities.
    parity = device_property(dtype=str, default_value='none')

    # The timout value im ms for for answers of requests send to the serial
    # line. This value should be lower than the Tango client server timout
    # value.
    timeout = device_property(dtype=int, default_value=100)

    # The number of stop bits used with the serial line protocol. The
    # possibilities are 1 or 2 stop bits.
    # TODO: Assert the possibilities.
    stopbits = device_property(dtype=int, default_value=1, doc='asjjssj')

    # TODO: Init
    async def init_device(self):
        await super().init_device()
        self.connection = None
        self.py_ds_serial = py_ds_serial.core.Py_ds_serial(self.connection)

    @command
    def DevSerWriteString(self, string: str) -> int:
        """
        Write a string of characters to a serial line and return the number of
        characters written.
        """
        # TODO
        return self.py_ds_serial.write_string(string)

    @command
    def DevSerFlush(self, what: int) -> None:
        """
        Flush serial line port according to argin passed. 0=input 1=output
        2=both.
        """
        # TODO: Comprobar que el comportamiento es el esperado. flush input
        # discards. flush output waits to write
        self.py_ds_serial.clear_buff(what)

    @command
    def DevSerReadChar(self, argin: int) -> bytes:
        """
        Read an array of characters, the type of read is specified in the input
        parameter, it can be SL_RAW SL_NCHAR SL_LINE.
        """
        # TODO: Check
        # SL_RAW = 0, SL_NCHAR=1, SL_LINE=2
        read_type = argin & 0x000f

        assert read_type in [0, 1, 2]
        if read_type == 0:
            return self.py_ds_serial.readall()
        if read_type == 1:
            nchar = argin >> 8
            return self.py_ds_serial.read_until(nchar)
        if read_type == 2:
            return self.py_ds_serial.readline()

    @command
    def DevSerReadRaw(self) -> bytes:
        """
        Read a string from the serialline device in mode raw (no end of string
        expected, just empty the entire serialline receiving buffer).
        """
        # TODO: Check
        return self.py_ds_serial.readall()

    @command
    def DevSerWriteChar(self, bytes) -> int:
        """
        Write N characters to a seria line and return the number of characters
        written.
        """
        # TODO: Check
        return self.py_ds_serial.write_string(bytes)

    @command
    def Init(self) -> None:
        """
        Reloads the value of the properties and restarts the connection to keep
        it working.
        """
        # TODO: Check
        pass


if __name__ == "__main__":
    import logging
    fmt = "%(asctime)s %(levelname)s %(name)s %(message)s"
    logging.basicConfig(level="DEBUG", format=fmt)
    Py_ds_serial.run_server()
