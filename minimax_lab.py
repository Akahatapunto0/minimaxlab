import random

FILAS = 6
COLUMNAS = 6
PROFUNDIDAD_MINIMAX = 3
TURNOS_ALEATORIOS = 4
MAX_TURNOS = 50

RATON = "🐭"
GATO = "😺"
QUESO = "🧀"
VACIO = "."

DIRECCIONES = [(-1,0), (1,0), (0,-1), (0,1)]

# POSICIONES INICIALES
POS_GATO = (0,0) 
POS_RATON = (FILAS -1, COLUMNAS -1)
POS_QUESO = (0,COLUMNAS -1)

def crear_tablero():
    tablero = [[VACIO for _ in range(COLUMNAS)] for _ in range(FILAS)]
    tablero[POS_QUESO[0]][POS_QUESO[1]] = QUESO
    return tablero

def mostrar_tablero(tablero):
    for fila in tablero:
        print(" ".join(fila))
    print()

def obtener_mov_validos(posicion):
    """Devuelve movimientos válidos como tuplas."""
    movimientos = []
    fil, col = posicion
    for dfil, dcol in DIRECCIONES:
        nfil, ncol = fil + dfil, col + dcol
        if 0 <= nfil < FILAS and 0 <= ncol < COLUMNAS:
            movimientos.append((nfil, ncol))  # ahora siempre tupla
    return movimientos

def mover_aleatoriamente(posicion):
    """Elige un movimiento válido al azar; si no hay, devuelve la misma posición."""
    opciones = obtener_mov_validos(posicion)
    if opciones:
        return random.choice(opciones)
    return posicion

def distancia_manhatthan(a,b):
    """Distancia Manhattan entre dos posiciones."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def evaluar_posicion(pos_raton, pos_gato, pos_queso):
    """
    Heurística: mayor valor = mejor para el ratón.
    Favor: estar lejos del gato.
    Penaliza: estar lejos del queso.
    """
    d_queso = distancia_manhatthan(pos_raton, pos_queso)
    d_gato = distancia_manhatthan(pos_raton, pos_gato)
    return d_gato - 2 * d_queso

# ========== MINIMAX ==========

def minimax(pos_raton, pos_gato, pos_queso, profundidad, es_turno_max):
    # Casos terminales
    if pos_raton == pos_queso:
        return 10000, pos_raton  # ratón gana
    if pos_raton == pos_gato:
        return -10000, pos_raton  # gato atrapa ratón
    if profundidad == 0:
        return evaluar_posicion(pos_raton, pos_gato, pos_queso), pos_raton

    if es_turno_max:  # turno del ratón
        mejor_valor = float('-inf')
        mejor_movimiento = pos_raton
        for nueva in obtener_mov_validos(pos_raton):
            valor, _ = minimax(nueva, pos_gato, pos_queso, profundidad - 1, False)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = nueva
        return mejor_valor, mejor_movimiento

    else:  # turno del gato
        peor_valor = float('inf')
        peor_movimiento = pos_gato
        for nueva in obtener_mov_validos(pos_gato):
            valor, _ = minimax(pos_raton, nueva, pos_queso, profundidad - 1, True)
            if valor < peor_valor:
                peor_valor = valor
                peor_movimiento = nueva
        return peor_valor, peor_movimiento

# ========== BUCLE PRINCIPAL ==========

def jugar():
    pos_raton = POS_RATON  # ya son tuplas, no necesitan copy
    pos_gato = POS_GATO

    for turno in range(1, MAX_TURNOS + 1):
        tablero = crear_tablero()
        tablero[pos_raton[0]][pos_raton[1]] = RATON
        tablero[pos_gato[0]][pos_gato[1]] = GATO

        print(f"--- TURNO {turno} ---")
        mostrar_tablero(tablero)

        # Chequeos inmediatos
        if pos_raton == POS_QUESO:
            print("🐭 ¡El ratón llegó al Queso y escapó!")
            return
        if pos_raton == pos_gato:
            print("🐱 ¡El gato atrapó al ratón!")
            return

        # 1) Movimiento del ratón
        if turno <= TURNOS_ALEATORIOS:
            print("Ratón se mueve aleatoriamente.")
            pos_raton = mover_aleatoriamente(pos_raton)
        else:
            print("Ratón usa Minimax para intentar escapar.")
            _, pos_raton = minimax(pos_raton, pos_gato, POS_QUESO, PROFUNDIDAD_MINIMAX, True)

        # Verificar tras movimiento del ratón
        if pos_raton == POS_QUESO:
            tablero = crear_tablero()
            tablero[pos_raton[0]][pos_raton[1]] = RATON
            tablero[pos_gato[0]][pos_gato[1]] = GATO
            mostrar_tablero(tablero)
            print("🐭 ¡El ratón llegó al Queso y escapó!")
            return
        if pos_raton == pos_gato:
            tablero = crear_tablero()
            tablero[pos_raton[0]][pos_raton[1]] = RATON
            tablero[pos_gato[0]][pos_gato[1]] = GATO
            mostrar_tablero(tablero)
            print("🐱 ¡El gato atrapó al ratón por colisión!")
            return

        # 2) Movimiento del gato
        print("Gato usa Minimax para acorralar.")
        _, pos_gato = minimax(pos_raton, pos_gato, POS_QUESO, PROFUNDIDAD_MINIMAX, False)

        # Verificar tras movimiento del gato
        if pos_gato == pos_raton:
            tablero = crear_tablero()
            tablero[pos_raton[0]][pos_raton[1]] = RATON
            tablero[pos_gato[0]][pos_gato[1]] = GATO
            mostrar_tablero(tablero)
            print("🐱 ¡El gato atrapó al ratón!")
            return

    print("⏳ Se alcanzó el límite de turnos. Empate / el ratón no logró escapar.")

if __name__ == "__main__":
    jugar()