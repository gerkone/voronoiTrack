import uuid as generator
import numpy as np
import math

from utils import *

ANGLE_RES = 50 #resolution for the rounded corners

class Straight:

    #id
    #startNode = id
    #startNode = id
    #nextStraight = id
    #previousStraight = id

    def __init__(self, start, end):
        self.id = generator.uuid1().int
        self.start_node = start.id
        self.end_node = end.id
        self.next_straight = None
        self.prev_straight = None
        self.is_start = False
        self.start_perc = None

    def setNextStraight(self, next):
        self.next_straight = next.id

    def setPreviousStraight(self, previous):
        self.prev_straight = previous.id

    def flagStart(self, startPerc=0.5):
        self.is_start = True
        self.start_perc = startPerc

    def __str__(self):
        return ("startNode: " +str(self.start_node)+"\n endNode: " +str(self.end_node)+ "\n")

class Corner:

    #id
    #x
    #y
    #previousStraight = id
    #nextStraight = id
    #spline = bool
    #radius = calc
    #center = calc
    #arcStart = calc
    #arcFInish = calc
    #arc_points = []

    def __init__(self, x, y):
        self.id = generator.uuid1().int
        self.x = x
        self.y = y
        self.prev_straight = None
        self.next_straight = None
        self.spline = False
        self.blend = False
        self.radius = None
        self.center = None
        self.arc_start = None
        self.arc_finish = None
        #array of coordinates for the circle
        self.arc_points = []

    def setPreviousStraight(self, previous):
        self.prev_straight = previous.id

    def setNextStraight(self, next):
        self.next_straight = next.id

    def flagSpline(self):
        self.spline = True

    def flagBlend(self):
        self.blend = True

    def __str__(self):
        return ("id: " +str(self.id)+ "\n")

    def _vecFromTo(self, S, E):
        return [E[0]-S[0], E[1]-S[1]]

    def _vecCrossProd(self, A, B):
        return A[0]*B[1]-A[1]*B[0]

    def _angleVec(self, V):
        return math.degrees(np.arctan2(V[1],V[0]))%360

    def _sign(self, a):
    	if a > 0:
    		return 1
    	elif a < 0:
    		return -1
    	else:
    		return 0

    def roundify(self, v, includeLimits=False):
        if self.blend and self.arc_start != None and self.arc_finish != None:
            circle_coords = lambda b : [self.center[0]+self.radius*math.cos(math.radians(b)), self.center[1]+self.radius*math.sin(math.radians(b))]
            vec_start = self._vecFromTo(self.center, self.arc_start)
            vec_end = self._vecFromTo(self.center, self.arc_finish)
            s = self._sign(self._vecCrossProd(vec_start, vec_end))

            angle_start = self._angleVec(vec_start)
            angle_end = self._angleVec(vec_end)
            theta = math.degrees(angle_3_points(self.arc_start, self.center, self.arc_finish))
            if v > 1:
                print("AS: "+str(angle_start))
                print("AE: "+str(angle_end))
                print("T: "+str(theta))
            anglespace = np.linspace(0, theta, num=ANGLE_RES, endpoint=includeLimits)

            for b in anglespace:
                p=circle_coords(angle_start + s*b)
                self.arc_points.append(p)
            if not includeLimits:
                self.arc_points.pop(0)
        else:
            return
