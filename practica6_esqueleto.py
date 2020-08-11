#! /usr/bin/python

# 6ta Practica Laboratorio
# Complementos Matematicos I
# Ejemplo parseo argumentos

import argparse
import matplotlib.pyplot as plt
import numpy as np
import utils
from random import randint

'''
	Argumentos pasados a LayOutGraph
	grafo: grafo en formato lista
	iters: cantidad de iteraciones a realizar
	refresh: cada cuántas iteraciones graficar
	c1: constante de repulsión
	c2: constante de atracción
	verbose: si está encendido, activa los comentarios
'''

class LayoutGraph:

	def __init__(self, grafo, iters, refresh, c1, c2, verbose=False):

		# Guardo el grafo
		self.grafo = grafo

		# Inicializo estado
		# Completar
		self.posiciones = {}
		self.fuerzas = {}

		# Guardo opciones
		self.iters = iters
		self.verbose = verbose
		# TODO: faltan opciones
		self.refresh = refresh
		self.c1 = c1
		self.c2 = c2

	def randomizarPosiciones(self):
		pos = {}
		for v in self.grafo[0]:
			pos[v] = ((randint(0, 300), randint(0, 300)))
		return pos


	def aristas(self, pos):
		listaAristas = []   # [([x1,y1],[x2,y2]),([x2,y2],[x3,y3]), ...]
		for (a,b) in self.grafo[1]:
			(x1,y1) = pos[a]
			(x2,y2) = pos[b]
			arista = ([x1,x2],[y1,y2])
			listaAristas.append(arista)
		return listaAristas


	def actualizarPosiciones(self, pos):
		x = []
		y = []

		for v in self.grafo[0]:
			(a,b) = pos[v]
			x.append(a)
			y.append(b)

		#plt.ion()

		plt.xlabel('x label')
		plt.ylabel('y label')
		plt.title("Simple Plot")
		plt.scatter(x,y)

		for (a,b) in self.aristas(pos):
			plt.plot(a,b)

		plt.show()

	def layout(self):
		'''
		Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar)
		un layout
		'''
		pos = self.randomizarPosiciones()
		self.actualizarPosiciones(pos)


def main():
	# Definimos los argumentos de linea de comando que aceptamos
	parser = argparse.ArgumentParser()

	# Verbosidad, opcional, False por defecto
	parser.add_argument(
		'-v', '--verbose',
		action='store_true',
		help='Muestra mas informacion al correr el programa'
	)
	# Cantidad de iteraciones, opcional, 50 por defecto
	parser.add_argument(
		'--iters',
		type=int,
		help='Cantidad de iteraciones a efectuar',
		default=50
	)
	# Temperatura inicial
	parser.add_argument(
		'--temp',
		type=float,
		help='Temperatura inicial',
		default=100.0
	)
	# Archivo del cual leer el grafo
	parser.add_argument(
		'file_name',
		help='Archivo del cual leer el grafo a dibujar'
	)

	args = parser.parse_args()
	G = utils.leerGrafo(archivo = args.file_name)

	# Descomentar abajo para ver funcionamiento de argparse
	# print args.verbose
	# print args.iters
	# print args.file_name
	# print args.temp
	# return

	# Creamos nuestro objeto LayoutGraph
	layout_gr = LayoutGraph(
		G,  # TODO: Cambiar para usar grafo leido de archivo
		iters=args.iters,
		refresh=1,
		c1=0.1,
		c2=5.0,
		verbose=args.verbose
		)

	# Ejecutamos el layout
	layout_gr.layout()
	return


if __name__ == '__main__':
	main()
