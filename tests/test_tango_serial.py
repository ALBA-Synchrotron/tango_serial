#!/usr/bin/env python

"""Tests for `tango_serial` package."""


import unittest


class TestSerial(unittest.TestCase):
    """Tests for `tango_serial` package.
    THIS TESTs ASSUME THAT YOU HAVE A SERIAL DEVICE WITH AN ECHO COMMAND
    AND YOU ALSO REGISTER YOUR DEVICE SERVER AS "lab_test/serial/1" AND
    IS RUNNING
    """

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""
