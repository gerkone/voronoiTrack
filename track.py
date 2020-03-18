from voronoi import *
from utils import *
import random as rand

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

track = Track([100,100],70)

track.figure._plot(track.boundary)

#Select a random starting cell not out_of_bounds

#continuiamo a scegliere celle adiacenti non out_of_bounds fino a che non raggiungiamo il p% delle celle totali non out_of_bounds

#eliminiamo i pnti e gli spigoli interni

#rimuoviamo eventuali punti troppo allineati

#scorriamo il tracciato per trovare trovare zone dense

#riordiniamo i punti dalla linea di partenza alla linea di arrivo

#flaggiamo quei punti come "splinare"

#arrotondiamo i punti rimanenti creando i punti: center, start e finish

#addensiamo i segmenti e le circonferenze non splinate

#spliniamo i punti marcati come "splinare"

#offset del tracciato
