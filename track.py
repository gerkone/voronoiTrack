import random as rand
import scipy
import math
from collections import deque
import matplotlib.pyplot as plt
import json

from voronoi import *
from utils import *
from sectors import *

BOUNDARY_DEFAULT_SCALE = 0.1

class Track:

    # straights = dequeue of obj corner
    # corners = dequeue of obj corner

    def __init__(self, boundary, npoints, seed, verbose=False, scale=BOUNDARY_DEFAULT_SCALE):
        self.straights = deque()
        self.corners = deque()

        self.boundary = Boundary(boundary[0],boundary[1], scale)
        self.figure = Vor(npoints, self.boundary, seed)
        for v_key in self.figure.vertices.keys():
            if(self.figure.vertices.get(v_key)._is_out_of_bounds(self.boundary)):
                self.figure.delete_element(v_key, False)
        self.figure.cleanup()

    def _element(self, ID):
        if ID is None:
            print("ID of _element is None")
            return None
        element = get_by_ID(ID, self.straights)
        if element is not None:
            return element
        element = get_by_ID(ID, self.corners)
        if element is not None:
            return element
        print("Found nothing")
        return None

    def select_bfs(self, perc):
        """
        Acts as a breath first visit and adds new cells to the selected area
        starting from a random cell. (deprecated)
        """
        areaTot = sum([self.figure._area(c) for c in list(self.figure.cells.values())])
        toCover = areaTot * perc
        covered = 0
        #start from a random cell
        q = deque([rand.choice(list(self.figure.cells.values()))])
        q[0].flag_center()
        while len(q) > 0:
            el = q.popleft()
            #update the area with the added region
            covered = covered + self.figure._area(el)
            if toCover < covered:
                #ugly (and wrong) way to patch possible holes
                for el in q:
                    if all([c.selected for c in self.figure._adjacent_cells(el)]):
                        el.flag_selected()
                break
            else:
                el.flag_selected()
                for adj in self.figure._adjacent_cells(el):
                    if adj not in q and not adj.selected:        #does not enqueue already enqueued and already selected
                        q.append(adj)

    def select_by_hull(self, perc, n = 5):
        """
        Draws a random n-edged hull over the voronoi diagram; only the cells that
        have at least one vertex inside the hull get included in the selected area.
        """
        figurePoints = []
        #generate a random point centered in the middle of the boundary
        randPoint = lambda : np.array((random.randint(0, self.boundary.x+1) * perc - 50 * perc + 50, random.randint(0, self.boundary.y+1) * perc - 50 * perc +50))
        figurePoints.append(randPoint())
        figurePoints.append(randPoint())
        figurePoints.append(randPoint())
        convex = scipy.spatial.ConvexHull(figurePoints, incremental=True)
        #add n vertices to the hull
        while len(convex.vertices) < n:
            convex.add_points([randPoint()])
        convex.close()
        #scans for vertices inside the hull
        for v in self.figure.vertices.values():
            if in_hull([[v.x,v.y]], [convex.points[i] for i in convex.vertices])[0]:
                for c in v.cells:
                    (self.figure.cells.get(c)).flag_selected()

    def select(self, perc, method = "hull", n = 5):
        if method == "hull":
            self.select_by_hull(perc, n)
        else:
            self.select_bfs(perc)

        vertices = []
        out_edges = self.figure._filter_outside_edges()
        for e in out_edges:
            if (e.v1 not in vertices):
                vertices.append(e.v1)
            if (e.v2 not in vertices):
                vertices.append(e.v2)
        #single cell representing the track
        track_cell = Cell([self.figure.vertices.get(v) for v in vertices], 0)
        for e in out_edges:
            track_cell.connect_edge(e)
        sorted_edges, sorted_vertices = self.figure.sort(track_cell)

        t1 = Corner(sorted_vertices[-1].x,sorted_vertices[-1].y)
        t0 = Corner(sorted_vertices[0].x,sorted_vertices[0].y)
        self.corners.append(t1)
        self.straights.append(Straight(t1,t0))
        for i in range(1, len(sorted_edges)-1):
            t1 = Corner(sorted_vertices[i].x,sorted_vertices[i].y)
            self.corners.append(t0)
            self.straights.append(Straight(t0,t1))
            t0 = t1
        self.corners.append(t1)
        self.straights.append(Straight(t1,self.corners[0]))
        for i in range(len(self.straights)):
            self.straights[0].setPreviousStraight(self.straights[-1])
            self.straights[0].setNextStraight(self.straights[1])
            self.straights.rotate(1)
            self.corners[0].setPreviousStraight(self.straights[-1])
            self.corners[0].setNextStraight(self.straights[0])
            self.corners.rotate(1)

    def avg_straight_length(self):
        return sum([distance(self._element(s.startNode), self._element(s.endNode)) for s in self.straights])/len(self.straights)

    def starting_line(self):
        max_straight = max(self.straights, key=lambda s : distance(self._element(s.startNode), self._element(s.endNode))).id
        while self.straights[0].id != max_straight:
            self.straights.rotate(1)
            self.corners.rotate(1)
        self.straights[0].flagStart()

    def flag_dense_corners(self, tol=0.6, min_p=2):
        min_d = tol*self.avg_straight_length()
        i = 0
        while i < len(self.straights):
            group_spline = []
            id_ls = generator.uuid1().int
            s = self.straights[i]
            while(distance(self._element(s.startNode), self._element(s.endNode)) < min_d):
                group_spline.append(s)
                i = i + 1
                s = self.straights[i]
            else:
                i = i + 1
            if len(group_spline) > min_p:
                for s in group_spline:
                    s.flagSpline(id_ls)

    def plot_out(self, points=None):
        ext = self.straights
        plt.xlim(left=self.boundary._x_min(), right=self.boundary._x_max())
        plt.ylim(bottom=self.boundary._y_min(), top=self.boundary._y_max())
        for e in ext:
            v1 = self._element(e.startNode)
            v2 = self._element(e.endNode)
            plt.plot([v1.x, v2.x], [v1.y, v2.y], c="k", lw=1)
            if v1.spline:
                label1 = str(v1.spline)
                plt.annotate(label1,[v1.x, v1.y], textcoords="offset points", xytext=(0,10), ha='center')
        if points is not None:
            plt.plot([p[0] for p in points], [p[1] for p in points], c="r")
        plt.show()

    def plot_fill(self):
        ax = plt.axes()
        xs = [v.x for v in self.corners]
        ys = [v.y for v in self.corners]
        ax.fill(xs,ys,color="r")
        plt.show()

    def round(self, corner, previous_f=None):
        if previous_f and previous_f > 0.1:
            f = 1-previous_f
        else:
            f = random.uniform(0.1, 0.5)
        A = self._element(self._element(corner.previousStraight).startNode)
        B = corners
        C = self._element(self._element(corner.nextStraight).endNode)
        m1 = float(B.y-A.y)/float(B.x-A.x)
        m2 = float(B.y-C.y)/float(B.x-C.x)
        l1 = distance(A, B)
        l2 = distance(B, C)
        alfa = angle_3_points(A,B,C)
        r = f*math.tan(alfa/2.0)*min(l1, l2)
        t = r/math.tan(alfa/2.0)
        costan = lambda x: math.cos(math.atan(x))
        sintan = lambda x: math.sin(math.atan(x))
        if A.x > B.x:
            T1 = [B.x+t*costan(m1), B.y+t*sintan(m2)]
        elif A.x < B.x:
            T1 = [B.x-t*tcostan(m1), B.y-t*sintan(m2)]
        else:
            raise Exception("Two consecutive points were aligned vertically")
        if C.x > B.x:
            T2 = [B.x+t*costan(m2), B.y+t*sintan(m1)]
        elif C.x < B.x:
            T2 = [B.x-t*costan(m2), B.y-t*sintan(m1)]
        else:
            raise Exception("Two consecutive points were aligned vertically")
        C = [float(m2*T1[0] + m1*m2*T1[1] - m1*T2[x] - m1*m2*T2[1])/float(m2-m1), float(T2[0]+m2*T2[1] - T1[0] - m1*T1[0])/float(m2-m1)]
        corner.radius = r
        corner.center = C
        corner.arcStart = T1
        corner.arcFInish = T2
        corner.flagBlend()

track = Track([100,100],70, rand.randint(0,2**32-1))
track.select(0.5)
track.figure.plot(boundary = track.boundary)

# track.starting_line()
# track.flag_dense_corners()
# track.plot_out(track.corners)
track.plot_fill()
