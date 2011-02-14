import kinematics
import time
import decimal
decimal.getcontext().prec = 8
Dec = decimal.Decimal

L1 = 198
L2 = 180
arm = kinematics.linkage(L1,L2)

gcfile = open('test.gcode')

UNITS = 'Metric'

for line in gcfile:
	items = line.split()
	code = items[0]
	if code == 'G1': #move command
		print 'g1 code'
		x = Dec(items[1].lstrip('X'))
		y = Dec(items[2].lstrip('Y'))
		z = Dec(items[3].lstrip('Z'))
		f = Dec(items[4].lstrip('F')) #speed mm/min
		arm.move(x,y)
	elif code == 'G20':
		UNITS = 'Standard'
		print 'standard units'
	elif code == 'G21':
		UNITS = 'Metric'
		print 'metric units'
	elif code == 'G28':
		print 'Go Home'
	elif code == 'G92':
		print 'Set Home'
	elif code == 'M101':
		print 'turn on extruder forwards'
	elif code == 'M102':
		print 'turn on extruder reverse'
	elif code == 'M103':
		print 'turn off extruder'
	elif code == 'M104':
		s = Dec(items[1].lstrip('S'))
		print 'set extruder temp to', s
	elif code == 'M108':
		s = Dec(items[1].lstrip('S'))
		print 'set extruder speed to', s

	print 'sleeping'
	time.sleep(1)

