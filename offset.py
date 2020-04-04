from utils import *
import numpy as np

class Offstpoly:
    def __init__(self, poly):
        self.poly = []

    def _bitan(self,a,b,r):
        """
        finds the bitangent line to the circles centered in two consequential corners (a,b).
        returns the coefficients and the lht.
        """
        t = angle_of(a,b)
        return (math.tan(t)), ((a[1]+r*math.cos(t)) + math.tan(t)*(a[0]-r*math.sin(t)))

    def _offset_2_edges(self,a,b,c,radius):
        """
        finds the intersect point of the offset edges, adds it to the offset poly
        """
        k1, b1 = self._bitan(a,b,radius)
        k2, b2 = self._bitan(b,c,radius)
        x_s = np.linalg.solve(np.array(k1,k2),np.array(b1,b2))
        self.poly.append([x_s,(x_s*k1+b1)])

    def offset_loop(self, inner, radius):
        #minimum lenght of a single straight, prevents overlapping ( temporary )
        min_s = 0.5
        i1 = 0
        i2 = 1
        i3 = 2
        l = len(inner)
        while i1 != l-1:
            c1 = inner[i1]
            c2 = inner[i2]
            c3 = inner[i3]
            if distance(c1,c2) < min_s*radius or distance(c2,c3) < min_s*radius:
                pass
            else:
                self._offset_2_edges(c1,c2,c3,radius)
            i1 = i1 + 1
            i2 = (i2 + 1)%l
            i3 = (i3 + 1)%l