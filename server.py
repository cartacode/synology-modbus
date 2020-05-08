#!/usr/bin/env python
"""
Server for Synogoly device
--------------------------------------------------------------------------
a python thread::

    from threading import Thread

    thread = Thread(target=updating_writer, args=(context,))
    thread.start()
"""
# --------------------------------------------------------------------------- #
# import the modbus libraries we need
# --------------------------------------------------------------------------- #
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer
# from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.server.sync import StartTcpServer

# --------------------------------------------------------------------------- #
# import the twisted libraries we need
# --------------------------------------------------------------------------- #
from twisted.internet.task import LoopingCall
# --------------------------------------------------------------------------- #
# configure the service logging
# --------------------------------------------------------------------------- #
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# MODBUS_SERVER_IP = '172.16.16.1'
# MODBUS_SERVER_PORT = 503
MODBUS_SERVER_IP = '127.0.0.1'
MODBUS_SERVER_PORT = 5020
MODUBS_ADDRESS = 0x162

def run_updating_server():
    # ----------------------------------------------------------------------- # 
    # initialize your data store
    # ----------------------------------------------------------------------- #
    slaves  = {
        0x0A: ModbusSlaveContext(),
        0x0B: ModbusSlaveContext(),
        0x0C: ModbusSlaveContext(),
    }
    context = ModbusServerContext(slaves=slaves, single=False)
    
    # ----------------------------------------------------------------------- # 
    # initialize the server information
    # ----------------------------------------------------------------------- # 
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Synology NAS'
    identity.ProductCode = 'Synology'
    identity.VendorUrl = ''
    identity.ProductName = 'Synology Server'
    identity.ModelName = 'Synology Server'
    identity.MajorMinorRevision = '0.0.1'
    
    # ----------------------------------------------------------------------- # 
    # run the server you want
    # ----------------------------------------------------------------------- # 
    StartTcpServer(context, identity=identity, address=(MODBUS_SERVER_IP, MODBUS_SERVER_PORT))


if __name__ == "__main__":
    run_updating_server()