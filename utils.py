import math

# MARK: Parseo de texto
def leerGrafo(archivo):
    f = open(archivo, mode='r')
    cantV = int(f.readline())

    V = []
    for i in range(0, cantV):
        vert = f.readline().replace('\n','')
        V.append(vert)

    E = []
    for line in f:
        [a,b] = line.split(' ')
        b = b.replace('\n','')
        E.append((a,b))

    G = (V, E)

    return G

diff = lambda v, u: (v[0]-u[0], v[1]-u[1])
norm = lambda v, u: math.sqrt(sum(a*a for a in diff(v,u)))

fuerzaAtraccion = norm
fuerzaRepulsion = norm
