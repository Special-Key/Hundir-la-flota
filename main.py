# main.py

from utils import modo_demo, modo_manual, modo_automatico

# Muestra el menú principal y gestiona la selección de modo
def mostrar_menu():
    print("\nBienvenido a Hundir la Flota\n")
    print("Selecciona un modo de juego:")
    print("1 - Modo demo")
    print("2 - Modo manual")
    print("3 - Modo automático")
    print("S - Salir del juego")

# Lógica principal del programa
def main():
    while True:
        mostrar_menu()
        opcion = input("Introduce tu elección: ").lower()

        if opcion == "1":
            modo_demo()
        elif opcion == "2":
            modo_manual()
        elif opcion == "3":
            modo_automatico()
        elif opcion == "s":
            print("Gracias por jugar. ¡Hasta la próxima!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")
            continue

        volver = input("¿Volver al menú principal? (s/n): ").lower()
        if volver != "s":
            print("Gracias por jugar. ¡Hasta la próxima!")
            break

# Ejecuta el juego solo si este archivo es el principal
if __name__ == "__main__":
    main()
