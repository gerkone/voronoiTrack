from voronoi import *
from utils import *
import random as rand
import scipy
from collections import deque
import matplotlib.pyplot as plt

BOUNDARY_DEFAULT_SCALE = 0.1

class Track:

    # track = []
    # straights = []
    # corners_tips = []

    def __init__(self, boundary, npoints, seed, verbose=False, scale=BOUNDARY_DEFAULT_SCALE):
        self.track = []
        self.boundary = Boundary(boundary[0],boundary[1], scale)
        self.figure = Vor(npoints, self.boundary,seed)
        for el in self.figure.vertices:
            if(el._is_out_of_bounds(self.boundary)):
                self.figure.delete_element(el, False)
        self.figure.cleanup()

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

    def plot_out(self):
        ext = self.figure._filter_outside_edges()
        plt.xlim(left=self.boundary._x_min(), right=self.boundary._x_max())
        plt.ylim(bottom=self.boundary._y_min(), top=self.boundary._y_max())
        for e in ext:
            v1 = self.figure._element(e.v1)
            v2 = self.figure._element(e.v2)
            plt.plot([v1.x, v2.x], [v1.y, v2.y], "k", lw=1)
        plt.show()

track = Track([100,100],70,rand.randint(0,2**32-1))
track.select(0.5)
track.figure.plot(boundary = track.boundary)
track.plot_out()
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
