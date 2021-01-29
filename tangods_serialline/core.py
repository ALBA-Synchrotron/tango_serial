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


class Serial:
    """The central Serial"""

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

        self._com = serial.serial_for_url(serialline)

        if timeout is not None:
            self.set_timeout(timeout)
        if newline is not None:
            self.set_newline(newline)
        if baudrate is not None:
            self.set_baudrate(baudrate)
        if charlength is not None:
            self.set_charlength(charlength)
        if parity is not None:
            self.set_parity(parity)
        if stopbits is not None:
            self.set_stopbits(stopbits)

    def set_newline(self, value):
        self._newline = chr(value).encode('ascii')

    def set_timeout(self, value):
        self._com.timeout = value / 1000.0  # Convert milliseconds to seconds.

    def set_parity(self, value):
        value = value.lower()
        if value == 'none' or value == 'empty':
            self._com.parity = serial.PARITY_NONE
        elif value == 'even':
            self._com.parity = serial.PARITY_EVEN
        elif value == 'odd':
            self._com.parity = serial.PARITY_ODD
        else:
            raise ValueError(
                "parity has to be 'none', 'empty', 'even', 'odd'. "
                "passed {}".format(value))

    def set_stopbits(self, value):
        if value == 1:
            self._com.stopbits = serial.STOPBITS_ONE
        elif value == 2:
            self._com.stopbits = serial.STOPBITS_TWO
        elif value == 1.5:
            self._com.stopbits = serial.STOPBITS_ONE_POINT_FIVE
        else:
            raise ValueError("stopbits has to be 1, 2 or 1.5. "
                             "passed: {}".format(value))

    def set_charlength(self, value):
        if value == 5:
            self._com.bytesize = serial.FIVEBITS
        elif value == 6:
            self._com.bytesize = serial.SIXBITS
        elif value == 7:
            self._com.bytesize = serial.SEVENBITS
        elif value == 8:
            self._com.bytesize = serial.EIGHTBITS
        else:
            raise ValueError(
                "charlength has to be 5, 6, 7 or 8 bits. "
                "passed {}".format(value))

    def set_baudrate(self, value):
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
            return self.readall() + b'\0'
        if read_type == 1:
            nchar = argin >> 8
            return self._com.read_until(size=nchar)
        if read_type == 2:
            return b"".join(self.__ireadline())
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

    def readall(self) -> bytes:
        """
        Reads all the remaining available in the serial line.
        """
        return self._com.read_all()
