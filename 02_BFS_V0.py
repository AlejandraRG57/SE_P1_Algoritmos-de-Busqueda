#Alejandra Rodriguez Guevara 21310127 7E1
"""Breadth First Search"""
# Comentario que indica que el código implementa el algoritmo de búsqueda en anchura (BFS).

import pygame, sys, random, math
# Importa las bibliotecas pygame (para gráficos y eventos), sys (para manipulación del sistema), random (para generar valores aleatorios), y math (para funciones matemáticas).

from collections import deque
# Importa deque, una estructura de datos de cola doble (doble extremo) de la biblioteca collections.

from tkinter import messagebox, Tk
# Importa la funcionalidad para mostrar cuadros de mensaje usando Tkinter.

size = (width, height) = 640, 480
# Define el tamaño de la ventana como 640 píxeles de ancho y 480 de alto.

pygame.init()
# Inicializa todos los módulos de pygame.

win = pygame.display.set_mode(size)
# Crea una ventana de tamaño definido por 'size'.

pygame.display.set_caption('Breadth First Search')
# Establece el título de la ventana como 'Breadth First Search'.

clock = pygame.time.Clock()
# Crea un reloj para controlar la velocidad de fotogramas.

cols, rows = 64, 48
# Define el número de columnas y filas de la cuadrícula.

w = width // cols
# Calcula el ancho de cada celda en la cuadrícula.

h = height // rows
# Calcula la altura de cada celda en la cuadrícula.

grid = []
# Inicializa la cuadrícula como una lista vacía.

queue, visited = deque(), []
# Inicializa la cola (para BFS) como un deque y la lista de visitados como una lista vacía.

path = []
# Inicializa la lista del camino como una lista vacía.

class Spot:
    # Clase que representa cada celda (spot) de la cuadrícula.

    def __init__(self, i, j):
        # Constructor de la clase Spot.
        self.x, self.y = i, j
        # Define las coordenadas de la celda en la cuadrícula.
        self.f, self.g, self.h = 0, 0, 0
        # Inicializa los valores f, g, y h (usados comúnmente en A*; no utilizados aquí).
        self.neighbors = []
        # Lista para almacenar los vecinos de la celda.
        self.prev = None
        # Variable para almacenar la celda anterior en el camino.
        self.wall = False
        # Indica si la celda es una pared.
        self.visited = False
        # Indica si la celda ha sido visitada.

        # if random.randint(0, 100) < 20:
        #     self.wall = True
        # Comentado: Asigna aleatoriamente si una celda será una pared (20% de probabilidad).

    def show(self, win, col):
        # Método para dibujar la celda en la ventana.
        if self.wall == True:
            # Si la celda es una pared, el color será negro.
            col = (0, 0, 0)
        pygame.draw.rect(win, col, (self.x * w, self.y * h, w - 1, h - 1))
        # Dibuja un rectángulo en la posición de la celda con el color especificado.

    def add_neighbors(self, grid):
        # Método para añadir los vecinos válidos de la celda.
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        # Añade el vecino a la derecha.
        
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        # Añade el vecino a la izquierda.

        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])
        # Añade el vecino abajo.

        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        # Añade el vecino arriba.

        #Add Diagonals
        # if self.x < cols - 1 and self.y < rows - 1:
        #     self.neighbors.append(grid[self.x+1][self.y+1])
        # Comentado: Añadir vecino diagonal abajo-derecha.
        
        # if self.x < cols - 1 and self.y > 0:
        #     self.neighbors.append(grid[self.x+1][self.y-1])
        # Comentado: Añadir vecino diagonal arriba-derecha.
        
        # if self.x > 0 and self.y < rows - 1:
        #     self.neighbors.append(grid[self.x-1][self.y+1])
        # Comentado: Añadir vecino diagonal abajo-izquierda.
        
        # if self.x > 0 and self.y > 0:
        #     self.neighbors.append(grid[self.x-1][self.y-1])
        # Comentado: Añadir vecino diagonal arriba-izquierda.

def clickWall(pos, state):
    # Función para activar/desactivar una celda como pared.
    i = pos[0] // w
    j = pos[1] // h
    # Convierte las coordenadas del clic en índices de la cuadrícula.

    # Verificar que i y j estén dentro de los límites de la grilla.
    if i >= 0 and i < cols and j >= 0 and j < rows:
        grid[i][j].wall = state
    # Si las coordenadas son válidas, se establece el estado de la celda (como pared o no).

def place(pos):
    # Función para obtener las dimensiones de una celda.
    i = pos[0] // w
    j = pos[1] // h
    return w, h
    # Devuelve el ancho y alto de una celda.

# Crear la cuadrícula.
for i in range(cols):
    arr = []
    for j in range(rows):
        arr.append(Spot(i, j))
    grid.append(arr)
    # Llena la cuadrícula con objetos Spot (celdas).

for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbors(grid)
    # Añade los vecinos a cada celda de la cuadrícula.

start = grid[cols // 2][rows // 2]
# Define la celda de inicio en el centro de la cuadrícula.

end = grid[cols - 1][rows - cols // 2]
# Define la celda final (objetivo) en la esquina derecha de la cuadrícula.

start.wall = False
end.wall = False
# Asegura que las celdas de inicio y final no sean paredes.

queue.append(start)
# Añade la celda inicial a la cola.

start.visited = True
# Marca la celda inicial como visitada.

def main():
    # Función principal del programa.
    flag = False
    noflag = True
    startflag = False
    # Variables para el control de estados.

    while True:
        # Bucle principal del programa.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Si se cierra la ventana, se sale del programa.

            if event.type == pygame.MOUSEBUTTONUP:
                if pygame.mouse.get_pressed()[0]:
                    clickWall(pygame.mouse.get_pos(), True)
                if pygame.mouse.get_pressed()[2]:
                    clickWall(pygame.mouse.get_pos(), False)
            # Detecta clics del mouse para activar o desactivar paredes.

            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    clickWall(pygame.mouse.get_pos(), True)
            # Detecta el movimiento del mouse para arrastrar y crear paredes.

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    startflag = True
            # Comienza la búsqueda cuando se presiona Enter.

        if startflag:
            # Si se ha iniciado la búsqueda:
            if len(queue) > 0:
                current = queue.popleft()
                # Extrae el primer elemento de la cola (BFS).

                if current == end:
                    temp = current
                    while temp.prev:
                        path.append(temp.prev)
                        temp = temp.prev
                    # Si se encuentra la meta, se reconstruye el camino.

                    if not flag:
                        flag = True
                        print("Done")
                    elif flag:
                        continue
                # Marca el final de la búsqueda si se llega al objetivo.

                if flag == False:
                    for i in current.neighbors:
                        if not i.visited and not i.wall:
                            i.visited = True
                            i.prev = current
                            queue.append(i)
                    # Si la celda no ha sido visitada y no es una pared, se marca y se añade a la cola.
            else:
                if noflag and not flag:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There was no solution")
                    noflag = False
                else:
                    continue
                # Muestra un mensaje si no se encuentra solución.

        win.fill((0, 20, 20))
        # Rellena la ventana con un color de fondo oscuro.

        for i in range(cols):
            for j in range(rows):
                spot = grid[i][j]
                spot.show(win, (255, 192, 203))
                # Muestra cada celda de la cuadrícula.

                if spot in path:
                    spot.show(win, (25, 120, 250))
                elif spot.visited:
                    spot.show(win, (255, 0, 0))
                if spot in queue:
                    spot.show(win, (0, 255, 0))
                if spot == end:
                    spot.show(win, (0, 120, 255))
                # Muestra las celdas según su estado (camino, visitada, en cola, meta).

        pygame.display.flip()
        # Actualiza la ventana.

main()
# Llama a la función principal para ejecutar el programa.
