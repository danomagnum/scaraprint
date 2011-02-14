import kinematics
import math
import time

L1 = 198
L2 = 180
arm = kinematics.linkage(L1,L2)
arm.move(-100,0)
wait = raw_input('hit enter when ready')
for x in xrange(-100,100):
	print x, 70*math.sin(x/10.0)
	arm.move(x,int(70*math.sin(x/30.0)))
	time.sleep(1.3)
