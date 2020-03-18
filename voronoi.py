# System defined imports
from scipy.spatial import Voronoi as VoronoiGenerator
from scipy.spatial import voronoi_plot_2d
import matplotlib.pyplot as plt
import numpy as np
import math
import uuid as generator
import random

#User defined imports
from utils import *

class Vor:

    def __init__(self, npoints, boundary):
        self.sites = []
        self.cells = []
        self.edges = []
        self.vertices = []
        for i in range(npoints):
            self.sites.append(Site(random.randint(0,boundary.x), random.randint(0, boundary.y)))
        vor = VoronoiGenerator([s._pos() for s in self.sites])
        #creating all voronoi vertices
        for v in vor.vertices:
            new_vertice = Vertice(v[0],v[1])
            self.vertices.append(new_vertice)
        #creating all voronoi edges
        for e in vor.ridge_vertices:
            if not -1 in e: #exclude imaginary edges
                new_edge = Edge(self.vertices[e[0]], self.vertices[e[1]])
                self.vertices[e[0]].connectEdge(new_edge)
                self.vertices[e[1]].connectEdge(new_edge)
                self.edges.append(new_edge)
        #creating all voronoi cells
        for c in vor.regions:
            if c != []:
                region_index = vor.regions.index(c)                             # the index relative to the current region
                site_index = np.where(vor.point_region == region_index)         # the index relative to the site of the current region
                found_site = self.sites[int(site_index[0])]                     # the site relative of the index
                if not -1 in c: #exclude immaginary cells()
                    new_cell = Cell([self.vertices[v] for v in c])
                    new_cell.connectSite(found_site)
                    for v in c:
                        self.vertices[v].connectCell(new_cell)
                    self.sites[int(site_index[0])].connectCell(new_cell)
                    self.cells.append(new_cell)
        for e in self.edges:
            cell_ids = intersect(get_by_ID(e.v1,self.vertices).cells, get_by_ID(e.v2,self.vertices).cells)
            e.cells = cell_ids
        self.cleanup()

    def cleanup(self):
        toRemove = []
        for i in range(len(self.edges)):
            if len(self.edges[i].cells) == 0 or self.edges[i].v1 == None or self.edges[i].v2 == None:
                toRemove.append(i)
        for i in reversed(toRemove):
            self.edges.pop(i)
        toRemove = []
        for i in range(len(self.vertices)):
            if len(self.vertices[i].cells) == 0 or len(self.vertices[i].edges) < 2:
                toRemove.append(i)
        for i in reversed(toRemove):
            self.vertices.pop(i)
        toRemove = []
        for i in range(len(self.cells)):
            if len(self.cells[i].vertices) < 3 or len(self.cells[i].edges) < 3:
                toRemove.append(i)
        for i in reversed(toRemove):
            self.cells.pop(i)

    def deleteElement(self, element, cleanup=True):
        for e in self.edges:
            e.purge(element)
        for v in self.vertices:
            v.purge(element)
        for c in self.cells:
            c.purge(element)
        if cleanup:
            self.cleanup()

    def _adjacentCells(self, cell):
        adj = []
        for edge_id in cell.edges:
            found_edge = get_by_ID(edge_id, self.edges)
            for c in found_edge.cells:
                if not c == cell.id:
                    adj.append([get_by_ID(c, self.cells), found_edge])
        return adj

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

    def _plot(self, boundary=None):
        if boundary:
            plt.xlim(left=boundary._x_min(), right=boundary._x_max())
            plt.ylim(bottom=boundary._y_min(), top=boundary._y_max())
        plt.plot([s.x for s in self.sites], [s.y for s in self.sites], "ro", ms=2)
        for e in self.edges:
            v1 = self._element(e.v1)
            v2 = self._element(e.v2)
            plt.plot([v1.x, v2.x], [v1.y, v2.y], "k", lw=1)
        plt.plot([v.x for v in self.vertices], [v.y for v in self.vertices], "go", ms=4)
        plt.show()

    def _is_out_of_bounds(self, element, boundary):
        if element.__class__.__name__ == "Cell":
            cell = self._element(element.id)
            return any( self._element(v)._isOutOfBounds(boundary) for v in cell.vertices )
        if element.__class__.__name__ == "Edge":
            edge = self._element(element.id)
            return (self._element(edge.v1)._isOutOfBounds(boundary) or self._element(edge.v2)._isOutOfBounds(boundary))
        if element.__class__.__name__ == "Vertice":
            vertice = self._element(element.id)
            return vertice._isOutOfBounds(boundary)
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

    def connectCell(self, cell):
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

    def connectEdge(self, edge):
        if (edge.id not in self.edges):
            self.edges.append(edge.id)

    def connectSite(self, site):
        self.site = site.id

    def purge(self, element):
        self.vertices = filter(lambda v: v != element.id, self.vertices)
        self.edges = filter(lambda e: e != element.id, self.edges)

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

    def connectCell(self, cell):
        if cell.id not in self.cells:
            self.cells.append(cell.id)

    def purge(self, element):
        self.edges = filter(lambda e: e != element.id, self.edges)
        if self.v1 == element.id:
            self.v1 = None
        if self.v2 == element.id:
            self.v2 = None

    def _length(self):
        return sqrt((v1.x - v2.x)**2 + (v1.y - v2.y)**2)

    def _angle(self):
        return math.degree(math.atan((v1.y - v2.y)/(v1.x - v2.x)))

    def _vertices(self):
        return [self.v1, self.v2]

    def _connectedToCell(self, cell):
        return (cell.id in self.cells)

    def __str__(self):
        return str(self.id) + ": v1=" + str(self.v1) + ": v2=" + str(self.v2)

class Vertice:

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

    def connectEdge(self, edge):
        self.edges.append(edge.id)

    def connectCell(self, cell):
        if cell.id not in self.cells:
            self.cells.append(cell.id)

    def purge(self, element):
        self.cells = filter(lambda c: c != element.id, self.cells)
        self.edges = filter(lambda e: e != element.id, self.edges)

    def _equal(self, v):
        return (v.id == self.id)

    def _pos(self):
        return [self.x, self.y]

    def _connectedToEdge(self, edge):
        return (edge.id in self.edges)

    def _connectedToCell(self, cell):
        return (cell.id in self.cells)

    def __str__(self):
        return str(self.id) + ": x= " + str(self.x) + ", y= " + str(self.y)

    def _isOutOfBounds(self, boundary):
        return (self.x > boundary._x_max() or self.x < boundary._x_min() or self.y > boundary._y_max() or self.y < boundary._y_min())
