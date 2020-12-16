import tango

dev_info = tango.DbDevInfo()
dev_info.server = "Serial/test"
dev_info._class = "Serial"
dev_info.name = "lab_test/serial/1"

db = tango.Database()
db.add_device(dev_info)
