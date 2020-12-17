# ALBA Python Serial DeviceServer


[![ALBA Python Serial DeviceServer](https://img.shields.io/pypi/v/tango_serial.svg)](https://pypi.python.org/pypi/tango_serial)


[![ALBA Python Serial DeviceServer updates](https://pyup.io/repos/github/catunlock/tango_serial/shield.svg)](https://pyup.io/repos/github/catunlock/tango_serial/)


ALBA Python Serial with tango DeviceServer


Apart from the core library, an optional [tango](https://tango-controls.org/) device server is also provided.


## Installation

From within your favorite python environment type:

`$ pip install tango_serial`

## Library

The core of the tango_serial library consists of Serial object.
To create a Serial object you need to pass a communication object.

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

Here is how to connect to a Serial controller:

```python
import asyncio

from sockio.aio import TCP
from tango_serial import Serial


async def main():
    tcp = TCP("192.168.1.123", 5000)  # use host name or IP
    tango_serial_dev = Serial(tcp)

    idn = await tango_serial_dev.idn()
    print("Connected to {} ({})".format(idn))


asyncio.run(main())
```

### Tango server

A [tango](https://tango-controls.org/) device server is also provided.

Make sure everything is installed with:

`$ pip install tango_serial[tango]`

Register a Serial tango server in the tango database:
```
$ tangoctl server add -s Serial/test -d Serial test/tango_serial/1
$ tangoctl device property write -d test/tango_serial/1 -p address -v "tcp://192.168.123:5000"
```

(the above example uses [tangoctl](https://pypi.org/project/tangoctl/). You would need
to install it with `pip install tangoctl` before using it. You are free to use any other
tango tool like [fandango](https://pypi.org/project/fandango/) or Jive)

Launch the server with:

```terminal
$ Serial test
```


## Credits

### Development Lead

* Alberto López Sánchez <alopez@cells.es>
* CTBeamlines (ctbeamlines@cells.es)

### Contributors

None yet. Why not be the first?
