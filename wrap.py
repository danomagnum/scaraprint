import kinematics
import time

class arm:
	def __init__(self):
		ratio = 200/182
		ratio = 198/180 #very close
		L1 = 198
		L2 = 180
		self.army = kinematics.linkage(L1,L2)
		self.x = 0
		self.y = 0
	def move(self,x,y):
		self.army.move(x,y)
		self.x = x
		self.y = y
		#time.sleep(.1)
	def walk(self,x,y):
		dx = self.x - x
		xdir = dx/abs(dx)
		dy = self.y - y
		slope = dy/dx
		intercept = y-slope*x
		moving = True
		xto = 0
		yto = 0
		while moving:
			if self.x != dx:
				newx = self.x + 1
				newy = newx * slope + intercept
				self.move(newx,newy)
			else:
				moving = False
	def calibrate(self,d=30):
		points = ((-d,-d),(d,-d),(-d,d),(d,d))
		while True:
			for pt in points:
				self.move(*pt)
				time.sleep(2)

if __name__ == "__main__":
	a = arm()
	a.calibrate()
