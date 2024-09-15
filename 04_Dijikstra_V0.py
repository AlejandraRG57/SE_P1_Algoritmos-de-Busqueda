#Alejandra Rodriguez Guevara 21310127 7E1
"""Djikstra's Path Finding"""

import pygame, sys, random, math
from collections import deque
from tkinter import messagebox, Tk

# Configuración de la ventana y la cuadrícula
size = (width, height) = 640, 480
pygame.init()

win = pygame.display.set_mode(size)
pygame.display.set_caption("Dijkstra's Path Finding")
clock = pygame.time.Clock()

cols, rows = 64, 48
w = width // cols
h = height // rows

grid = []
queue, visited = deque(), []
path = []

class Spot:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.prev = None
        self.wall = False
        self.visited = False
        if (i + j) % 7 == 0:
            self.wall = True
        # Si la suma de las coordenadas de la celda es múltiplo de 7, marca la celda como pared.
        
    def show(self, win, col, shape=1):
        if self.wall:
            col = (0, 0, 0)  # Color negro para las paredes.
        if shape == 1:
            pygame.draw.rect(win, col, (self.x * w, self.y * h, w - 1, h - 1))
        else:
            pygame.draw.circle(win, col, (self.x * w + w // 2, self.y * h + h // 2), w // 3)
        # Dibuja la celda en la ventana en el color especificado. Puede ser un rectángulo o un círculo.
    
    def add_neighbors(self, grid):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        # Añade los vecinos en las cuatro direcciones cardinales.
        # Añadir diagonales está comentado, pero se puede descomentar si se desea soporte para movimiento diagonal.

def clickWall(pos, state):
    i = pos[0] // w
    j = pos[1] // h

    # Verificar que i y j estén dentro de los límites de la grilla
    if 0 <= i < cols and 0 <= j < rows:
        grid[i][j].wall = state
        # Cambia el estado de la celda a pared o no pared según el estado proporcionado.

def place(pos):
    i = pos[0] // w
    j = pos[1] // h
    return w, h
    # Esta función no se utiliza en el código proporcionado, pero podría servir para otras tareas relacionadas con el tamaño de la celda.

for i in range(cols):
    arr = []
    for j in range(rows):
        arr.append(Spot(i, j))
    grid.append(arr)
# Inicializa la cuadrícula creando objetos `Spot` para cada celda.

for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbors(grid)
# Añade los vecinos a cada celda en la cuadrícula.

start = grid[0][0]
end = grid[cols - cols // 2][rows - cols // 4]
start.wall = False
end.wall = False
# Define la celda de inicio (esquina superior izquierda) y la celda de fin (posición calculada).

queue.append(start)
start.visited = True
# Añade el nodo inicial a la cola y marca como visitado.

def main():
    flag = False
    noflag = True
    startflag = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (1, 3):  
                    clickWall(pygame.mouse.get_pos(), event.button == 1)
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0] or event.buttons[2]:
                    clickWall(pygame.mouse.get_pos(), event.buttons[0])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    startflag = True
        # Maneja eventos: cierre de ventana, clics del mouse para agregar o quitar paredes y comenzar la búsqueda al presionar Enter.

        if startflag:
            if len(queue) > 0:
                current = queue.popleft()
                if current == end:
                    temp = current
                    while temp.prev:
                        path.append(temp.prev)
                        temp = temp.prev 
                    if not flag:
                        flag = True
                        print("Done")
                    elif flag:
                        continue
                if not flag:
                    for i in current.neighbors:
                        if not i.visited and not i.wall:
                            i.visited = True
                            i.prev = current
                            queue.append(i)
            else:
                if noflag and not flag:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There was no solution" )
                    noflag = False
                else:
                    continue
        # Si se ha iniciado la búsqueda, expande los nodos en la cola y reconstruye el camino si se encuentra el nodo final.
        # Muestra un mensaje si no hay solución.

        win.fill((0, 20, 20))
        for i in range(cols):
            for j in range(rows):
                spot = grid[i][j]
                spot.show(win, (255, 192, 203))
                if spot in path:
                    spot.show(win, (46, 204, 113))
                    spot.show(win, (192, 57, 43), 0)
                elif spot.visited:
                    spot.show(win, (39, 174, 96))
                if spot in queue and not flag:
                    spot.show(win, (44, 62, 80))
                    spot.show(win, (39, 174, 96), 0)
                if spot == start:
                    spot.show(win, (0, 255, 200))
                if spot == end:
                    spot.show(win, (0, 120, 255))
                # Dibuja cada celda en la ventana con colores diferentes según su estado: camino encontrado (verde), visitado (verde claro), en la cola (gris), inicio (cian) y fin (azul).

        pygame.display.flip()
        # Actualiza la pantalla.

main()
# Llama a la función principal para ejecutar el programa.
