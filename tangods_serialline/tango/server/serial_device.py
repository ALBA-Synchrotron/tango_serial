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

from tangods_serialline.core import Charlength, Parity, Stopbits
import tangods_serialline.core
import tango
from time import sleep
import logging


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

    def safe_reconnection(self, func, arg):
        if self.connected:
            try:
                return func(arg)
            except SerialException as e:
                logging.warning("{}: {}".format(func.__name__, e))
                self.connect()
            except BrokenPipeError as e:
                logging.warning("{}: {}".format(func.__name__, e))
                self.connect()
        else:
            self.connect()

    def connect(self):
        self.connected = False
        if not self.connected:
            try:
                self.serial = tangods_serialline.core.Serial(
                    self.serialline, self.baudrate, self.charlength,
                    self.newline, self.parity, self.timeout,
                    self.stopbits
                )
                self.connected = True
            except SerialException as e:
                print("Serial Exception initializing device: ", e)
                print("\nCheck the properties!")
                raise tango.CommunicationFailed("The port is down.")
                sleep(1)

    def init_device(self):
        super().init_device()
        self.connect()

    @command(dtype_in=str, doc_in="string of characters",
             dtype_out=int, doc_out="number of characters written")
    def DevSerWriteString(self, string: str) -> int:
        """
        Write a string of characters to a serial line and return the number of
        characters written.
        """
        return self.safe_reconnection(self.serial.write_string, string)

    @command(dtype_in=int, doc_in="SL_RAW SL_NCHAR SL_LINE",
             dtype_out=str,
             doc_out="byte array with the characters readed.")
    def DevSerReadString(self, argin: int) -> str:
        """
        Read terminated string from the serialline device (end of string
        expected).
        """
        return self.safe_reconnection(self.serial.read, argin)

    @command(dtype_in=int, doc_in="0=input 1=output 2=both")
    def DevSerFlush(self, what: int) -> None:
        """
        Flush serial line port according to argin passed. 0=input 1=output
        2=both.
        """
        # TODO: Comprobar que el comportamiento es el esperado. flush input
        # discards. flush output waits to write
        self.safe_reconnection(self.serial.clear_buff, what)

    @command(dtype_in=int, doc_in="SL_RAW SL_NCHAR SL_LINE",
             dtype_out=tango.DevVarCharArray,
             doc_out="byte array with the characters readed.")
    def DevSerReadChar(self, argin: int) -> tango.DevVarCharArray:
        """
        Read an array of characters, the type of read is specified in the input
        parameter, it can be SL_RAW SL_NCHAR SL_LINE.
        """
        return self.safe_reconnection(self.serial.read, argin)

    @command(dtype_out=str,
             doc_out="byte array with the characters readed.")
    def DevSerReadRaw(self) -> str:
        """
        Read a string from the serialline device in mode raw (no end of string
        expected, just empty the entire serialline receiving buffer).
        """
        return self.safe_reconnection(self.serial.readall, None)

    @command(dtype_in=tango.DevVarCharArray, doc_in="string of characters",
             dtype_out=int, doc_out="number of characters written")
    def DevSerWriteChar(self, chararray: bytes) -> int:
        """
        Write N characters to a serial line and return the number of characters
        written.
        """
        return self.safe_reconnection(self.serial.write_chars, chararray)

    # Valid VarLongStringArray: argin = ([1,2,3], ["Hello", "TangoTest device"])
    @command(dtype_in=tango.DevVarLongStringArray, dtype_out=tango.DevString)
    def WriteRead(self, argin) -> str:
        """
        This method permit to send a request to a device throw the serial line
        and returns the response of the device.
        The commands write and read don`t return until they have not finished.
        """
        read_mode = argin[0][0]
        message = argin[1][0]
        self.safe_reconnection(self.serial.write_string, message)
        response = self.safe_reconnection(self.serial.read, read_mode)

        return response.decode("UTF-8")

    @command(dtype_in=tango.DevLong, dtype_out=tango.DevVarCharArray)
    def DevSerReadNBinData(self, n_chars: int) -> tango.DevVarCharArray:
        """
        Read the specified number of char from the serial line.
        If the number of caracters is greater than caracters avaiable, this
        command returns all caracters avaiables.
        If there are no characters to be read returns an empty array.
        """
        return self.safe_reconnection(self.serial.read_nchars, n_chars)

    @command(dtype_in=tango.DevLong, dtype_out=tango.DevString)
    def DevSerReadRetry(self, nretry: int) -> str:
        """
        read a string from the serialline device in mode raw (no end
        of string expected, just empty the entire serialline receiving buffer).
        - If read successfull, read again "nretry" times.
        - If no more data found exit on timeout without error.
        """
        b = self.safe_reconnection(self.serial.readretry, nretry)
        return b.decode("utf-8")

    @command(dtype_in=tango.DevVarLongArray, dtype_out=tango.DevVoid)
    def DevSerSetParameter(self, params: tango.DevVarLongArray) -> None:
        """
        Set serial line parameters. Example: [SL_TIMEOUT, 100, SL_PARITY, 1]
        """
        parameters = [(params[i], params[i+1])
                      for i in range(0, len(params), 2)]

        self.serial.set_parameter(parameters)

    @command(dtype_in=tango.DevShort, dtype_out=tango.DevVoid)
    def DevSerSetTimeout(self, timeout: int) -> None:
        """
        This command sets the new timeout (in ms).
        """
        self.serial.set_timeout(timeout)

    @command(dtype_in=tango.DevShort, dtype_out=tango.DevVoid)
    def DevSerSetParity(self, value: int) -> None:
        """
        Sets the new parity of the serial line. NONE=0 ODD=1 EVEN=3
        """
        self.serial.set_parity(Parity(value))

    @command(dtype_in=tango.DevShort, dtype_out=tango.DevVoid)
    def DevSerSetCharLength(self, value: int) -> None:
        """
        Sets the new charlength. 0 = 8 bits, 1 = 7 bits, 2 = 6 bits, 3 = 5 bits
        """

        self.serial.set_charlength(Charlength(value))

    @command(dtype_in=tango.DevShort, dtype_out=tango.DevVoid)
    def DevSerSetStopbit(self, value: int) -> None:
        """
        Sets the new stop bit. 0 = one, 1 = two stop, 2 = 1.5 stop bit
        # TODO: Check if what the documentation says is true.
        """
        self.serial.set_stopbits(Stopbits(value))

    @command(dtype_in=tango.DevULong, dtype_out=tango.DevVoid)
    def DevSerSetBaudrate(self, baudrate: int) -> None:
        """
        Sets the new baudrateof the serial line.
        """
        self.serial.set_baudrate(baudrate)

    @command(dtype_in=tango.DevUShort, dtype_out=tango.DevVoid)
    def DevSerSetNewline(self, newline: int) -> None:
        """
        The new ending character in hexa. Default is 0x13 (=CR)
        """
        self.serial.set_newline(newline)


if __name__ == "__main__":
    fmt = "%(asctime)s %(levelname)s %(name)s %(message)s"
    logging.basicConfig(level="DEBUG", format=fmt)
    Serial.run_server()
