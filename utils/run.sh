#!/bin/bash
export TANGO_HOST=192.168.3.41:10000
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib
python3 serial_device.py test -v4%
