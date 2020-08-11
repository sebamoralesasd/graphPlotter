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
