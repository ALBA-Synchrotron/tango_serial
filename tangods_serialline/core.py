# -*- coding: utf-8 -*-
#
# This file is part of the ALBA Python Serial DeviceServer project
#
# Copyright (c) 2020 Alberto López Sánchez
# Distributed under the GNU General Public License v3. See LICENSE for more
# info.
"""
Core Serial module to adapt the Tango Serial Device Server interface.

It can connects with any serial device. Example::

    from serial.core import Serial

    def main():
        serial = Serial(
            rfc2217://serialDevice.cells.es:40001,
            # bauds speed of the device
            baudrate=115200,
            # the charlength o bytesize. it can be 8, 7, 6 or 5.
            charlength=8,
            # the ASCII value of the character used as newline.
            newline=13,
            # the parity. It can be none, odd or even.
            parity='none',
            # timeout response. It has to be lower than Tango timeout.
            timeout=100,
            # How many stopbits. 1 or 2.
            stopbits=1,
        )

        idn = await serial.get_idn()
        print(idn)

    main()
"""

import serial
from enum import Enum
import logging


class ReadType(Enum):
    Raw = 0
    NChar = 1
    Line = 2
    Retry = 3


class Parity(Enum):
    No = 0
    Odd = 1
    Even = 3


class Charlength(Enum):
    Data8 = 0
    Data7 = 1
    Data6 = 2
    Data5 = 3


class Stopbits(Enum):
    One = 0
    OneAndHalf = 1
    Two = 2


class Parameter(Enum):
    Timeout = 3
    Parity = 4
    Charlength = 5
    Stopbits = 6
    Baudrate = 7
    Newline = 8


class Serial:
    """The central Serial"""

    def __init__(self,
                 serialline: str,
                 baudrate: int = None,
                 charlength: Charlength = None,
                 newline: int = None,
                 parity: Parity = None,
                 timeout: int = None,
                 stopbits: Stopbits = None):
        """
        Class constructor.

        Parameters
        ----------
        serialline : str
            The path and name of the serial line device to be used.
        baudrate : int
            The communication speed in baud used with the serial line protocol.
        charlength : Charlength
            The character length used with the serial line protocol.
            The possibilities are 8, 7, 6 or 5 bits per character.
        newline : int
            End of message Character used in particular by the DevSerReadLine
            command Default = 13
        parity : Parity
            The parity used with the serial line protocol. The possibilities are
            none = empty, even or odd.
        timeout : float
            The timout value in seconds for for answers of requests send to the
            serial line.
        stopbits : Stopbits
            The number of stop bits used with the serial line protocol. The
            possibilities are 1, 1.5 or 2 stop bits.

        """

        self._serialline = serialline
        self._baudrate = baudrate
        self._timeout = timeout / 1000.0  # Convert ms to s.
        self._newline = chr(newline).encode('ascii')

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

        self._com = serial.serial_for_url(
            self._serialline, timeout=self._timeout, baudrate=self._baudrate,
            bytesize=self._charlength, parity=self._parity,
            stopbits=self._stopbits)

    def set_newline(self, value):
        logging.info("Setting newline to: {}".format(value))
        self._newline = chr(value).encode('ascii')

    def set_timeout(self, value):
        logging.info("Setting timeout to: {}".format(value))
        self._com.timeout = value / 1000.0  # Convert milliseconds to seconds.

    def set_parity(self, value: Parity):
        logging.info("Setting parity to: {}".format(value))

        if value == Parity.No:
            self._com.parity = serial.PARITY_NONE
        elif value == Parity.Even:
            self._com.parity = serial.PARITY_EVEN
        elif value == Parity.Odd:
            self._com.parity = serial.PARITY_ODD
        else:
            raise ValueError(
                "parity has to be 'none', 'empty', 'even', 'odd'. "
                "passed {}".format(value))

    def set_stopbits(self, value: Stopbits):
        logging.info("Setting stopbits to: {}".format(value))
        if value == Stopbits.One:
            self._com.stopbits = serial.STOPBITS_ONE
        elif value == Stopbits.Two:
            self._com.stopbits = serial.STOPBITS_TWO
        elif value == Stopbits.OneAndHalf:
            self._com.stopbits = serial.STOPBITS_ONE_POINT_FIVE
        else:
            raise ValueError("stopbits has to be 1, 2 or 1.5. "
                             "passed: {}".format(value))

    def set_charlength(self, value: Charlength):
        logging.info("Setting charlength to: {}".format(value))
        if value == Charlength.Data5:
            self._com.bytesize = serial.FIVEBITS
        elif value == Charlength.Data6:
            self._com.bytesize = serial.SIXBITS
        elif value == Charlength.Data7:
            self._com.bytesize = serial.SEVENBITS
        elif value == Charlength.Data8:
            self._com.bytesize = serial.EIGHTBITS
        else:
            raise ValueError(
                "charlength has to be 5, 6, 7 or 8 bits. "
                "passed {}".format(value))

    def set_baudrate(self, value):
        logging.info("Setting baudrate to: {}".format(value))
        self._com.baudrate = value

    def write_string(self, string: str) -> int:
        """
        Write a string of characters to a serial line and return the number of
        characters written.
        """
        return self._com.write(string.encode('ascii'))

    def write_chars(self, chars: bytes) -> int:
        """
        Write the bytes directly to a serial line and return the number of
        characters written.
        """
        return self._com.write(chars)

    def clear_buff(self, option=0):
        """
        Clears the input buffer or flushs the output buffer.
        arguments
        ----------
        option : int
            0 clears the input buffer, 1 clears the output buffer, 2 both
        """
        if option == 0:
            self._com.reset_input_buffer()
        elif option == 1:
            self._com.flush()
        elif option == 2:
            self._com.flush()
            self._com.reset_input_buffer()
        else:
            raise ValueError('Option {} not valid'.format(option))

    def read(self, argin: int) -> bytes:
        """
        Read chars from the serial line. SL_RAW = 0, SL_NCHAR=1, SL_LINE=2
        """

        read_type = argin & 0x000f

        if read_type == 0:
            return self.readall(None) + b'\0'
        if read_type == 1:
            nchar = argin >> 8
            return self._com.read_until(size=nchar)
        if read_type == 2:
            return b"".join(self.__ireadline())
        if read_type == 3:
            nretry = argin >> 8
            return self.readretry(nretry)
        else:
            raise ValueError("Error in the read type: {}".format(read_type))

    def __ireadline(self):
        while True:
            ch = self._com.read()
            if ch:
                yield ch
                if ch == self._newline:
                    break
            else:
                break

    def readall(self, _) -> bytes:
        """
        Reads all the remaining available in the serial line.
        """
        return self._com.read_all()

    def readretry(self, times):
        buf = bytearray()
        for i in range(times):
            b = self._com.read_all()
            buf.extend(b)
            if b == b"":
                return buf
        return buf

    def read_nchars(self, nchars):
        return self._com.read(size=nchars)

    def set_parameter(self, params):
        print("holaa")
        for type, value in params:
            if type == Parameter.Newline.value:
                self.set_newline(value)
            if type == Parameter.Baudrate.value:
                self.set_baudrate(value)
            if type == Parameter.Charlength.value:
                self.set_charlength(Charlength(value))
            if type == Parameter.Parity.value:
                self.set_parity(Parity(value))
            if type == Parameter.Stopbits.value:
                self.set_stopbits(Stopbits(value))
            if type == Parameter.Timeout.value:
                self.set_timeout(value)
