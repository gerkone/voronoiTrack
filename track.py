import random as rand
import scipy
import math
from collections import deque
import matplotlib.pyplot as plt

from voronoi import *
from utils import *
from sectors import *

BOUNDARY_DEFAULT_SCALE = 0.1

class Track:

    # straights = [] of obj corner
    # corners = [] of obj corner

    def __init__(self, boundary, npoints, seed, verbose=False, scale=BOUNDARY_DEFAULT_SCALE):
        self.boundary = Boundary(boundary[0],boundary[1], scale)
        self.figure = Vor(npoints, self.boundary,seed)
        for el in self.figure.vertices:
            if(el._is_out_of_bounds(self.boundary)):
                self.figure.delete_element(el, False)
        self.figure.cleanup()
        self.straights = []
        self.corners = []

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
        return None

    def select_bfs(self, perc):
        areaTot = sum([self.figure._area(c) for c in self.figure.cells])
        toCover = areaTot * perc
        covered = 0
        q = deque([rand.choice(self.figure.cells)])
        q[0].flag_center()
        while len(q) > 0:
            el = q.popleft()
            covered = covered + self.figure._area(el)
            if toCover < covered:
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
        figurePoints = []
        randPoint = lambda : np.array((random.randint(0, self.boundary.x+1) * perc - 50 * perc +50, random.randint(0, self.boundary.y+1) * perc - 50 * perc +50))
        figurePoints.append(randPoint())
        figurePoints.append(randPoint())
        figurePoints.append(randPoint())
        convex = scipy.spatial.ConvexHull(figurePoints, incremental=True)
        while len(convex.vertices) < n:
            convex.add_points([randPoint()])
        convex.close()
        for v in self.figure.vertices:
            if in_hull([[v.x,v.y]], [convex.points[i] for i in convex.vertices])[0]:
                for c in v.cells:
                    (self.figure._element(c)).flag_selected()

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
        track_cell = Cell([self.figure._element(v) for v in vertices])  #single cell representing the track
        for e in out_edges:
            track_cell.connect_edge(e)
        sorted_edges, sorted_vertices = self.figure.sort(track_cell)

        # t1 = Corner(sorted_vertices[-1].x,sorted_vertices[-1].y)
        # t0 = Corner(sorted_vertices[0].x,sorted_vertices[0].y)
        # self.corners.append(t1)
        # self.straights.append(Straight(t1,t0))
        # for i in range(1, len(sorted_edges)-1):
        #     t1 = Corner(sorted_vertices[i].x,sorted_vertices[i].y)
        #     self.corners.append(t0)
        #     self.straights.append(Straight(t0,t1))
        #     t0 = t1
        # self.straights.append(Straight(t1,self.corners[0]))

    # def plot_out(self):
    #     ext = self.figure._filter_outside_edges()
    #     plt.xlim(left=self.boundary._x_min(), right=self.boundary._x_max())
    #     plt.ylim(bottom=self.boundary._y_min(), top=self.boundary._y_max())
    #     for e in ext:
    #         v1 = self.figure._element(e.v1)
    #         v2 = self.figure._element(e.v2)
    #         plt.plot([v1.x, v2.x], [v1.y, v2.y], "k", lw=1)
    #     plt.show()


    def plot_out(self):
        ext = self.straights
        plt.xlim(left=self.boundary._x_min(), right=self.boundary._x_max())
        plt.ylim(bottom=self.boundary._y_min(), top=self.boundary._y_max())
        for e in ext:
            v1 = self._element(e.startNode)
            v2 = self._element(e.endNode)
            plt.plot([v1.x, v2.x], [v1.y, v2.y], "k", lw=1)
            label1 = "start"
            plt.annotate(label1,[v1.x, v1.y], textcoords="offset points", xytext=(0,10), ha='center')
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
        alfa = math.acos(((B.x-A.x)*(B.x-C.x)+(B.y-A.y)*(B.y-C.y))/float(l1*l2))
        r = f*math.tan(alfa/2.0)*min(l1, l2)
        t = r/math.tan(alfa/2.0)
        costan = lambda x: math.cos(math.atan(x))
        sintan = lambda x: math.sin(math.atan(x))
        if A.x > B.x:
            T1 = [B.x+t*costan(m1), B.y+t*sintan(m2)]
        elif A.x < B.x:
            T1 = [B.x-t*tcostan(m1), B.y-t*sintan(m2)]
        else:
            raise Exception("Two consecutive points where aligned vertically")
        if C.x > B.x:
            T2 = [B.x+t*costan(m2), B.y+t*sintan(m1)]
        elif C.x < B.x:
            T2 = [B.x-t*costan(m2), B.y-t*sintan(m1)]
        else:
            raise Exception("Two consecutive points where aligned vertically")
        C = [float(m2*T1[0] + m1*m2*T1[1] - m1*T2[x] - m1*m2*T2[1])/float(m2-m1), float(T2[0]+m2*T2[1] - T1[0] - m1*T1[0])/float(m2-m1)]
        corner.radius = r
        corner.center = C
        corner.arcStart = T1
        corner.arcFInish = T2
        corner.flagBlend()

track = Track([100,100],70,rand.randint(0,2**32-1))
track.select(0.5)
# track.figure.plot(boundary = track.boundary)
print(str(len(track.straights)))
print(str(len(track.corners)))
track.plot_out()
# track.plot_fill()



#select a percentage of the cells in the figure

#eliminiamo i pnti e gli spigoli interni

#rimuoviamo eventuali punti troppo allineati

#scorriamo il tracciato per trovare trovare zone dense

#riordiniamo i punti dalla linea di partenza alla linea di arrivo

#flaggiamo quei punti come "splinare"

#arrotondiamo i punti rimanenti creando i punti: center, start e finish

#addensiamo i segmenti e le circonferenze non splinate

#spliniamo i punti marcati come "splinare"

#offset del tracciato
