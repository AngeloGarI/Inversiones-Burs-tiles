import uuid


def mostrar_menu():
    print("\n Sistema de Inversiones Bursátiles ")
    print("1. Crear usuario")
    print("2. Consultar acciones disponibles")
    print("3. Invertir en acciones")
    print("4. Ver portafolio")
    print("5. Consultar saldo y resumen")
    print("6. Mostrar reporte general")
    print("7. Salir")

def ejecutar_menu():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-7): ").strip()
        
        if opcion == "1":
            crear_usuario()
        elif opcion == "2":
            consultar_acciones()
        elif opcion == "3":
            invertir_en_acciones()
        elif opcion == "4":
            ver_portafolio()
        elif opcion == "5":
            consultar_saldo_y_resumen()
        elif opcion == "6":
            mostrar_reporte_general()
        elif opcion == "7":
            print("Gracias por usar el sistema. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# Aquí tienen que completar con la parte que les correspondió

def crear_usuario():
    # La persona 2 implementa esto
    print("Función crear_usuario A implementar...")

def consultar_acciones():
    # La persona 3 implementa esto
    print(" Función consultar_acciones A implementar...")

def invertir_en_acciones():
    # La persona 4 implementa esto
    print(" Función invertir_en_acciones A implementar...")

def ver_portafolio():
    # La persona 4 implementa esto
    print(" Función ver_portafolio A implementar...")

def consultar_saldo_y_resumen():
    # La persona 5 implementa esto
    print(" Función consultar_saldo_y_resumen A implementar...")

def mostrar_reporte_general():
    # La persona 5 implementa esto
    print(" Función mostrar_reporte_general A implementar...")

# Este será el punto de entrada del programa
if __name__ == "__main__":
    ejecutar_menu()