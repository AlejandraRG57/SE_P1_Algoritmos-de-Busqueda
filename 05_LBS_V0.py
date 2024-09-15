#Alejandra Rodriguez Guevara 21310127 7E1
"""Local Beam Search"""

import pygame, sys, random
from collections import deque
from tkinter import messagebox, Tk
# Importa las bibliotecas necesarias: pygame para gráficos, sys para interacción con el sistema, random para generar números aleatorios, collections para estructuras de datos como deque y tkinter para mostrar mensajes emergentes.

size = (width, height) = 640, 480
pygame.init()
# Define el tamaño de la ventana y se inicializa pygame.

win = pygame.display.set_mode(size)
pygame.display.set_caption('Local Beam Search')
clock = pygame.time.Clock()
# Crea la ventana con el título 'Local Beam Search' y se inicia el reloj de pygame.

cols, rows = 64, 48
# Define la cantidad de columnas y filas de la cuadrícula.

w = width // cols
h = height // rows
# Calcula el ancho y alto de cada celda en función del tamaño de la ventana y la cantidad de columnas y filas.

grid = []
beam = []
path = []
beam_width = 10  # Número de caminos en el haz
visited = []
# Inicializa las estructuras de datos: la cuadrícula (grid), el haz (beam), el camino (path), el ancho del haz (beam_width) y la lista de visitados.

class Spot:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.neighbors = []
        self.prev = None
        self.wall = False
        self.visited = False
        # Inicializa cada celda (spot) con coordenadas x, y. 
        # La celda tiene una lista de vecinos, una referencia al nodo anterior, y booleanos para indicar si es una pared o si ha sido visitada.
        
    def show(self, win, col):
        # Dibuja la celda en la ventana con el color especificado.
        if self.wall:
            col = (0, 0, 0)
            # Si es una pared, el color será negro.
        pygame.draw.rect(win, col, (self.x * w, self.y * h, w - 1, h - 1))
        # Dibuja un rectángulo en la posición de la celda.

    def add_neighbors(self, grid):
        # Añade los vecinos de la celda en las cuatro direcciones cardinales.
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])

def clickWall(pos, state):
    # Función para convertir una celda en pared o quitarla como pared.
    i = pos[0] // w
    j = pos[1] // h
    if 0 <= i < cols and 0 <= j < rows:
        grid[i][j].wall = state
        # Cambia el estado de la celda a pared si está dentro de los límites de la cuadrícula.

for i in range(cols):
    arr = []
    for j in range(rows):
        arr.append(Spot(i, j))
    grid.append(arr)
# Crea la cuadrícula inicializando cada celda como un objeto Spot.

for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbors(grid)
# Añade los vecinos a cada celda de la cuadrícula.

start = grid[cols // 2][rows // 2]
end = grid[cols - 1][rows - cols // 2]
# Define la celda de inicio (en el centro) y la celda de fin (en la esquina derecha).

start.wall = False
end.wall = False
# Asegura que las celdas de inicio y final no sean paredes.

beam.append([start])
start.visited = True
# Añade el nodo inicial al haz y lo marca como visitado.

def heuristic(spot):
    # Función heurística que calcula la distancia Manhattan desde una celda hasta la celda final.
    return abs(spot.x - end.x) + abs(spot.y - end.y)

def local_beam_search():
    global beam
    if not beam:
        return None
    # Si el haz está vacío, se devuelve None.

    # Expandir el haz actual
    new_beam = []
    for path in beam:
        current = path[-1]  # Último nodo en el camino
        if current == end:
            return path  # Si alcanzamos el objetivo, devolvemos el camino
        
        neighbors = []
        for neighbor in current.neighbors:
            if not neighbor.visited and not neighbor.wall:
                neighbors.append(neighbor)
                neighbor.visited = True
                neighbor.prev = current
        # Añade los vecinos no visitados y que no son paredes, y los marca como visitados.

        # Ordenamos a los vecinos por la heurística
        neighbors.sort(key=lambda x: heuristic(x))
        
        # Agregar vecinos al nuevo haz
        for neighbor in neighbors:
            new_path = list(path) + [neighbor]
            new_beam.append(new_path)
        # Crea un nuevo camino añadiendo cada vecino y lo añade al nuevo haz.

    # Mantener solo los `beam_width` mejores caminos
    new_beam.sort(key=lambda x: heuristic(x[-1]))
    beam = new_beam[:beam_width]
    # Mantiene solo los mejores caminos, según la heurística, limitados por el ancho del haz.

    return None

def main():
    searching = False
    found = False
    # Variables para controlar el estado de búsqueda y si se ha encontrado el objetivo.

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Si el usuario cierra la ventana, se sale del programa.

            if event.type == pygame.MOUSEBUTTONUP:
                if pygame.mouse.get_pressed()[0]:
                    clickWall(pygame.mouse.get_pos(), True)
                if pygame.mouse.get_pressed()[2]:
                    clickWall(pygame.mouse.get_pos(), False)
            # Controla los clics del mouse para activar o desactivar paredes.

            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    clickWall(pygame.mouse.get_pos(), True)
            # Permite arrastrar el mouse para activar las paredes.

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    searching = True
            # Comienza la búsqueda cuando se presiona Enter.

        if searching and not found:
            result = local_beam_search()
            if result:
                found = True
                path.extend(result)
            # Ejecuta la búsqueda y, si encuentra el objetivo, almacena el camino encontrado.

        win.fill((0, 20, 20))
        # Rellena la pantalla con un color de fondo.

        for i in range(cols):
            for j in range(rows):
                spot = grid[i][j]
                spot.show(win, (255, 255, 255))
                # Dibuja cada celda en blanco.

                if spot in path:
                    spot.show(win, (255, 255, 0))  # Camino encontrado (Amarillo)
                elif spot.visited:
                    spot.show(win, (255, 0, 0))  # Visitado (Rojo)
                if any(spot == b[-1] for b in beam):
                    spot.show(win, (0, 255, 0))  # Haz actual (Verde)
                if spot == end:
                    spot.show(win, (0, 120, 255))  # Nodo final (Azul)
                # Colorea las celdas según su estado: camino encontrado, visitada, parte del haz, o el nodo final.

        pygame.display.flip()
        clock.tick(30)
        # Actualiza la pantalla y controla la velocidad de actualización.

main()
# Llama a la función principal para ejecutar el programa.
