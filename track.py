from voronoi import *
from utils import *
import random as rand

boundary = Boundary(100, 100, 0.1)
vor = Vor(20, boundary)
vor.cleanup()
vor._plot(boundary, True)

#Select a random starting cell not out_of_bounds
# track_cells = []
# rnd = rand.randrange(len(vor.cells))
# if not vor.cells[rnd]._isOutOfBounds(boundary):
#     track_cells.append(vor.cells[rnd])

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
