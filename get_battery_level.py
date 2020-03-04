#!/usr/bin/env python3


def execute(battery_log_dir, serial_port):

	import serial, time, array, binascii
	import datetime

	ser = serial.Serial()
	ser.port = serial_port # arg number 2 (e.g. "/dev/ttyUSB0")
	ser.baudrate = 38400
	ser.bytesize = serial.EIGHTBITS
	ser.parity = serial.PARITY_NONE
	ser.stopbits = serial.STOPBITS_ONE
	ser.timeout = 1
	ser.xonxoff = False
	ser.rtscts = False
	ser.dsrdtr = False
	ser.open()
	ser.flushInput()
	ser.flushOutput()

	a0 = array.array('B',[0xA5,0x69,0x03,0x10,0xEC]) # READ PARAMS
	a1 = array.array('B',[0xA5,0x69,0x03,0x60,0x9c]) # READ I&V
	a2 = array.array('B',[0xA5,0x69,0x03,0x61,0x9b]) # READ ACTUAL AH


	try:
		ser.write(a0)
		r0 = binascii.hexlify(ser.read(25))
		ah = (int(r0[6:8] + r0[4:6] + r0[2:4] + r0[0:2],16)/1000)/3600.0
		Vbat = int(r0[10:12] + r0[8:10],16)
		I_Factor = int(r0[14:16]+ r0[12:14],16)
		I_Factor=I_Factor/1000
		I_Offset = int(r0[18:20]+ r0[16:18],16)

		ser.write(a1)
		r1 = binascii.hexlify(ser.read(25))
		Current = int(r1[2:4]+r1[0:2],16)
		CurrentCurrent = ((I_Offset - Current)*I_Factor)/1000
		Volt = int(r1[6:8]+r1[4:6],16)
		VoltVal = (Volt*Vbat)/10000


		CurrentCurrent = CurrentCurrent if CurrentCurrent > 0 else CurrentCurrent*-1

		ser.write(a2)
		r2 = binascii.hexlify(ser.read(25))

		AH_low = int(r2[2:4]+r2[0:2],16)
		AH_high = int(r2[6:8]+r2[4:6],16)

		actual_ah = (int(r2[6:8] + r2[4:6] + r2[2:4] + r2[0:2],16)/1000)/3600.0
		new_calc_prcnt=round(100*actual_ah/ah,2)

	except Exception as e:
		print("-E- Failed to read data from battery --")
		print("	-- " + str(e))
		exit(1)

	##### units  alignment
	VoltVal=VoltVal/1000

	#### rounding for nice niew
	actual_ah=round(actual_ah,2)
	CurrentCurrent=round(CurrentCurrent,2)
	VoltVal=round(VoltVal,2)

	#### current time
	import time
	# nice_time=time.strftime("%d_%b_%Y_%l_%M%p")
	now = datetime.datetime.now().strftime("%Y%m%d%H%M")
	########## saving to file ###########
	with open(battery_log_dir + "/an_battery_" +  now + ".log", 'w') as w1:
		endline = '\r\n'

		head = 'Design Ampere hour,Current,Volt,Amp H,% capacity' + endline
		w1.write(head)
		l = now
		l += ","
		l += str(ah)+" AH"
		l += ","
		l += str(CurrentCurrent)+" mA"
		l += ","
		l += str(VoltVal)+" v"
		l += ","
		l += str(actual_ah)+" AH"
		l += ","
		l += str(new_calc_prcnt) + "%"
		l += endline
		w1.write(l)
		print(head)
		print(l)


if __name__ == '__main__':
    execute(".", "/dev/ttyUSB0")
