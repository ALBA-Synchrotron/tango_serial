#!/usr/bin/env python

"""Tests for `tango_serial` package."""


import unittest

from tango_serial import core
import tango
import os
import time


class TestSerial(unittest.TestCase):
    """Tests for `tango_serial` package.
    THIS TESTs ASSUME THAT YOU HAVE A SERIAL DEVICE WITH AN ECHO COMMAND
    AND YOU ALSO REGISTER YOUR DEVICE SERVER AS "lab_test/serial/1" AND
    IS RUNNING
    """

    def setUp(self):
        """Set up test fixtures, if any."""
        os.environ["TANGO_HOST"] = "192.168.3.41:10000"
        self.message = b"ECHO Hola\nAdios"

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_DevSerReadRaw(self):
        """Test something."""
        t = tango.DeviceProxy("lab_test/serial/1")
        t.Init()

        nchar = t.DevSerWriteString(self.message)
        print("Nchar:", 15)
        self.assertEqual(nchar, 15)

        time.sleep(1)

        response = t.DevSerReadRaw()
        response = t.DevSerReadRaw()
        print("Response:", response)
        self.assertEqual(response, 'Hola\nAdios')
