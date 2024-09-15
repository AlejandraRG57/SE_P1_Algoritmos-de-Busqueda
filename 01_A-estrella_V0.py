"""A*"""

import pygame, sys, random, math
from tkinter import messagebox, Tk
# Importa las bibliotecas necesarias: pygame para gráficos, sys para interacción con el sistema, random para números aleatorios, math para funciones matemáticas y tkinter para mostrar mensajes emergentes.

size = (width, height) = 600, 600
# Define el tamaño de la ventana.

pygame.init()
# Inicializa pygame.

win = pygame.display.set_mode(size)
# Crea la ventana de tamaño definido.

clock = pygame.time.Clock()
# Inicializa el reloj para controlar la tasa de actualización.

cols, rows = 50, 50
# Define la cantidad de columnas y filas de la cuadrícula.

grid = []
openSet, closeSet = [], []
path = []
# Inicializa las estructuras de datos: cuadrícula (grid), conjuntos abiertos (openSet) y cerrados (closeSet), y el camino (path).

w = width // cols
h = height // rows
# Calcula el ancho y alto de cada celda en función del tamaño de la ventana y la cantidad de columnas y filas.

class Spot:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.prev = None
        self.wall = False
        # Inicializa cada celda con coordenadas (x, y) y establece los valores f, g, h (para A*), lista de vecinos, referencia al nodo anterior y estado de pared.

    def show(self, win, col):
        if self.wall == True:
            col = (0, 0, 0)
            # Si es una pared, el color será negro.
        pygame.draw.rect(win, col, (self.x * w, self.y * h, w - 1, h - 1))
        # Dibuja un rectángulo en la ventana en la posición de la celda con el color especificado.

    def add_neighbors(self, grid):
        # Añade los vecinos de la celda en las cuatro direcciones cardinales y diagonales.
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        # Añade vecinos diagonales
        if self.x < cols - 1 and self.y < rows - 1:
            self.neighbors.append(grid[self.x + 1][self.y + 1])
        if self.x < cols - 1 and self.y > 0:
            self.neighbors.append(grid[self.x + 1][self.y - 1])
        if self.x > 0 and self.y < rows - 1:
            self.neighbors.append(grid[self.x - 1][self.y + 1])
        if self.x > 0 and self.y > 0:
            self.neighbors.append(grid[self.x - 1][self.y - 1])

def clickWall(pos, state):
    i = pos[0] // w
    j = pos[1] // h
    # Calcula las coordenadas de la celda a partir de la posición del mouse.

    if i >= 0 and i < cols and j >= 0 and j < rows:
        grid[i][j].wall = state
        # Cambia el estado de la celda a pared o no pared si está dentro de los límites de la cuadrícula.

def place(pos):
    i = pos[0] // w
    j = pos[1] // h
    return w, h
    # Calcula el ancho y alto de la celda, pero no se utiliza en el código proporcionado.

def heuristics(a, b):
    return math.sqrt((a.x - b.x)**2 + abs(a.y - b.y)**2)
    # Calcula la heurística (distancia Euclidiana) entre dos celdas `a` y `b`.

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

start = grid[0][0]
end = grid[cols - cols//2][rows - cols//4]
# Define la celda de inicio (esquina superior izquierda) y la celda de fin (posición calculada).

openSet.append(start)
# Añade el nodo inicial al conjunto abierto.

def close():
    pygame.quit()
    sys.exit()
# Función para cerrar pygame y salir del programa.

def main():
    flag = False
    noflag = True
    startflag = False
    # Variables para controlar el estado de búsqueda y si se ha encontrado el objetivo.

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.MOUSEBUTTONUP:
                if pygame.mouse.get_pressed()[0]:
                    clickWall(pygame.mouse.get_pos(), True)
                if pygame.mouse.get_pressed()[2]:
                    clickWall(pygame.mouse.get_pos(), False)
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    clickWall(pygame.mouse.get_pos(), True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    startflag = True
        # Maneja los eventos: cerrar la ventana, hacer clic para agregar o quitar paredes y comenzar la búsqueda al presionar Enter.

        if startflag:
            if len(openSet) > 0:
                winner = 0
                for i in range(len(openSet)):
                    if openSet[i].f < openSet[winner].f:
                        winner = i
                # Encuentra el nodo en el conjunto abierto con el menor costo total (f).

                current = openSet[winner]
                
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
                # Si se ha alcanzado el nodo final, reconstruye el camino desde el nodo final hasta el nodo inicial y marca que se ha encontrado el objetivo.

                if flag == False:
                    openSet.remove(current)
                    closeSet.append(current)

                    for neighbor in current.neighbors:
                        if neighbor in closeSet or neighbor.wall:
                            continue
                        tempG = current.g + 1

                        newPath = False
                        if neighbor in openSet:
                            if tempG < neighbor.g:
                                neighbor.g = tempG
                                newPath = True
                        else:
                            neighbor.g = tempG
                            newPath = True
                            openSet.append(neighbor)
                        
                        if newPath:
                            neighbor.h = heuristics(neighbor, end)
                            neighbor.f = neighbor.g + neighbor.h
                            neighbor.prev = current
                            # Actualiza los costos g, h y f de los vecinos y añade el vecino al conjunto abierto si es necesario.

            else:
                if noflag:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There was no solution" )
                    noflag = False
                # Muestra un mensaje de error si no hay solución y la búsqueda ha terminado.

        win.fill((0, 20, 20))
        # Rellena la pantalla con un color de fondo.

        for i in range(cols):
            for j in range(rows):
                spot = grid[j][i]
                spot.show(win, (255, 192, 203))
                # Dibuja cada celda en la cuadrícula.

                if flag and spot in path:
                    spot.show(win, (25, 120, 250))
                elif spot in closeSet:
                    spot.show(win, (255, 0, 0))
                elif spot in openSet:
                    spot.show(win, (0, 255, 0))
                try:
                    if spot == end:
                        spot.show(win, (0, 120, 255))
                except Exception:
                    pass
                # Colorea las celdas según su estado: camino encontrado (azul), visitado (rojo), en el conjunto abierto (verde), o el nodo final (azul).

        pygame.display.flip()
        # Actualiza la pantalla.

main()
# Llama a la función principal para ejecutar el programa.
