class Nod:
    def __init__(self, e):
        self.e = e
        self.urm = None

class Lista:
    def __init__(self, prim=None):
        self.prim = prim

'''
crearea unei liste din valori citite pana la 0
'''
def creareLista():
    lista = Lista()
    lista.prim = creareLista_rec()
    return lista

def creareLista_rec():
    x = int(input("x="))
    if x == 0:
        return None
    else:
        nod = Nod(x)
        nod.urm = creareLista_rec()
        return nod

'''
tiparirea elementelor unei liste
'''
def tipar(lista):
    tipar_rec(lista.prim)

def tipar_rec(nod):
    if nod is not None:
        print(nod.e)
        tipar_rec(nod.urm)

'''
a. Transform a list into a set (remove duplicates)
b. Determine the union of two sets. The sets are represented as lists.
'''

def found(x, lista):
    current = lista.prim
    while current is not None:
        if current.e == x:
            return True
        current = current.urm
    return False

# f1: Transform a list into a set (remove duplicates)
def f1(lista):
    if lista.prim is None:
        return Lista() 

    unique_list = Lista()
    unique_list.prim = f1_rec(lista.prim)
    return unique_list

def f1_rec(nod):
    if nod is None:
        return None

    urm = f1_rec(nod.urm)
    
    if not found(nod.e, Lista(urm)):
        new_nod = Nod(nod.e)
        new_nod.urm = urm
        return new_nod
    
    return urm

# f2: Union of two sets (lists)
def f2(nod1, nod2):
    if nod1 is None:
        return nod2  # If the first list is empty, return the second list

    if not found(nod1.e, Lista(nod2)):
        new_nod = Nod(nod1.e)
        new_nod.urm = f2(nod1.urm, nod2)
        return new_nod

    return f2(nod1.urm, nod2)

# Main test function
def main():
    print("Introduceti elementele listei 1:")
    list1 = creareLista()
    print("Rezultatul f1 (lista 1 fără duplicate) este:")
    unique_list1 = f1(list1)
    tipar(unique_list1)

    print("--------------")
    
    print("Introduceti elementele listei 2:")
    list2 = creareLista()
    print("Rezultatul f1 (lista 2 fără duplicate) este:")
    unique_list2 = f1(list2)
    tipar(unique_list2)

    print("--------------")
    
    print("Uniunea celor două liste este:")
    union_list = Lista(f2(unique_list1.prim, unique_list2.prim))
    tipar(union_list)

main()

"""
    p1.pdf 9

"""