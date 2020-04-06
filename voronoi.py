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
        self.sites = {}
        self.cells = {}
        self.edges = {}
        self.vertices = {}
        self.seed = seed
        random.seed(self.seed)
        randx = random.sample(range(boundary.x+1),npoints)  #random xs no repetition
        randy = random.sample(range(boundary.y+1),npoints)  #random ys no repetition
        for i in range(npoints):
            id = generator.uuid1().int
            self.sites[id] = (Site(randx[i], randy[i], id))
        #creating the voronoi diagram
        vor = VoronoiGenerator([s._pos() for s in list(self.sites.values())])
        #gtting all voronoi vertices
        for v in vor.vertices:
            id = generator.uuid1().int
            new_vertex = Vertex(v[0],v[1], id)
            self.vertices[id] = new_vertex
        #getting all voronoi edges
        for e in vor.ridge_vertices:
            if not -1 in e: #exclude imaginary edges
                id = generator.uuid1().int
                new_edge = Edge(list(self.vertices.values())[e[0]], list(self.vertices.values())[e[1]], id)
                self.vertices[list(self.vertices.keys())[e[0]]].connect_edge(new_edge)
                self.vertices[list(self.vertices.keys())[e[1]]].connect_edge(new_edge)
                self.edges[id] = new_edge
        #getting all voronoi cells
        for c in vor.regions:
            if c != []:
                region_index = vor.regions.index(c)                             # the index relative to the current region
                site_index = np.where(vor.point_region == region_index)         # the index relative to the site of the current region
                found_site = list(self.sites.values())[int(site_index[0])]             # the site relative of the index
                if not -1 in c: #exclude immaginary cells()
                    id = generator.uuid1().int
                    new_cell = Cell([list(self.vertices.values())[v] for v in c], id)
                    new_cell.connect_site(found_site)
                    for v in c:
                        self.vertices[list(self.vertices.keys())[v]].connect_cell(new_cell)
                    self.sites[list(self.sites.keys())[int(site_index[0])]].connect_cell(new_cell)
                    self.cells[id] = new_cell
        for k in self.edges.keys():
            cell_ids = self._intersect(self.vertices.get(self.edges[k].v1).cells, self.vertices.get(self.edges[k].v2).cells)
            self.edges[k].cells = cell_ids
            for cid in cell_ids:
                self.cells.get(cid).connect_edge(self.edges[k])
        self.cleanup()

    def _intersect(self,L1,L2):
    	t = set(L2)
    	LI = [x for x in L1 if x in t]
    	return LI

    #bug if there are two or more detached cells (condition of 0 adjacent cells is passed)
    def cleanup(self):
        for v_key in list(self.vertices.keys()):
            el = self.vertices.get(v_key)
            if el is not None:
                if len(el.edges) < 2:
                    del self.vertices[v_key]
                    self.delete_element(v_key)
        for e_key in list(self.edges.keys()):
            el = self.edges.get(e_key)
            if el is not None:
                if el.v1 is None or el.v2 is None or len(el.cells) < 1:
                    del self.edges[e_key]
                    self.delete_element(e_key)
        for c_key in list(self.cells.keys()):
            el = self.cells.get(c_key)
            if el is not None:
                adj = self._adjacent_cells(el)
                if len(el.edges) != len(el.vertices) or len(adj) == 0:
                    del self.cells[c_key]
                    self.delete_element(c_key)


    def delete_element(self, key, cleanup=True):
        for e in self.edges.values():
            e.purge(key)
        for v in self.vertices.values():
            v.purge(key)
        for c in self.cells.values():
            c.purge(key)
        if cleanup:
            #recursive cleanup
            self.cleanup()

    def _adjacent_cells(self, cell):
        adj = []
        for edge_id in cell.edges:
            found_edge = self.edges.get(edge_id)
            for cell_id in found_edge.cells:
                if cell_id != cell.id:
                    adj.append(self.cells.get(cell_id))
        return adj

    def _filter_selected_cells(self):
        return [c for c in list(self.cells.values()) if c.selected]

    def _filter_outside_edges(self):
        ext = []
        for e in self.edges.values():
            i = 0
            for c in e.cells:
                cell = self.cells.get(c)
                if cell.selected:
                    i = i + 1
            #external edge iff selected by only one cell
            if i == 1:
                ext.append(e)
        return ext

    def sort(self, cell):
        eds = [self.edges.get(vid) for vid in cell.edges]
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
        return sorted_e, [self.vertices.get(v_id) for v_id in sorted_v]

    def _area(self,cell):
        """
        Gauss method for area of a shape in coordinate geometry
        """
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
        return sum(distance(self.edges.get(e).v1, self.edges.get(e).v2) for e in cell.edges)

    def plot_only_selected(self, boundary=None):
        if boundary:
            ax = plt.axes()
            cells = self._filter_selected()
            for c in cells:
                xs = [self.vertices.get(v).x for v in c.vertices]
                ys = [self.vertices.get(v).y for v in c.vertices]
                ax.fill(xs,ys,color="r")
        plt.show()

    def plot(self, boundary=None):
        if boundary:
            plt.xlim(left=boundary._x_min(), right=boundary._x_max())
            plt.ylim(bottom=boundary._y_min(), top=boundary._y_max())
        #plot sites
        plt.plot([s.x for s in list(self.sites.values())], [s.y for s in list(self.sites.values())], "ko", ms=2)
        #plot edges
        for e in self.edges.values():
            v1 = self.vertices.get(e.v1)
            v2 = self.vertices.get(e.v2)
            plt.plot([v1.x, v2.x], [v1.y, v2.y], "k", lw=1)
        #plot vertices
        plt.plot([v.x for v in list(self.vertices.values())], [v.y for v in list(self.vertices.values())], "ko", ms=4)
        cycol = cycle('bcmy')
        ax = plt.axes()
        #coloring cells
        for c in self.cells.values():
            xs = [self.vertices.get(v).x for v in c.vertices]
            ys = [self.vertices.get(v).y for v in c.vertices]
            if c.selected and not c.center:
                ax.fill(xs,ys,color="r")
            elif c.selected and c.center:
                ax.fill(xs,ys,color="g")
            else:
                ax.fill(xs,ys,color=next(cycol))
        plt.show()

    def _is_out_of_bounds(self, element, boundary):
        if element.__class__.__name__ == "Cell":
            cell = self.cells.get(element.id)
            return any( self._element(v)._is_out_of_bounds(boundary) for v in cell.vertices )
        if element.__class__.__name__ == "Edge":
            edge = self.edges.get(element.id)
            return (self._element(edge.v1)._is_out_of_bounds(boundary) or self._element(edge.v2)._is_out_of_bounds(boundary))
        if element.__class__.__name__ == "Vertex":
            vertex = self.vertices.get(element.id)
            return vertex._is_out_of_bounds(boundary)
        if element.__class__.__name__ == "Site":
            return False
        return None

class Site:

    # id
    # x
    # y
    # cell

    def __init__(self, x, y, id):
        self.id = id
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

    def __init__(self, vertices, id):
        self.id = id
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

    def purge(self, key):
        self.vertices = list(filter(lambda v: v != key, self.vertices))
        self.edges = list(filter(lambda e: e != key, self.edges))

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

    def __init__(self, V1, V2,id):
        self.id = id
        self.v1 = V1.id
        self.v2 = V2.id
        self.cells = []

    def connect_cell(self, cell):
        if cell.id not in self.cells:
            self.cells.append(cell.id)

    def purge(self, key):
        self.cells = list(filter(lambda c: c != key, self.cells))
        if self.v1 == key:
            self.v1 = None
        if self.v2 == key:
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

    def __init__(self, X, Y, id):
        self.id = id
        self.x = X
        self.y = Y
        self.edges = []
        self.cells = []

    def connect_edge(self, edge):
        self.edges.append(edge.id)

    def connect_cell(self, cell):
        if cell.id not in self.cells:
            self.cells.append(cell.id)

    def purge(self, key):
        self.cells = list(filter(lambda c: c != key, self.cells))
        self.edges = list(filter(lambda e: e != key, self.edges))

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
