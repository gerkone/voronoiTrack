from voronoi import *
from utils import *
import random as rand

boundary = Boundary(100, 100, 0.1)
vor = None
count = 0;
while vor is None and count < 20:
    count = count + 1
    try:
        vor = Vor(20, boundary)
    except TypeError:
        print("A cell had 2 sites associated for some reason.... (could be that 2 points are the same)")
vor._plot(boundary)
# vor.deleteElement(rand.choice(vor.cells))
# vor._plot(boundary)

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
