# System defined imports
from scipy.spatial import Voronoi as VoronoiGenerator
from scipy.spatial import voronoi_plot_2d
import matplotlib.pyplot as plt
import numpy as np
import uuid as generator
import random
from datetime import datetime
from itertools import cycle

#User defined imports
from utils import *

class Vor:

    def __init__(self, npoints, boundary, seed):
        self.sites = []
        self.cells = []
        self.edges = []
        self.vertices = []
        self.seed = seed
        random.seed(self.seed)
        simple_log(datetime.now().strftime("[%d/%m/%Y %H:%M:%S]") + " " + str(seed) + "\n")
        randx = random.sample(range(boundary.x+1),npoints)  #random xs no repetition
        randy = random.sample(range(boundary.y+1),npoints)  #random ys no repetition
        for i in range(npoints):
            self.sites.append(Site(randx[i], randy[i]))
        vor = VoronoiGenerator([s._pos() for s in self.sites])
        #creating all voronoi vertices
        for v in vor.vertices:
            new_vertice = Vertex(v[0],v[1])
            self.vertices.append(new_vertice)
        #creating all voronoi edges
        for e in vor.ridge_vertices:
            if not -1 in e: #exclude imaginary edges
                new_edge = Edge(self.vertices[e[0]], self.vertices[e[1]])
                self.vertices[e[0]].connect_edge(new_edge)
                self.vertices[e[1]].connect_edge(new_edge)
                self.edges.append(new_edge)
        #creating all voronoi cells
        for c in vor.regions:
            if c != []:
                region_index = vor.regions.index(c)                             # the index relative to the current region
                site_index = np.where(vor.point_region == region_index)         # the index relative to the site of the current region
                found_site = self.sites[int(site_index[0])]                     # the site relative of the index
                if not -1 in c: #exclude immaginary cells()
                    new_cell = Cell([self.vertices[v] for v in c])
                    new_cell.connect_site(found_site)
                    for v in c:
                        self.vertices[v].connect_cell(new_cell)
                    self.sites[int(site_index[0])].connect_cell(new_cell)
                    self.cells.append(new_cell)
        for e in self.edges:
            cell_ids = intersect(get_by_ID(e.v1,self.vertices).cells, get_by_ID(e.v2,self.vertices).cells)
            e.cells = cell_ids
            for cid in cell_ids:
                self._element(cid).connect_edge(e)
        self.cleanup()

    def cleanup(self):
        for v in self.vertices:
            if len(v.edges) < 2:
                self.vertices.remove(v)
                self.delete_element(v)
        for e in self.edges:
            if e.v1 is None or e.v2 is None or len(e.cells) < 1:
                self.edges.remove(e)
                self.delete_element(e)
        for c in self.cells:
            if len(c.edges) != len(c.vertices) or len(self._adjacent_cells(c)) == 0:
                self.cells.remove(c)
                self.delete_element(c)

    def delete_element(self, element, cleanup=True):
        for e in self.edges:
            e.purge(element)
        for v in self.vertices:
            v.purge(element)
        for c in self.cells:
            c.purge(element)
        if cleanup:
            self.cleanup()

    def _adjacent_cells(self, cell):
        adj = []
        for edge_id in cell.edges:
            found_edge = self._element(edge_id)
            for cell_id in found_edge.cells:
                if cell_id != cell.id:
                    adj.append(self._element(cell_id))
        return adj

    def _filter_selected_cells(self):
        return [c for c in self.cells if c.selected]

    def _filter_outside_edges(self):
        ext = []
        for e in self.edges:
            i = 0
            for c in e.cells:
                cell = self._element(c)
                if cell.selected:
                    i = i + 1
            if i == 1:
                ext.append(e)
        return ext

    def _element(self, ID):
        element = get_by_ID(ID, self.cells)
        if element is not None:
            return element
        element = get_by_ID(ID, self.edges)
        if element is not None:
            return element
        element = get_by_ID(ID, self.vertices)
        if element is not None:
            return element
        element = get_by_ID(ID, self.sites)
        if element is not None:
            return element
        return None

    def sort(self, cell):
        eds = [self._element(vid) for vid in cell.edges]
        last = eds[0].v1
        next = eds[0].v2
        eds.pop(0)
        sorted_v = [last,next]
        sorted_e = [eds[0]]
        while len(eds) > 0 and next != last:
            t = None
            for e in eds:
                if e.v1 == next:
                    t = e.v2
                elif e.v2 == next:
                    t = e.v1
                if t is not None:
                    sorted_e.append(e)
                    if t not in sorted_v:
                        sorted_v.append(t)
                    eds.remove(e)
                    next = t
                    break
            if t is None:
                return None, None
        return sorted_e, [self._element(v_id) for v_id in sorted_v]

    def _area(self,cell):
        val = 0
        _, vs = self.sort(cell)
        if vs is not None:
            j = len(vs) - 1
            for i in range(len(vs)):
                val = val + (vs[j].x + vs[i].x) * (vs[j].y - vs[i].y)
                j = i
            return abs(val)/2
        else:
            return None

    def _perimeter(self, cell):
        _edge = lambda e: get_by_ID(e,self.edges)
        return sum(distance(_edge(e).v1, _edge(e).v2)*len(e.cells) for e in cell.edges)

    def plot_only_selected(self, boundary=None):
        if boundary:
            ax = plt.axes()
            cells = self._filter_selected()
            for c in cells:
                xs = [self._element(v).x for v in c.vertices]
                ys = [self._element(v).y for v in c.vertices]
                ax.fill(xs,ys,color="r")
        plt.show()

    def plot(self, boundary=None):
        if boundary:
            plt.xlim(left=boundary._x_min(), right=boundary._x_max())
            plt.ylim(bottom=boundary._y_min(), top=boundary._y_max())
        plt.plot([s.x for s in self.sites], [s.y for s in self.sites], "ko", ms=2)  #plot of sites
        for e in self.edges:    #plot of edges
            v1 = self._element(e.v1)
            v2 = self._element(e.v2)
            plt.plot([v1.x, v2.x], [v1.y, v2.y], "k", lw=1)
        plt.plot([v.x for v in self.vertices], [v.y for v in self.vertices], "ko", ms=4) #plot of vertices
        cycol = cycle('bcmy')
        ax = plt.axes()
        for c in self.cells:
            xs = [self._element(v).x for v in c.vertices]
            ys = [self._element(v).y for v in c.vertices]
            if c.selected and not c.center:
                ax.fill(xs,ys,color="r")
            elif c.selected and c.center:
                ax.fill(xs,ys,color="g")
            else:
                ax.fill(xs,ys,color=next(cycol))
        plt.show()

    def _is_out_of_bounds(self, element, boundary):
        if element.__class__.__name__ == "Cell":
            cell = self._element(element.id)
            return any( self._element(v)._is_out_of_bounds(boundary) for v in cell.vertices )
        if element.__class__.__name__ == "Edge":
            edge = self._element(element.id)
            return (self._element(edge.v1)._is_out_of_bounds(boundary) or self._element(edge.v2)._is_out_of_bounds(boundary))
        if element.__class__.__name__ == "Vertex":
            vertice = self._element(element.id)
            return vertice._is_out_of_bounds(boundary)
        if element.__class__.__name__ == "Site":
            return False
        return None

class Site:

    # id
    # x
    # y
    # cell

    def __init__(self, x, y):
        self.id = generator.uuid1().int
        self.x = x
        self.y = y

    def connect_cell(self, cell):
        self.cell = cell.id

    def _pos(self):
        return [self.x, self.y]

    def __str__(self):
        return str(self.id) + ": x= " + str(self.x) + ", y=" + str(self.y) + ", cell=" + str(self.cell)

class Boundary:

    # x
    # y
    # factor

    def __init__(self, x, y, factor):
        self.x = x
        self.y = y
        self.factor = factor

    def _x_max(self):
        return self.x*(1 + self.factor)

    def _y_max(self):
        return self.y*(1 + self.factor)

    def _x_min(self):
        return self.x*(-self.factor)

    def _y_min(self):
        return self.y*(-self.factor)

class Cell:

    # id
    # site
    # edges
    # vertices

    def __init__(self, vertices):
        self.id = generator.uuid1().int
        self.vertices = [v.id for v in vertices]
        self.edges = []
        self.site = None
        self.selected = False
        self.center = False

    def connect_edge(self, edge):
        if (edge.id not in self.edges):
            self.edges.append(edge.id)

    def connect_site(self, site):
        self.site = site.id

    def purge(self, element):
        self.vertices = list(filter(lambda v: v != element.id, self.vertices))
        self.edges = list(filter(lambda e: e != element.id, self.edges))

    def flag_selected(self):
        self.selected = True

    def flag_center(self):
        self.center = True

    def __str__(self):
        return str(self.id) + ": site= " + str(self.site)

class Edge:

    # id
    # v1
    # v2
    # cells

    def __init__(self, V1, V2):
        self.id = generator.uuid1().int
        self.v1 = V1.id
        self.v2 = V2.id
        self.cells = []

    def connect_cell(self, cell):
        if cell.id not in self.cells:
            self.cells.append(cell.id)

    def purge(self, element):
        self.cells = list(filter(lambda c: c != element.id, self.cells))
        if self.v1 == element.id:
            self.v1 = None
        if self.v2 == element.id:
            self.v2 = None

    def _connected_to_cell(self, cell):
        return (cell.id in self.cells)

    def __str__(self):
        return str(self.id) + ": v1=" + str(self.v1) + ": v2=" + str(self.v2)

class Vertex:

    # id
    # x
    # y
    # edges
    # cells

    def __init__(self, X, Y):
        self.id = generator.uuid1().int
        self.x = X
        self.y = Y
        self.edges = []
        self.cells = []

    def connect_edge(self, edge):
        self.edges.append(edge.id)

    def connect_cell(self, cell):
        if cell.id not in self.cells:
            self.cells.append(cell.id)

    def purge(self, element):
        self.cells = list(filter(lambda c: c != element.id, self.cells))
        self.edges = list(filter(lambda e: e != element.id, self.edges))

    def _equal(self, v):
        return (v.id == self.id)

    def _pos(self):
        return [self.x, self.y]

    def _connected_to_edge(self, edge):
        return (edge.id in self.edges)

    def _connected_to_cell(self, cell):
        return (cell.id in self.cells)

    def __str__(self):
        return str(self.id) + ": x= " + str(self.x) + ", y= " + str(self.y)

    def _is_out_of_bounds(self, boundary):
        return (self.x > boundary._x_max() or self.x < boundary._x_min() or self.y > boundary._y_max() or self.y < boundary._y_min())
