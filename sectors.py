import uuid as generator

ANGLE_RES = 20 #resolution for the rounded corners

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

    def _angle_of(t):
        alpha = math.degrees(math.atan((t[1] - self.center[1])/(t[0] - self.center[0])))
        if alpha < 0:
            alpha = alpha + 180

    def roundify(self):
        if blend != None and arc_start != None and arc_finish != None:
            circle = lambda b : [self.center[0]+self.radius*math.cos(b), self.center[1]+self.radius*math.sin(b)]
            start_angle = _angle_of(self.arc_start)
            end_angle = _angle_of(self.arc_end)
            steps = np.linspace(start_angle, end_angle, ANGLE_RES)
            for t in steps:
                arc_points.append(circle(t))
        else:
            return
