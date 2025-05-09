# utils.py

import numpy as np
import random
import time
from variables import (
    TAM_TABLERO, LETRAS_FILAS, AGUA, BARCO, AGUA_IMPACTADA,
    TOCADO, HUNDIDO, BARCOS
)

# ------------------------- FUNCIONES DE TABLERO -------------------------

def crear_tablero():
    return np.full((TAM_TABLERO, TAM_TABLERO), AGUA)

def mostrar_tablero(tablero, mostrar_barcos=False):
    print("   " + " ".join([str(i + 1).rjust(2) for i in range(tablero.shape[1])]))
    for i, fila in enumerate(tablero):
        fila_mostrar = []
        for casilla in fila:
            if not mostrar_barcos and casilla == BARCO:
                fila_mostrar.append(AGUA)
            else:
                fila_mostrar.append(casilla)
        print(LETRAS_FILAS[i] + "  " + " ".join(c.rjust(2) for c in fila_mostrar))

# ---------------------- COLOCACIÓN AUTOMÁTICA ----------------------

def colocar_barcos_automaticamente(tablero, barcos, lista_barcos):
    for clave, datos in barcos.items():
        nombre, eslora, cantidad = datos
        for _ in range(cantidad):
            colocado = False
            while not colocado:
                fila = random.randint(0, TAM_TABLERO - 1)
                col = random.randint(0, TAM_TABLERO - 1)
                direccion = random.choice(["ar", "ab", "iz", "de"])
                coords = obtener_coordenadas(fila, col, direccion, eslora)
                if validar_colocacion(tablero, coords):
                    for f, c in coords:
                        tablero[f][c] = BARCO
                    lista_barcos.append(coords)
                    colocado = True

# ---------------------- COLOCACIÓN MANUAL ----------------------

def colocar_barcos_manual(tablero, barcos, lista_barcos):
    contador = 1
    for clave, datos in barcos.items():
        nombre, eslora, cantidad = datos
        for i in range(1, cantidad + 1):
            while True:
                print(f"\nColoca la {nombre.lower()} (eslora {eslora}) nº {contador}")
                entrada = input("\n>>> Introduce la coordenada inicial (ej: b4) o 's' para salir:\n> ").strip().lower()
                if entrada == 's':
                    return False
                if len(entrada) < 2 or entrada[0].upper() not in LETRAS_FILAS or not entrada[1:].isdigit():
                    print("Coordenada inválida. Intenta de nuevo.")
                    continue
                fila = LETRAS_FILAS.index(entrada[0].upper())
                col = int(entrada[1:]) - 1
                direccion = input(">>> Introduce la dirección: ar = arriba | ab = abajo | iz = izquierda | de = derecha\n> ").strip().lower()
                if direccion == 's':
                    return False
                coords = obtener_coordenadas(fila, col, direccion, eslora)
                if validar_colocacion(tablero, coords):
                    for f, c in coords:
                        tablero[f][c] = BARCO
                    lista_barcos.append(coords)
                    contador += 1
                    break
                else:
                    print(f"La {nombre.lower()} de eslora {eslora} no se puede colocar ahí. Intenta otra dirección u otra coordenada.")
    return True


# ---------------------- FUNCIONES AUXILIARES ----------------------

def obtener_coordenadas(fila, col, direccion, eslora):
    coords = []
    for i in range(eslora):
        if direccion == "ar":
            coords.append([fila - i, col])
        elif direccion == "ab":
            coords.append([fila + i, col])
        elif direccion == "iz":
            coords.append([fila, col - i])
        elif direccion == "de":
            coords.append([fila, col + i])
    return coords

def validar_colocacion(tablero, coords):
    for f, c in coords:
        if f < 0 or f >= TAM_TABLERO or c < 0 or c >= TAM_TABLERO:
            return False
        if tablero[f][c] != AGUA:
            return False
    return True

# ---------------------- DISPAROS ----------------------

def disparo_jugador(tablero_maquina, disparos_jugador, barcos_maquina):
    while True:
        entrada = input("\n>>> ¡Tu turno! Introduce la coordenada de disparo o 's' para salir:\n> ").strip().lower()
        if entrada == 's':
            return 'salir'
        if len(entrada) < 2 or entrada[0].upper() not in LETRAS_FILAS or not entrada[1:].isdigit():
            print("Coordenada inválida. Intenta de nuevo.")
            continue
        fila = LETRAS_FILAS.index(entrada[0].upper())
        col = int(entrada[1:]) - 1
        if [fila, col] in disparos_jugador:
            print("Ya has disparado ahí. Prueba otra coordenada o 's' para salir.")
            continue
        disparos_jugador.append([fila, col])
        return procesar_disparo(tablero_maquina, fila, col, barcos_maquina, disparos_jugador)


def disparo_maquina(tablero_jugador, disparos_maquina, barcos_jugador):
    print("Turno del adversario...")
    time.sleep(3)
    while True:
        fila = random.randint(0, TAM_TABLERO - 1)
        col = random.randint(0, TAM_TABLERO - 1)
        if [fila, col] not in disparos_maquina:
            disparos_maquina.append([fila, col])
            return procesar_disparo(tablero_jugador, fila, col, barcos_jugador, disparos_maquina, es_maquina=True)

def procesar_disparo(tablero, fila, col, lista_barcos, lista_disparos, es_maquina=False):
    for barco in lista_barcos:
        if [fila, col] in barco:
            tablero[fila][col] = TOCADO
            if all(tablero[f][c] == TOCADO for f, c in barco):
                for f, c in barco:
                    tablero[f][c] = HUNDIDO
                mensaje = "¡Tu adversario ha hundido uno de tus barcos!" if es_maquina else "¡Has hundido un barco enemigo!"
                print(mensaje)
                return "hundido"
            mensaje = "¡Tu adversario ha tocado uno de tus barcos!" if es_maquina else "¡Has tocado un barco enemigo!"
            print(mensaje)
            return "tocado"
    tablero[fila][col] = AGUA_IMPACTADA
    mensaje = "¡Tu adversario ha fallado el disparo!" if es_maquina else "¡Agua!"
    print(mensaje)
    return "agua"

# ---------------------- VISUALIZACIÓN DE 4 TABLEROS ----------------------

def mostrar_tableros_completos(tab_jugador, tab_maquina, disp_jugador, disp_maquina):
    print("\n\n\n\n\n")

    # TÍTULOS
    print("Tablero de barcos del jugador".ljust(36) + "Tablero de barcos del adversario")

    # NÚMEROS DE COLUMNA
    cabecera = "   " + "".join(f"{str(i+1):^3}" for i in range(TAM_TABLERO))
    print(f"{cabecera}{' ' * 6}{cabecera}")

    # TABLEROS DE BARCOS
    for i in range(TAM_TABLERO):
        fila_izq = "".join(f"{c:^3}" for c in tab_jugador[i])
        fila_der = "".join(f"{c:^3}" for c in tab_maquina[i])
        print(f"{LETRAS_FILAS[i]}  {fila_izq}{' ' * 6}{LETRAS_FILAS[i]}  {fila_der}")

    print("\n\n\n\n\n")

    # TÍTULOS DE DISPARO
    print("Tablero de disparos del jugador".ljust(36) + "Tablero de disparos del adversario")
    print(f"{cabecera}{' ' * 6}{cabecera}")

    # TABLEROS DE DISPARO
    for i in range(TAM_TABLERO):
        fila_izq = "".join(f"{c:^3}" for c in disp_jugador[i])
        fila_der = "".join(f"{c:^3}" for c in disp_maquina[i])
        print(f"{LETRAS_FILAS[i]}  {fila_izq}{' ' * 6}{LETRAS_FILAS[i]}  {fila_der}")
    print()


# ---------------------- MODOS DE JUEGO ----------------------

def modo_demo():
    for ronda in range(2):
        print(f"RONDA {ronda + 1} - Dispara el jugador")
        tablero_maquina = crear_tablero()
        tablero_disparos_jugador = crear_tablero()
        barcos_maquina = []
        colocar_barcos_automaticamente(tablero_maquina, {"l": ["Lancha", 2, 1]}, barcos_maquina)
        disparos_jugador = []
        while True:
            mostrar_tableros_completos(crear_tablero(), tablero_maquina, tablero_disparos_jugador, crear_tablero())
            resultado = disparo_jugador(tablero_maquina, disparos_jugador, barcos_maquina)
            if resultado == "salir":
                return
            for f, c in disparos_jugador:
                if tablero_maquina[f][c] in [TOCADO, HUNDIDO]:
                    tablero_disparos_jugador[f][c] = tablero_maquina[f][c]
                elif tablero_maquina[f][c] == AGUA_IMPACTADA:
                    tablero_disparos_jugador[f][c] = AGUA_IMPACTADA
            if all(tablero_maquina[f][c] == HUNDIDO for barco in barcos_maquina for f, c in barco):
                print("¡Barco derribado!")
                if input("Pulsa espacio para continuar o s para volver al menú: ").lower() == "s":
                    return
                break

    for ronda in range(2):
        print(f"RONDA {ronda + 1} - Dispara el adversario")
        tablero_jugador = crear_tablero()
        tablero_disparos_maquina = crear_tablero()
        barcos_jugador = []
        exito = colocar_barcos_manual(tablero_jugador, {"l": ["Lancha", 2, 1]}, barcos_jugador)
        if not exito:
            return
        disparos_maquina = []
        while True:
            mostrar_tableros_completos(tablero_jugador, crear_tablero(), crear_tablero(), tablero_disparos_maquina)
            resultado = disparo_maquina(tablero_jugador, disparos_maquina, barcos_jugador)
            for f, c in disparos_maquina:
                if tablero_jugador[f][c] in [TOCADO, HUNDIDO]:
                    tablero_disparos_maquina[f][c] = tablero_jugador[f][c]
                elif tablero_jugador[f][c] == AGUA_IMPACTADA:
                    tablero_disparos_maquina[f][c] = AGUA_IMPACTADA
            if all(tablero_jugador[f][c] == HUNDIDO for barco in barcos_jugador for f, c in barco):
                print("¡Barco derribado!")
                if input("Pulsa espacio para continuar o s para volver al menú: ").lower() == "s":
                    return
                break

def modo_manual():
    jugar_partida(manual=True)

def modo_automatico():
    jugar_partida(manual=False)

# ---------------------- PARTIDA GENERAL ----------------------

def jugar_partida(manual=False):
    tablero_jugador = crear_tablero()
    tablero_maquina = crear_tablero()
    disparos_jugador = []
    disparos_maquina = []
    tablero_disparos_jugador = crear_tablero()
    tablero_disparos_maquina = crear_tablero()
    barcos_jugador = []
    barcos_maquina = []

    if manual:
        exito = colocar_barcos_manual(tablero_jugador, BARCOS, barcos_jugador)
        if not exito:
            return
    else:
        colocar_barcos_automaticamente(tablero_jugador, BARCOS, barcos_jugador)

    colocar_barcos_automaticamente(tablero_maquina, BARCOS, barcos_maquina)

    turno_jugador = random.choice([True, False])
    print("¡Todo listo! Empieza el jugador." if turno_jugador else "¡Todo listo! Empieza el adversario.")

    while True:
        mostrar_tableros_completos(tablero_jugador, tablero_maquina, tablero_disparos_jugador, tablero_disparos_maquina)

        if turno_jugador:
            resultado = disparo_jugador(tablero_maquina, disparos_jugador, barcos_maquina)
            if resultado == "salir":
                return
            for f, c in disparos_jugador:
                if tablero_maquina[f][c] in [TOCADO, HUNDIDO]:
                    tablero_disparos_jugador[f][c] = tablero_maquina[f][c]
                elif tablero_maquina[f][c] == AGUA_IMPACTADA:
                    tablero_disparos_jugador[f][c] = AGUA_IMPACTADA
            if all(tablero_maquina[f][c] == HUNDIDO for barco in barcos_maquina for f, c in barco):
                print("¡Has ganado, hundiste la flota del adversario!")
                return
            if resultado != "agua":
                continue
        else:
            resultado = disparo_maquina(tablero_jugador, disparos_maquina, barcos_jugador)
            for f, c in disparos_maquina:
                if tablero_jugador[f][c] in [TOCADO, HUNDIDO]:
                    tablero_disparos_maquina[f][c] = tablero_jugador[f][c]
                elif tablero_jugador[f][c] == AGUA_IMPACTADA:
                    tablero_disparos_maquina[f][c] = AGUA_IMPACTADA
            if all(tablero_jugador[f][c] == HUNDIDO for barco in barcos_jugador for f, c in barco):
                print("¡Perdiste, el adversario hundió tu flota!")
                return
            if resultado != "agua":
                continue
        turno_jugador = not turno_jugador
