import minimalmodbus
import os
import time

from serial import SerialException

while True:
        time.sleep(0.5)
        try:   
                sunsaver = minimalmodbus.Instrument( '/dev/ttyS1', 1 )

                sunsaver.serial.baudrate = 9600
                sunsaver.serial.stopbits = 2

                interval = os.getenv('COLLECTD_INTERVAL')
                hostname = os.getenv('COLLECTD_HOSTNAME')

                data = sunsaver.read_registers(8,45)

                battVoltage=data[0]*100.0/32768.0
                loadVoltage=data[2]*100.0/32768.0
                arrayVoltage=data[1]*100.0/32768.0
                chargeCurrent=data[3]*100.0/32768.0
                loadCurrent=data[4]*79.16/32768.0
                ambientTemp=data[7]
                powerOut=data[31]*989.5/65536.0

                print "%s battVoltage: %1.2fV / arrayVoltage: %1.2fV / loadVoltage: %1.2fV / chargeCurrent: %1.2fA / loadCurrent: %1.2fA / powerOut: %1.2fW / ambientTemp: %1.2fC" % (time.strftime('%x %X'), battVoltage, arrayVoltage, loadVoltage, chargeCurrent, loadCurrent, powerOut, ambientTemp)

        except SerialException:
                pass
