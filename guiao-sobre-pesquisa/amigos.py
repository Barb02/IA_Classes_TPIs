from constraintsearch import *

amigos = ["Andre", "Bernardo", "Claudio"]

def constraint(a1, i1, a2, i2):
    b1,c1 = i1
    b2,c2 = i2

    if a1 in i1 or a2 in i2:
        return False 

    if c1 == b1 or c2 == b2 or c1 == c2 or b1 == b2:
        return False

    if c1 == "Claudio" and b1 != "Bernardo":
        return False
    if c2 == "Claudio" and b2 != "Bernardo":
        return False

    return True

def make_constraint_graph(amigos):
    return { (X,Y): constraint for X in amigos for Y in amigos if X != Y}

def make_domain(amigos):
    return { amigo:[(bicicleta, chapeu) for chapeu in amigos for bicicleta in amigos] for amigo in amigos }
    
cs = ConstraintSearch(make_domain(amigos), make_constraint_graph(amigos))

print(cs.search())
