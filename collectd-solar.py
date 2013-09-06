#!/usr/bin/python 

import minimalmodbus
import os
import time


interval = float(os.getenv('COLLECTD_INTERVAL'))
hostname = os.getenv('COLLECTD_HOSTNAME')

while True: 
	solar = minimalmodbus.Instrument( '/dev/ttyS1', 1 )
	solar.serial.baudrate = 9600
	solar.serial.stopbits = 2

	time.sleep(interval)
	data =  solar.read_registers(8,45)
	tm = time.time()

	iLoad=data[4]*79.16/32768.0
	vLoad=data[2]*100.0/32768.0
	AhLoad=((data[23] << 16) + data[24])*0.1
	print "PUTVAL \"%s/solar/solar_load\" interval=%s %0.0f:%0.2f:%0.2f:%0.2f" % (hostname, interval, tm, iLoad, vLoad, AhLoad)

	vArray=data[1]*100.0/32768.0
	vMP=data[32]*100.0/32768.0
	pMax=data[33]*989.5/65536.0
	vOC=data[34]*100.0/32768.0
	print "PUTVAL \"%s/solar/solar_array\" interval=%s %0.0f:%0.2f:%0.2f:%0.2f:%0.2f" % (hostname, interval, tm, vArray, vMP, pMax, vOC)

	vBatt=data[0]*100.0/32768.0
	print "PUTVAL \"%s/solar/solar_battery\" interval=%s %0.0f:%0.2f" % (hostname, interval, tm, vBatt)

	iCharge=data[3]*100.0/32768.0
	AhCharge=((data[13] << 16) + data[14])*0.1
	kWhCharge=data[17]*0.1
	WCharge=data[31]*989.5/65536.0
	print "PUTVAL \"%s/solar/solar_charge\" interval=%s %0.0f:%0.2f:%0.2f:%0.2f:%0.2f" % (hostname, interval, tm, iCharge, AhCharge, kWhCharge, WCharge)
	
	ambientC=data[7]
	print "PUTVAL \"%s/solar/solar_temp\" interval=%s %0.0f:%0.2f" % (hostname, interval, tm, ambientC)
