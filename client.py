#!/usr/bin/env python
'''
Client for Synology device
'''
#---------------------------------------------------------------------------# 
# import the various server implementations
#---------------------------------------------------------------------------# 
from datetime import datetime, time

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
#from pymodbus.client.sync import ModbusUdpClient as ModbusClient
#from pymodbus.client.sync import ModbusSerialClient as ModbusClient

#---------------------------------------------------------------------------# 
# configure the client logging
#---------------------------------------------------------------------------# 
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

#---------------------------------------------------------------------------# 
# Decide if you want to enable or disable
#---------------------------------------------------------------------------# 
def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def is_enable():
	day = datetime.today().weekday()

	if is_time_between(time(13,00), time(19,00)) and day < 5:
		return True
	elif is_time_between(time(17,00), time(20,00)) and day > 4:
		return True
	else:
		return False

#---------------------------------------------------------------------------# 
# choose the client you want
#---------------------------------------------------------------------------# 
# make sure to start an implementation to hit against. For this
# you can use an existing device, the reference implementation in the tools
# directory, or start a pymodbus server.
#---------------------------------------------------------------------------#
# MODBUS_SERVER_IP = '172.16.16.1'
# MODBUS_SERVER_PORT = 503
MODBUS_SERVER_IP = '127.0.0.1'
MODBUS_SERVER_PORT = 5020
MODUBS_ADDRESS = 0x162
client = ModbusClient(MODBUS_SERVER_IP, port=MODBUS_SERVER_PORT)

# slaves = [10, 11, 12]
slaves = [0x01]
GRID_SUPPORT_VALUE = 1 if is_enable() == True else 0

log.debug("Write to a Coil and read back")

for slave_id in slaves:
	log.debug("slave: {}".format(slave_id))
	rq = client.write_coil(0, GRID_SUPPORT_VALUE, unit=slave_id)
	rr = client.read_coils(0, 1, unit=slave_id)
	print("~"*10, rq)
	assert(not rq.isError())     # test that we are not an error
	assert(rr.bits[0] == True)          # test the expected value

log.debug("Completed")


#---------------------------------------------------------------------------# 
# close the client
#---------------------------------------------------------------------------# 
client.close()