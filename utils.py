# import pyclipper
import math

def distance(q1,q2):
	((q1.x - q2.x)**2 + (q1.y - q2.y)**2)**0.5

def intersect(L1,L2):
	t = set(L2)
	LI = [x for x in L1 if x in t]
	return LI

def get_by_ID(id,L):
	for el in L:
		if el.id == id:
			return el
	return None

def simple_log(data, filename="seeds.log"):
	with open(filename, 'a') as f:
		f.write(data)

def in_hull(p, hull):
    from scipy.spatial import Delaunay
    if not isinstance(hull,Delaunay):
        hull = Delaunay(hull)

    return hull.find_simplex(p)>=0

def angle_3_points(A, B, C):
	l1 = distance(A, B)
	l2 = distance(B, C)
	return math.acos(((B.x-A.x)*(B.x-C.x)+(B.y-A.y)*(B.y-C.y))/float(l1*l2))

# def offset(points, offset):
# 	pco = pyclipper.PyclipperOffset()
# 	pco.AddPath([[p.x, p.y] for p in points], pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
# 	return pco.Execute(offset)
