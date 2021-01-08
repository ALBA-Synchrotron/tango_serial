import tango
import os

os.environ["TANGO_HOST"] = "192.168.3.93:10000"

serial1 = tango.DeviceProxy("lab_test/serial/1")

property_names = [
    "serialline",
    "baudrate",
    "charlength",
    "newline",
    "parity",
    "timeout",
    "stopbits"
]

serial_properties = serial1.get_property(property_names)
for prop in serial_properties.keys():
    print("%s: %s" % (prop, serial_properties[prop]))

# Changing Properties
serial_properties["serialline"] = ["/dev/ttyACM0"]
serial_properties["baudrate"] = ["115200"]
serial_properties["charlength"] = ["8"]
serial_properties["newline"] = ["10"]
serial_properties["parity"] = ["none"]
serial_properties["timeout"] = ["100"]
serial_properties["stopbits"] = ["1"]


serial1.put_property(serial_properties)

serial1.Init()
