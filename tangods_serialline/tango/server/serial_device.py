# -*- coding: utf-8 -*-
#
# This file is part of the ALBA Python Serial DeviceServer project
#
# Copyright (c) 2020 Alberto López Sánchez
# Distributed under the GNU General Public License v3. See LICENSE for more
# info.

"""Tango server class for Serial"""


from serial.serialutil import SerialException
from tango.server import Device, command, device_property

import tangods_serialline.core
import tango


class Serial(Device):

    serialline = device_property(

        dtype=str,
        default_value="/dev/ttyR0",
        doc="Device name, number or URL. "
        "Examples: '/dev/ttyACM0', 'COM1',"
        "rfc2217://<host>:<port>[?<option>[&<option>...]]."
        "For more information about the supported URLs visit:"
        "https://pyserial.readthedocs.io/en/latest/url_handlers.html#urls")

    baudrate = device_property(
        dtype=int, default_value=9600,
        doc="The speed in baud used with the serial line protocol."
        "Examples: 9600, 115200")

    charlength = device_property(
        dtype=int, default_value=8,
        doc="The character"
        "length used with the serial line protocol."
        "The possibilities are 8, 7, 6 or 5 bits per character.")
    # TODO: 6 and 5 doesn't work in the Arduino.

    newline = device_property(
        dtype=int, default_value=13,
        doc="End of message Character used in particular by the "
        "DevSerReadLine command. Default = 13")

    parity = device_property(
        dtype=str, default_value='none',
        doc="The parity used with the serial line protocol. The possibilities "
        "are none = empty, even or odd.")

    timeout = device_property(
        dtype=int, default_value=100,
        doc="The timout value im ms for for answers of requests send to the "
        "serial line. This value should be lower than the Tango client server "
        "timout value.")

    stopbits = device_property(
        dtype=int, default_value=1,
        doc="The number of stop bits used with the serial line protocol."
        " The possibilities are 1 or 2 stop bits.")

    def init_device(self):
        super().init_device()
        try:
            self.serial = tangods_serialline.core.Serial(
                self.serialline, self.baudrate, self.charlength,
                self.newline, self.parity, self.timeout,
                self.stopbits
            )
        except SerialException as e:
            print("Serial Exception initializing device: ", e)
            print("\nCheck the properties!")

    @command(dtype_in=str, doc_in="string of characters",
             dtype_out=int, doc_out="number of characters written")
    def DevSerWriteString(self, string: str) -> int:
        """
        Write a string of characters to a serial line and return the number of
        characters written.
        """
        return self.serial.write_string(string)

    @command(dtype_in=int, doc_in="SL_RAW SL_NCHAR SL_LINE",
             dtype_out=str,
             doc_out="byte array with the characters readed.")
    def DevSerReadString(self, argin: int) -> str:
        """
        Read terminated string from the serialline device (end of string
        expected).
        """
        return self.serial.read(argin)

    @command(dtype_in=int, doc_in="0=input 1=output 2=both")
    def DevSerFlush(self, what: int) -> None:
        """
        Flush serial line port according to argin passed. 0=input 1=output
        2=both.
        """
        # TODO: Comprobar que el comportamiento es el esperado. flush input
        # discards. flush output waits to write
        self.serial.clear_buff(what)

    @command(dtype_in=int, doc_in="SL_RAW SL_NCHAR SL_LINE",
             dtype_out=tango.DevVarCharArray,
             doc_out="byte array with the characters readed.")
    def DevSerReadChar(self, argin: int) -> tango.DevVarCharArray:
        """
        Read an array of characters, the type of read is specified in the input
        parameter, it can be SL_RAW SL_NCHAR SL_LINE.
        """
        return self.serial.read(argin)

    @command(dtype_out=str,
             doc_out="byte array with the characters readed.")
    def DevSerReadRaw(self) -> str:
        """
        Read a string from the serialline device in mode raw (no end of string
        expected, just empty the entire serialline receiving buffer).
        """
        return self.serial.readall()

    @command(dtype_in=tango.DevVarCharArray, doc_in="string of characters",
             dtype_out=int, doc_out="number of characters written")
    def DevSerWriteChar(self, chararray: bytes) -> int:
        """
        Write N characters to a serial line and return the number of characters
        written.
        """
        # TODO: Check
        print("DevSerWriteChar: ", chararray)
        return self.serial.write_chars(chararray)

    @command(dtype_in=tango.DevVarLongStringArray, dtype_out=tango.DevString)
    def WriteRead(self, charaarray: bytes) -> int:
        """
        This method permit to send a request to a device throw the serial line and returns the
        response of the device.
        The commands write and read don`t return until they have not finished. 
        """
        raise RuntimeError("Uninplemented method")

if __name__ == "__main__":
    import logging
    fmt = "%(asctime)s %(levelname)s %(name)s %(message)s"
    logging.basicConfig(level="DEBUG", format=fmt)
    Serial.run_server()
