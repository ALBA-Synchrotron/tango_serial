# ALBA Python Serial DeviceServer


[![ALBA Python Serial DeviceServer](https://img.shields.io/pypi/v/py_ds_serial.svg)](https://pypi.python.org/pypi/py_ds_serial)


[![ALBA Python Serial DeviceServer updates](https://pyup.io/repos/github/catunlock/py_ds_serial/shield.svg)](https://pyup.io/repos/github/catunlock/py_ds_serial/)


ALBA Python Serial with tango DeviceServer




Apart from the core library, an optional [tango](https://tango-controls.org/) device server is also provided.


## Installation

From within your favorite python environment type:

`$ pip install py_ds_serial`

## Library

The core of the py_ds_serial library consists of Py_ds_serial object.
To create a Py_ds_serial object you need to pass a communication object.

The communication object can be any object that supports a simple API
consisting of two methods (either the sync or async version is supported):

* `write_readline(buff: bytes) -> bytes` *or*

  `async write_readline(buff: bytes) -> bytes`

* `write(buff: bytes) -> None` *or*

  `async write(buff: bytes) -> None`

A library that supports this API is [sockio](https://pypi.org/project/sockio/)
(ALBA Python Serial DeviceServer comes pre-installed so you don't have to worry
about installing it).

This library includes both async and sync versions of the TCP object. It also
supports a set of features like re-connection and timeout handling.

Here is how to connect to a Py_ds_serial controller:

```python
import asyncio

from sockio.aio import TCP
from py_ds_serial import Py_ds_serial


async def main():
    tcp = TCP("192.168.1.123", 5000)  # use host name or IP
    py_ds_serial_dev = Py_ds_serial(tcp)

    idn = await py_ds_serial_dev.idn()
    print("Connected to {} ({})".format(idn))


asyncio.run(main())
```





### Tango server

A [tango](https://tango-controls.org/) device server is also provided.

Make sure everything is installed with:

`$ pip install py_ds_serial[tango]`

Register a Py_ds_serial tango server in the tango database:
```
$ tangoctl server add -s Py_ds_serial/test -d Py_ds_serial test/py_ds_serial/1
$ tangoctl device property write -d test/py_ds_serial/1 -p address -v "tcp://192.168.123:5000"
```

(the above example uses [tangoctl](https://pypi.org/project/tangoctl/). You would need
to install it with `pip install tangoctl` before using it. You are free to use any other
tango tool like [fandango](https://pypi.org/project/fandango/) or Jive)

Launch the server with:

```terminal
$ Py_ds_serial test
```


## Credits

### Development Lead

* Alberto López Sánchez <alopez@cells.es>

### Contributors

None yet. Why not be the first?
