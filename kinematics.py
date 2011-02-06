import math
import time
import serial
from vector2 import Vector
from decimal import *
getcontext().prec = 8

ser = serial.Serial(0,9600,timeout=0,parity=serial.PARITY_NONE,rtscts=1)
#example: ser.write(serial.to_bytes((255,0,100))) where 255 is always 255, 0 is the servo number, and 100 is the servo position, scaled from 0-254

class linkage:
	def __init__(self,L1,L2,theta1=0,theta2=0):
		self.L1 = L1 #bicep length
		self.L2 = L2 #forearm length
		self.theta1 = theta1 #Shoulder
		self.theta2 = theta2 #Elbow
		self.x,self.y = self.forward() #hand position

	def degrees(self):
		'''return tuple of shoulder,elbow angles'''
		mlt = 180/math.pi
		return (mlt*self.theta1,mlt*self.theta2)

	def set_inverse(self,x,y):
		'''given x,y pair, figure out and set my angles, and new xy values'''
		self.theta1,self.theta2 = self.inverse(x,y)
		self.set_forward()

	def inverse(self,x,y):
		'''given x,y pair, figure out angles'''
		B = math.sqrt(x**2 + y**2)
		q1 = math.atan2(y,x)
		q2 = math.acos((self.L1**2 - self.L2**2 + B**2)/(2 * self.L1 * B))
		theta1 = q1+q2
		theta2 = math.pi - math.acos((self.L1**2 + self.L2**2 - B**2)/(2 * self.L1 * self.L2))
		return (theta1,theta2)

	def set_forward(self):
		'''re-calculate and set my hand position x,y values'''
		self.x, self.y = self.forward()
			
	def forward(self):
		'''calculate and return my hand position x,y values'''
		y = math.sin(self.theta1)*self.L1
		x = math.cos(self.theta1)*self.L1
		y += math.sin(self.theta1 - self.theta2)*self.L2
		x += math.cos(self.theta1 - self.theta2)*self.L2
		return (Decimal(str(x)),Decimal(str(y)))

	def move(self,x,y,steps=1,stepdelay=1):
		'''splits a move up into intermediate points
		this results in a straighter line from the current point to x,y'''
		steps = Decimal(steps)
		dx = (x - self.x)/steps
		dy = (y - self.y)/steps
		step = 1
		while step <= steps:
			self.set_inverse(self.x + dx,self.y + dy)
			print 'moved to', self.x,self.y, 'angles are', self.degrees()
			self.apply_xy()
			time.sleep(stepdelay) #stepdelay should probably end up being a function of dx and dy
			step += 1

	def apply_xy(self):
		'''this invokes the serial communication to the servos
		which causes them to move to the position of this class model'''
		p1 = self.theta1 #p1 and p2 are the scaled values for servo position from 0-254 instead of -90 to 90 or whatever
		p2 = self.theta2
		ser.write(serial.to_bytes((255,0,p1))) #write x
		ser.write(serial.to_bytes((255,1,p2))) #write y
		pass

	def apply_z(self):
		'''this talks over the serrial communication to set the z height'''
		p3 = self.z
		ser.write(serial.to_bytes((255,2,p3))) #write z

