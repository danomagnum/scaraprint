from Tkinter import *
import kinematics
import time

WINSIZE = 200
L1 = 198
L2 = 180
arm = kinematics.linkage(L1,L2)
JOGSIZE = 5

root = Tk()

def movetoclick(event):
	x = event.x - WINSIZE/2
	y = event.y - WINSIZE/2
	print "moving to", x,y
	arm.move(-y,x)

def jog(event):
	key = event.keycode
	x = arm.truex()
	y = -arm.truey()
	print "Jogging from",x, y, key
	if key == 111:#up
		arm.move(x+JOGSIZE,y)
	elif key == 116:#down
		arm.move(x-JOGSIZE,y)
	elif key == 113:#left
		arm.move(x,y-JOGSIZE)
	elif key == 114:#right
		arm.move(x,y+JOGSIZE)

frame = Frame(root, width=WINSIZE, height=WINSIZE)
frame.bind("<Button-1>", movetoclick)
root.bind("<Up>", jog)
root.bind("<Down>", jog)
root.bind("<Left>", jog)
root.bind("<Right>", jog)
frame.pack()
arm.move(0,0)
root.mainloop()

