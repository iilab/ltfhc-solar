#!/usr/bin/python 

import minimalmodbus
import os

sunsaver = minimalmodbus.Instrument( '/dev/ttyS1', 1 )

sunsaver.serial.baudrate = 9600
sunsaver.serial.stopbits = 2

interval = os.getenv('COLLECTD_INTERVAL')
hostname = os.getenv('COLLECTD_HOSTNAME')

data =  sunsaver.read_registers(8,45)

iLoad=data[4]*79.16/32768.0
vLoad=data[2]*100.0/32768.0
AhLoad=((data[23] << 16) + data[24])*0.1
print "PUTVAL \"%s/sunsaver/solar_load\" interval=%s N:%0.2f N:%0.2f N:%0.2f" % (hostname, interval, iLoad, vLoad, AhLoad)

vArray=data[1]*100.0/32768.0
vMP=data[32]*100.0/32768.0
pMax=data[33]*989.5/65536.0
vOC=data[34]*100.0/32768.0
print "PUTVAL \"%s/sunsaver/solar_array\" interval=%s N:%0.2f N:%0.2f N:%0.2f N:%0.2f" % (hostname, interval, vArray, vMP, pMax, vOC)

vBatt=data[0]*100.0/32768.0
print "PUTVAL \"%s/sunsaver/solar_battery\" interval=%s N:%0.2f" % (hostname, interval, vBatt)

iCharge=data[3]*100.0/32768.0
AhCharge=((data[13] << 16) + data[14])*0.1
kWhCharge=data[17]*0.1
WCharge=data[31]*989.5/65536.0
print "PUTVAL \"%s/sunsaver/solar_charge\" interval=%s N:%0.2f N:%0.2f N:%0.2f N:%0.2f" % (hostname, interval, iCharge, AhCharge, kWhCharge, WCharge)

ambientC=data[7]
print "PUTVAL \"%s/sunsaver/solar_temp\" interval=%s N:%0.2f" % (hostname, interval, ambientC)
