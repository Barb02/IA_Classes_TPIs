import math
import functools

#Exercicio 4.1
impar = lambda x : x % 2 == 1

#Exercicio 4.2
positivo = lambda x : x > 0

#Exercicio 4.3
comparar_modulo = lambda x, y : abs(x) < abs(y)

#Exercicio 4.4
cart2pol = lambda x, y : (math.hypot(x,y), math.atan2(y, x))

#Exercicio 4.5
ex5 = lambda f, g, h : lambda x, y, z : h(f(x,y), g(y,z))

#Exercicio 4.6
def quantificador_universal(lista, f):
    if len(list(filter(lambda x: f(x), lista))) == len(lista):
        return True
    return False

#Exercicio 4.8
def subconjunto(lista1, lista2):
    listaIntersec = [x for x in lista1 if x in lista2]
    if listaIntersec == lista1:
        return True
    return False

#Exercicio 4.9
def menor_ordem(lista, f):
    return functools.reduce((lambda x,y : x if f(x,y) else y), lista)

#Exercicio 4.10
def menor_e_resto_ordem(lista, f):
    if len(lista) == 1:
        return lista[0], []
    
    m, r = menor_e_resto_ordem(lista[1:], f)

    if f(lista[0], m):
        return lista[0], [m] + r
    return m, [lista[0]] + r

#Exercicio 5.2
def ordenar_seleccao(lista, ordem):
    if lista == []:
        return lista
    
    menor, resto = menor_e_resto_ordem(lista, ordem)

    return [menor] + ordenar_seleccao(resto, ordem)