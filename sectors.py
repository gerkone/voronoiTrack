import uuid as generator
import math

from utils import angle_3_points

ANGLE_RES = 5 #resolution for the rounded corners

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
            return 360 - (- t%360)

    def _angle_of(self,t):
        a = math.degrees(math.atan((t[1] - self.center[1])/(t[0] - self.center[0])))
        if a < 0:
            a = a +180
        return self._mod360(a)

    def roundify(self):
        if self.blend and self.arc_start != None and self.arc_finish != None:
            circle_coords = lambda b : [self.center[0]+self.radius*math.cos(math.radians(b)), self.center[1]+self.radius*math.sin(math.radians(b))]
            start_angle = self._mod360(self._angle_of(self.arc_start))
            #end angle non viene calcolato bene
            end_angle = self._mod360(self._angle_of(self.arc_finish))
            theta = math.degrees(angle_3_points(self.arc_start,self.center,self.arc_finish))
            angle_steps = []
            if abs(self._mod360(start_angle + theta) - end_angle) < abs(self._mod360(start_angle - theta) - end_angle):
                step = ANGLE_RES
            else:
                step = -ANGLE_RES
            a = start_angle
            while self._mod360(a - end_angle) > ANGLE_RES:
                a = self._mod360(a + step)
                angle_steps.append(a)
            if end_angle in angle_steps:
                angle_steps.remove(end_angle)
            self.arc_points = [circle_coords(b) for b in angle_steps]
        else:
            return
