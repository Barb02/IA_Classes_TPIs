from constraintsearch import *

region = ['A', 'B', 'C', 'D', 'E']
colors = ['red', 'blue', 'green', 'yellow', 'white']

mapa_a ={
    "A": "BED",
    "B": "AEC",
    "C": "BED",
    "D": "AEC",
    "E": "ABCD"
}

mapa_b ={
    "A": "BED",
    "B": "AEC",
    "C": "BEF",
    "D": "AEF",
    "E": "ABCDF",
    "F": "DEC"
}

mapa_c ={
    "A": "BFED",
    "B": "AFC",
    "C": "BFG",
    "D": "AEGC",
    "E": "AFGD",
    "F": "ABCEG",
    "G": "CDEF"
}

def make_constraint_graph(mapa):
    return {(X, Y): lambda r1, c1, r2, c2: c1 != c2 for X in mapa.keys() for Y in mapa[X]}

def make_domain(regions, colors):
    return {r:colors for r in regions}

cs = ConstraintSearch(make_domain(mapa_a.keys(), colors),make_constraint_graph(mapa_a))
print(cs.search())
""" cs = ConstraintSearch(make_domain(mapa_b.keys(), colors),make_constraint_graph(mapa_a))
print(cs.search())
cs = ConstraintSearch(make_domain(mapa_c.keys(), colors),make_constraint_graph(mapa_a))
print(cs.search()) """
