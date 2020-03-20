from voronoi import *
from utils import *
import random as rand
from collections import deque
import matplotlib.pyplot as plt

BOUNDARY_DEFAULT_SCALE = 0.1

class Track:

    # track = []

    def __init__(self, boundary, npoints, seed, verbose=False, scale=BOUNDARY_DEFAULT_SCALE):
        self.track = []
        self.boundary = Boundary(boundary[0],boundary[1], scale)
        self.figure = Vor(npoints, self.boundary,seed)
        for el in self.figure.vertices:
            if(el._is_out_of_bounds(self.boundary)):
                self.figure.delete_element(el, False)
        self.figure.cleanup()

    def select(self, perc, method="sum"):
        if method == "sum":
            areaTot = sum([self.figure._area(c) for c in self.figure.cells])
        elif method == "boudary":
            areaTot = (self.boundary._x_max() - self.boundary._x_min())*(self.boundary._y_max() - self.boundary._y_min())
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

track = Track([100,100],70,rand.randint(0,2**32-1))
# track.figure._plot(boundary = track.boundary)
track.select(0.5)
track.figure.plot(boundary = track.boundary)

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
