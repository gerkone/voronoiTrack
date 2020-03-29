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
        self.isStart = False
        self.startPerc = None

    def setNextStraight(self, next):
        self.nextStraight = next.id

    def setPreviousStraight(self, previous):
        self.previousStraight = previous.id

    def flagStart(self, startPerc=0.5):
        self.isStart = True
        self.startPerc = startPerc

    def __str__(self):
        return ("startNode: " +str(self.startNode)+"\n endNode: " +str(self.endNode)+ "\n")

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

    def __init__(self, x, y):
        self.id = generator.uuid1().int
        self.x = x
        self.y = y
        self.previousStraight = None
        self.nextStraight = None
        self.spline = False
        self.blend = False
        self.radius = None
        self.center = None
        self.arcStart = None
        self.arcFInish = None

    def setPreviousStraight(self, previous):
        self.previousStraight = previous.id

    def setNextStraight(self, next):
        self.nextStraight = next.id

    def flagSpline(self):
        self.spline = True

    def flagBlend(self):
        self.blend = True

    def __str__(self):
        return ("id: " +str(self.id)+ "\n")
