#! /usr/bin/python

# 6ta Practica Laboratorio
# Complementos Matematicos I
# Ejemplo parseo argumentos

import argparse
import matplotlib.pyplot as plt
import numpy as np
import utils
from math import sqrt
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
		self.posiciones = {}
		self.fuerzas = {}

		# Guardo opciones
		self.iters = iters
		self.verbose = verbose
		# TODO: faltan opciones
		self.refresh = refresh
		self.c1 = c1			# Coeficiente fuerza atracción
		self.c2 = c2			# Coeficiente fuerza repulsión
		self.lado = 300
		self.k = sqrt(self.lado * self.lado / len(self.grafo[0]))
		self.t = 100
		self.eps = 0.5

	def fuerzaAtr(self, dist):
		return dist**2/(self.k * self.c1)

	def fuerzaRep(self, dist):
		return (self.k * self.c2)**2/dist

	def randomizarPosiciones(self):
		for v in self.grafo[0]:
			self.posiciones[v] = ((randint(0, self.lado-1),
								   randint(0, self.lado-1)))

	def resetAccum(self):
		accum = {}
		for v in self.grafo[0]:
			accum[v] = (0,0)
		return accum

	def calcularFuerzasAtr(self, accum):
		for (a,b) in self.grafo[1]:
			posA = self.posiciones[a]
			posB = self.posiciones[b]
			delta = utils.diff(posA, posB)
			distance = utils.norm(delta)
			if distance > self.eps:
				modFA = self.fuerzaAtr(distance)
				(dx, dy) = utils.diff(posB, posA)
				(fX, fY) = (modFA*dx/distance, modFA*dy/distance)
				(ax, ay) = accum[a]
				accum[a] = (ax+fX, ay+fY)
				(bx, by) = accum[b]
				accum[b] = (bx-fX, by-fY)
		return accum

	def calcularFuerzasRep(self, accum):
		for v in self.grafo[0]:
			for u in self.grafo[0]:
				if v != u:
					posV = self.posiciones[v]
					posU = self.posiciones[u]
					delta = utils.diff(posV, posU)
					distance = utils.norm(delta)
					(ax, ay) = accum[v]
					if distance > self.eps:
						modFR = self.fuerzaRep(distance)
						(dx, dy) = utils.diff(posU, posV)
						(fx, fy) = (modFR*dx/distance, modFR*dy/distance)
					else:
						(fx, fy) = (randint(-100, 100), randint(-100, 100))
					accum[v] = (ax+fx, ay+fy)

		return accum

	def calcularFuerzasGrav(self, accum):
		xyCenter = self.lado/2
		center = (xyCenter, xyCenter)
		for v in self.grafo[0]:
			posV = self.posiciones[v]
			dist = max(utils.distancia(center, posV), self.eps)
			(dx, dy) = utils.diff(posV, center)
			(fX, fY) = (0.1*dx/dist, 0.1*dy/dist)
			(vx, vy) = accum[v]
			accum[v] = (vx+fX,vy+fY)
		return accum

	def actualizarPosiciones(self, accum):
		for v in self.grafo[0]:
			(fX, fY) = accum[v]
			#print("distance", utils.norm(accum[v]))
			if utils.norm(accum[v]) > self.t:
				(fX, fY) = utils.versor(accum[v])
				fX *= self.t
				fY *= self.t
			(x,y) = self.posiciones[v]
			self.posiciones[v] = (int(max(min(fX+x, self.lado), 0)),
								  int(max(min(fY+y, self.lado), 0)))

	def actualizarTemperatura(self):
		self.t *= 0.95


	def step(self):
		accum = self.calcularFuerzasGrav(
					self.calcularFuerzasRep(
						self.calcularFuerzasAtr(self.resetAccum())))
		self.actualizarPosiciones(accum)
		#print(self.posiciones)
		self.actualizarTemperatura()
		self.dibujar()


	def layout(self):
		'''
		Aplica el algoritmo de Fruchtermann-Reingold para obtener (y mostrar)
		un layout
		'''
		self.randomizarPosiciones()
		#print(self.posiciones)
		for i in range(self.iters):
			self.step()


	# Funciones de dibujado
	def aristas(self):
		listaAristas = []   # [([x1,y1],[x2,y2]),([x2,y2],[x3,y3]), ...]
		for (a,b) in self.grafo[1]:
			(x1,y1) = self.posiciones[a]
			(x2,y2) = self.posiciones[b]
			arista = ([x1,x2],[y1,y2])
			listaAristas.append(arista)
		return listaAristas


	def dibujar(self):
		plt.clf()
		plt.xlim(0, self.lado)
		plt.ylim(0, self.lado)

		x = []
		y = []

		for v in self.grafo[0]:
			(a,b) = self.posiciones[v]
			x.append(a)
			y.append(b)

		plt.xlabel('x label')
		plt.ylabel('y label')
		plt.title("Simple Plot")
		plt.scatter(x,y)

		for (a,b) in self.aristas():
			plt.plot(a,b)

		plt.pause(0.05)

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
		G,
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
