import uuid as generator
import numpy as np
import math

from utils import angle_3_points

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

    def _mod360(self,t):
        if t > 0:
            return t%360
        else:
            return 360 - (-t%360)

    def _mod180(self, t):
        if t > 180:
            print("before: " + str(t))
            print("after: " + str(t%180 - 180))
            return t%180 - 180
        elif t < -180:
            print("before: " + str(t))
            print("after: " + str(t%(-180) + 180))
            return t%(-180) + 180
        else:
            print(": " + str(t))
            return t

    def roundify(self):
        if self.blend and self.arc_start != None and self.arc_finish != None:
            circle_coords = lambda b : [self.center[0]+self.radius*math.cos(math.radians(b)), self.center[1]+self.radius*math.sin(math.radians(b))]
            start_angle = angle_of(self.arc_start)
            end_angle = angle_of(self.arc_finish)
            theta = math.degrees(angle_3_points(self.arc_start, self.center, self.arc_finish))

            print("Center: "+str(self.center))
            print("Radius: "+str(self.radius))
            print("Start angle: " +str(start_angle))
            print("End angle: " +str(end_angle))
            print("Theta: " +str(theta))

            plus = abs((start_angle+theta)%180 - end_angle)%180
            minus = abs((start_angle-theta)%180 - end_angle)%180

            anglespace = np.linspace(0, theta, num=ANGLE_RES, endpoint=False)

            if plus < minus:
                print("Choosing +")
                s = -1
            elif minus < plus:
                print("Choosing -")
                s = +1
            else:
                s = 0
            for b in anglespace:
                p=circle_coords(start_angle + s*b)
                self.arc_points.append(p)
            self.arc_points.pop(0)
            print("")
        else:
            return
