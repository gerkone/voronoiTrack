import uuid as generator

class Straight:

    def __init__(self, start, end):
        self.id = generator.uuid1().int
        self.startNode = start
        self.endNode = end
        self.nextStraight = None
        self.previousStraight = None

    def setNextStraight(self, next):
        self.nextStraight = next.id

    def setPreviousSTraight(self, previous):
        self.previousStraight = previous.id

class Node: 

    def __init__(self, x, y):
        self.id = generator.uuid1().int
        self.x = x
        self.y = y
        self.prevoiusStraight = None
        self.nextStraight = None

class Corner:

    def __init__(self, node, previous, next):
        self.id = generator.uuid1().int
        self.node = node
        self.previousStraight = previous
        self.nextStraight = next
        self.spline = False
        self.radius = None
        self.center = None
        self.arcStart = None
        self.arcFInish = None

    # TODO: metodo per calcolo di raggio e centro di curvatura
    # TODO: flag per la splinatura
    # TODO: metodo per la generazione di punti densi
