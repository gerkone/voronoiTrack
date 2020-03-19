from voronoi import *
from utils import *
import random as rand
from collections import deque

BOUNDARY_DEFAULT_SCALE = 0.1

class Track:

    # track = []

    def __init__(self, boundary, npoints, verbose=False, scale=BOUNDARY_DEFAULT_SCALE):
        self.track = []
        self.boundary = Boundary(boundary[0],boundary[1], scale)
        self.figure = Vor(npoints, self.boundary)
        for el in self.figure.vertices:
            if(el._isOutOfBounds(self.boundary)):
                self.figure.deleteElement(el, False)
        self.figure.cleanup()

    def selectTrackArea(self, perc, delete=True):
        print("there are "+str(len(self.figure.cells))+" cells in total")
        selected = []
        q = deque()
        q.append(rand.choice(self.figure.cells))
        # print("adding first cell to queue")
        while float(len(selected))/len(self.figure.cells) < perc:
            examined_cell = q.popleft()
            # print("popping cell from queue")
            # print("queue length is now " + str(len(q)))
            adjacent_cells = self.figure._adjacentCells(examined_cell)
            # print("found "+str(len(adjacent_cells)) +" adjacent cells")
            for adjacent_cell in adjacent_cells:
                if adjacent_cell not in q:
                    # print("adding adjacent cell to queue")
                    q.append(adjacent_cell)
                else:
                    # print("found a cell that was already added")
                    pass
            selected.append(examined_cell)
            # print("selected is now "+str(len(selected)))
            # print("queue is now "+str(len(q)))
            # print("current coverage factor is "+ str(float(len(selected))/len(self.figure.cells)))
        print("selected is now "+str(len(selected)))
        print("queue is now "+str(len(q)))
        print("current coverage factor is "+ str(float(len(selected))/len(self.figure.cells)))
        q.clear()

track = Track([100,100],70)
track.figure._plot(boundary = track.boundary)

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
