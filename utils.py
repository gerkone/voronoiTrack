import matplotlib.pyplot as plt
from catmull_spline import *
import numpy as np
import math

MAX_X = 100
MAX_Y = 100

def cross(q1,q2,q3):
	return (q2.x - q1.x)*(q3.y - q1.y) - (q2.y - q1.y)*(q3.x - q1.x)

def length(q1,q2):
	return ((q1.x - q2.x)**2 + (q1.y - q2.y)**2)**(1/2.0)

def angle(p1, p2, p3):
	return math.degrees(math.acos((length(p2, p1)**2 + length(p2,p3)**2 - length(p1, p3)**2) / (2 * length(p2, p1) * length(p2, p3))))

def line(q1,q2,x):
	return (slope(q1,q2)*(x - q1.x) + q1.y)

def spline(points):
	qxs = [q.x for q in points]
	qys = [q.y for q in points]
	return catmull_rom(qxs,qys,10)

def intersect(L1,L2):
	t = set(L2)
	LI = [x for x in L1 if x in t]
	return LI

def get_by_ID(id,L):
	for el in L:
		if el.id == id:
			return el
	return None
