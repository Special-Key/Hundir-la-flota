import numpy as np


# Tamaño del tablero (10x10)
TAM_TABLERO = 10

# Letras que representan las filas: A-J
LETRAS_FILAS = [chr(i) for i in range(65, 65 + TAM_TABLERO)]

# Símbolos usados en los tableros
AGUA = "."                 # Casilla vacía (sin disparo)
BARCO = "O"                # Parte visible de un barco
AGUA_IMPACTADA = "#"       # Disparo que cayó en el agua
TOCADO = "X"               # Parte del barco tocada (aún no hundido)
HUNDIDO = "\033[91mX\033[0m"  # Parte del barco hundido (en rojo ANSI)

# Definición de barcos:
# Cada barco tiene: [Nombre, tamaño (eslora), cantidad disponible]

L = ["Lancha", 2, 3]        # 3 lanchas de tamaño 2
S = ["Submarino", 3, 2]     # 2 submarinos de tamaño 3
D = ["Destructor", 4, 1]    # 1 destructor de tamaño 4

# Diccionario con los barcos disponibles
BARCOS = {
    "l": L,
    "s": S,
    "d": D
}

