import minimalmodbus
import os

sunsaver = minimalmodbus.Instrument( '/dev/ttyS1', 1 )

sunsaver.serial.baudrate = 9600
sunsaver.serial.stopbits = 2

interval = os.getenv('COLLECTD_INTERVAL')
hostname = os.getenv('COLLECTD_HOSTNAME')

data =  sunsaver.read_registers(8,45)

for (i, j) in enumerate(data):
    print i, j

battVoltage=data[0]*100.0/32768.0
arrayVoltage=data[1]*100.0/32768.0
loadVoltage=data[2]*100.0/32768.0
chargeCurrent=data[3]*100.0/32768.0
loadCurrent=data[4]*79.16/32768.0
ambientTemp=data[7]
powerOut=data[31]*989.5/65536.0


def collectdPrint( name, var ):
	print "PUTVAL \"%s/sunsaver/%s\" interval=%s N:%0.2f" % (hostname, name, interval, var)

collectdPrint( "battVoltage", battVoltage )
collectdPrint( "arrayVoltage", arrayVoltage )
collectdPrint( "loadVoltage", loadVoltage )
collectdPrint( "chargeCurrent", chargeCurrent )
collectdPrint( "loadCurrent", loadCurrent )
collectdPrint( "powerOut", powerOut )
collectdPrint( "ambientTemp", ambientTemp )

