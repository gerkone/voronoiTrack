def intersect(L1,L2):
	t = set(L2)
	LI = [x for x in L1 if x in t]
	return LI

def get_by_ID(id,L):
	for el in L:
		if el.id == id:
			return el
	return None
