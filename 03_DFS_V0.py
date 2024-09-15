#Alejandra Rodriguez Guevara 21310127 7E1
"""Backtracking Recursive Maze Generation"""
"""Recursive Depth First Search"""

import pygame, sys, random

# Inicializa Pygame
pygame.init()

# Configura la ventana de visualización
win = pygame.display.set_mode((600, 360))
clock = pygame.time.Clock()

# Define el tamaño de cada celda
w = 10

# Calcula el número de columnas y filas basadas en el tamaño de la ventana y las celdas
cols = int(win.get_width() / w)
rows = int(win.get_height() / w)

# Inicializa la cuadrícula y la pila para el algoritmo de retroceso
grid = []
stack = []

# Función para obtener el índice de una celda basada en sus coordenadas
def index(i, j):
    if i < 0 or j < 0 or i >= cols or j >= rows:
        return None
    else:
        return i + j * cols

# Clase para representar una celda en la cuadrícula
class Cell:
    def __init__(self, i, j):
        self.i, self.j = i, j
        # Las paredes están inicialmente presentes en las 4 direcciones: arriba, derecha, abajo, izquierda
        self.walls = [True, True, True, True]
        self.visited = False

    # Muestra la celda en la ventana
    def show(self, win):
        x = self.i * w
        y = self.j * w
        # Si la celda ha sido visitada, dibuja un rectángulo en color rosa
        if self.visited:
            pygame.draw.rect(win, (255, 192, 203), (x, y, w, w))
        # Dibuja las paredes de la celda si están presentes
        if self.walls[0]:
            pygame.draw.line(win, (0, 0, 0), (x, y), (x + w, y))  # pared superior
        if self.walls[1]:
            pygame.draw.line(win, (0, 0, 0), (x + w, y), (x + w, y + w))  # pared derecha
        if self.walls[2]:
            pygame.draw.line(win, (0, 0, 0), (x + w, y + w), (x, y + w))  # pared inferior
        if self.walls[3]:
            pygame.draw.line(win, (0, 0, 0), (x, y + w), (x, y))  # pared izquierda

    # Resalta la celda con un borde azul
    def highlight(self, win):
        x = self.i * w
        y = self.j * w
        pygame.draw.rect(win, (0, 0, 255), (x, y, w, w), 2)  # Borde azul

    # Comprueba los vecinos de la celda actual
    def checkNeighbors(self):
        neighbors = []
        i, j = self.i, self.j
        # Verifica las celdas vecinas (superior, derecha, izquierda, inferior)
        if index(i, j - 1) is not None:
            top = grid[index(i, j - 1)]
            if not top.visited:
                neighbors.append(top)
        if index(i + 1, j) is not None:
            right = grid[index(i + 1, j)]
            if not right.visited:
                neighbors.append(right)
        if index(i - 1, j) is not None:
            left = grid[index(i - 1, j)]
            if not left.visited:
                neighbors.append(left)
        if index(i, j + 1) is not None:
            bottom = grid[index(i, j + 1)]
            if not bottom.visited:
                neighbors.append(bottom)
        
        # Devuelve un vecino aleatorio si hay vecinos disponibles
        if len(neighbors) > 0:
            return random.choice(neighbors)
        else:
            return None

# Elimina las paredes entre dos celdas adyacentes
def removeWalls(a, b):
    x = a.i - b.i
    if x == 1:
        a.walls[3] = False
        b.walls[1] = False
    elif x == -1:
        a.walls[1] = False
        b.walls[3] = False
    y = a.j - b.j
    if y == 1:
        a.walls[0] = False
        b.walls[2] = False
    elif y == -1:
        a.walls[2] = False
        b.walls[0] = False

# Inicializa la cuadrícula con celdas
for j in range(rows):
    for i in range(cols):
        cell = Cell(i, j)
        grid.append(cell)

# Elige una celda inicial para comenzar el algoritmo
n = 0
current = grid[n]

# Bucle principal del algoritmo de generación del laberinto
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Limpia la ventana y dibuja todas las celdas
    win.fill((0, 0, 0))
    
    for cell in grid:
        cell.show(win)
    
    # Marca la celda actual como visitada y la resalta
    current.visited = True
    current.highlight(win)
    
    # Paso 1: Buscar un vecino no visitado
    nextcell = current.checkNeighbors()
    
    if isinstance(nextcell, Cell):
        # Paso 2: Marca el vecino como visitado y lo agrega a la pila
        nextcell.visited = True
        stack.append(current)
        # Paso 3: Elimina las paredes entre la celda actual y el vecino
        removeWalls(current, nextcell)
        # Paso 4: Avanza a la siguiente celda
        current = nextcell
    elif len(stack) > 0:
        # Regresa a la celda anterior si no hay vecinos disponibles
        current = stack.pop()
    
    # Actualiza la pantalla
    pygame.display.flip()
    # Controla la velocidad de la generación del laberinto
    clock.tick(100)
