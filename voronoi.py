from scipy.spatial import Voronoi as VoronoiGenerator
from scipy.spatial import voronoi_plot_2d
import matplotlib.pyplot as plt
import numpy as np
import math
import uuid as generator
import random

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
            cell_ids = intersect(get_by_ID(e.v1.id,self.vertices).cells, get_by_ID(e.v2.id,self.vertices).cells)
            e.cells = cell_ids

    def _adjacentCells(self, cell):
        adj = []
        for edge_id in cell.edges:
            found_edge = get_by_ID(edge_id, self.edges)
            for c in found_edge.cells:
                if not c == cell.id
                    adj.append([get_by_ID(c, self.cells), found_edge])
        return adj

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
        self.vertices = []

    def connectEdge(self, edge):
        if (edge.id not in self.edges):
            self.edges.append(edge.id)

    def connectSite(self, site):
        self.site = site.id

    def _isOutOfBounds(self, boundary):
        return any( (v.x > boundary._x_max() or v.y > boundary._y_max() or v.x < boundary._x_min() or v.y < boundary._y_min() ) for v in self.vertices)

    def __str__(self):
        return str(self.id) + ": site= " + str(self.site)

class Edge:

    # id
    # v1
    # v2
    # cells

    def __init__(self, V1, V2):
        self.id = generator.uuid1().int
        self.v1 = V1
        self.v2 = V2
        self.cells = []

    def connectCell(self, cell):
        if cell.id not in self.cells:
            self.cells.append(cell.id)

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
