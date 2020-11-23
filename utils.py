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

versor = lambda vec: (vec[0]/norm(vec), vec[1]/norm(vec))
norm = lambda vec: math.sqrt((vec[0]**2)+(vec[1]**2))
diff = lambda u, v: (u[0]-v[0], u[1]-v[1])
distancia = lambda u, v: math.sqrt(sum(a*a for a in diff(u,v)))
