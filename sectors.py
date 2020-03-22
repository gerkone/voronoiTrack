import uuid as generator

class Straight:

    #id
    #startNode = id
    #startNode = id
    #nextStraight = id
    #previousStraight = id

    def __init__(self, start, end):
        self.id = generator.uuid1().int
        self.startNode = start.id
        self.endNode = end.id
        self.nextStraight = None
        self.previousStraight = None

    def setNextStraight(self, next):
        self.nextStraight = next.id

    def setPreviousSTraight(self, previous):
        self.previousStraight = previous.id

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

    def __init__(self, x, y, previous, next):
        self.id = generator.uuid1().int
        self.x = x
        self.y = y
        self.previousStraight = previous.id
        self.nextStraight = next.id
        self.spline = False
        self.blend = False
        self.radius = None
        self.center = None
        self.arcStart = None
        self.arcFInish = None

    def flagSpline(self):
        self.spline = True

    def flagBlend(self):
        self.blend = True
