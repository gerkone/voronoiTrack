from utils import *
import numpy as np

class Offstpoly:
    def __init__(self,inner):
        self.poly = []
        self.inner = inner

    def _bitan(self, a, b, r,):
        """
        finds the bitangent line to the circles centered in two consequential corners (a,b).
        returns the coefficients and the lht.
        """
        t = angle_of(a,b)
        # if in_hull([a[0]-r*math.sin(t),a[1]+r*math.cos(t)], self.inner):
        #     s = -1
        # else:
        #     s = 1
        s = 1
        return math.tan(t), (a[1]+s*r*math.cos(t) - math.tan(t)*(a[0]-s*r*math.sin(t)))

    def _offset_2_edges(self,e1,e2,radius):
        """
        finds the intersect point of the offset edges, adds it to the offset poly
        """
        k1, b1 = self._bitan(e1[0],e1[1],radius)
        k2, b2 = self._bitan(e2[0],e2[1],radius)

        x_s = np.linalg.solve(np.array([[-k1,1], [-k2,1]]), np.array([b1,b2]))
        self.poly.append(x_s)

    def offset_loop(self, radius):
        #minimum lenght of a single straight, prevents overlapping ( temporary )
        
        min_s = 2
        i1 = 0
        i2 = 1
        i3 = 2
        l = len(self.inner)
        while i1 != l-1:
            c1 = self.inner[i1]
            c2 = self.inner[i2]
            c3 = self.inner[i3]
            # if distance(c1,c2) < min_s*radius:
               
            if distance(c2,c3) < min_s*radius:
                #leap a edge
                i3 = (i3 + 1)%l
                c4 = self.inner[i3]
                self._offset_2_edges([c1,c2], [c3,c4], radius)
                i1 = i1 + 2
                i2 = (i2 + 2)%l
                i3 = (i3 + 1)%l
            else:
                self._offset_2_edges([c1,c2], [c2,c3], radius)
                i1 = i1 + 1
                i2 = (i2 + 1)%l
                i3 = (i3 + 1)%l
        print(self.poly)