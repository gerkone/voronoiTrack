# import pyclipper
import math
import numpy as np

def distance(q1,q2):
	if hasattr(q1,"x"):
		x1,y1 = q1.x,q1.y
	else:
		x1,y1 = q1[0],q1[1]
	if hasattr(q2,"x"):
		x2,y2 = q2.x,q2.y
	else:
		x2,y2 = q2[0],q2[1]
	return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

def angle_3_points(A, B, C):
	l1 = distance(A, B)
	l2 = distance(B, C)
	if hasattr(A,"x"):
		x1,y1 = A.x,A.y
	else:
		x1,y1 = A[0],A[1]
	if hasattr(B,"x"):
		x2,y2 = B.x,B.y
	else:
		x2,y2 = B[0],B[1]
	if hasattr(C,"x"):
		x3,y3 = C.x,C.y
	else:
		x3,y3 = C[0],C[1]
	return math.acos(((x2-x1)*(x2-x3)+(y2-y1)*(y2-y3))/float(l1*l2))

def angle_of(q,center):
	#engineer's method
    dx = 10**-10
    return (angle_3_points(q, center, [center[0] + dx, center[1]]))
