bn = [("C", [("A", True), ("B", True)], 0.95), ("C", [("A", True), ("B", False)], 0.95), 
      ("C", [("A", False), ("B", True)], 0.95), ("C", [("A", False), ("B", False)], 0.95),
      ("D", [("C", True)], 0.9), ("D", [("C", False)], 0.9), ("B", [], 0.33)]

def get_ancestors(bn, var):
    ancestors = set()
    for pc in bn:
        if pc[0] == var:
            for v in pc[1]:
                ancestors.add(v[0])
    ancestors_l = list(ancestors)
    if ancestors_l == []:
        return []
    res = []
    for a in ancestors_l:
        res.extend(get_ancestors(bn, a))
    return res + ancestors_l

print(get_ancestors(bn, "D"))