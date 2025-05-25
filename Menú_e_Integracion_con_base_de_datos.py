import uuid
import boto3
from botocore.exceptions import ClientError
from datetime import datetime

# Configuración DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Cambia región de Aws si es us-east-1 o us-east-2

#  Funciones de DynamoDB (Persona 5) agregada

def guardar_usuario(usuario):
    try:
        tabla = dynamodb.Table('Usuarios')
        tabla.put_item(Item=usuario)
    except ClientError as e:
        print("Error al guardar usuario:", e)

def obtener_usuario(user_id):
    try:
        tabla = dynamodb.Table('Usuarios')
        response = tabla.get_item(Key={'user_id': user_id})
        return response.get('Item', None)
    except ClientError as e:
        print("Error al obtener usuario:", e)
        return None

def guardar_inversion(inversion):
    try:
        tabla = dynamodb.Table('Inversiones')
        tabla.put_item(Item=inversion)
    except ClientError as e:
        print("Error al guardar inversión:", e)

def obtener_inversiones(user_id):
    try:
        tabla = dynamodb.Table('Inversiones')
        response = tabla.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr('user_id').eq(user_id)
        )
        return response.get('Items', [])
    except ClientError as e:
        print("Error al obtener inversiones:", e)
        return []

# Menú

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

# --- Funciones a implementar por otras personas (marcadas para completar) ---

def crear_usuario():
    # Aquí implementa Persona 2, aquí un ejemplo básico con integración a DynamoDB
    nombre = input("Ingrese nombre de usuario: ").strip()
    if not nombre:
        print("El nombre no puede estar vacío.")
        return
    correo = input("Ingrese correo electrónico (opcional): ").strip()
    user_id = str(uuid.uuid4())
    saldo_inicial = 1000.0  # saldo virtual inicial fijo
    
    # Validar que usuario no exista (simplificado)
    # Idealmente, buscar en DynamoDB por correo osea lo que dijo el inge para evitar duplicados
    # Aquí omitido para simplificar

    usuario = {
        'user_id': user_id,
        'nombre': nombre,
        'correo': correo,
        'saldo': saldo_inicial
    }
    guardar_usuario(usuario)
    print(f"Usuario creado con ID: {user_id} y saldo inicial de Q{saldo_inicial:.2f}")

def consultar_acciones():
    print("Función consultar_acciones A implementar...")
    # La persona 3 implementa esto

def invertir_en_acciones():
    print("Función invertir_en_acciones A implementar...")
    # La persona 4 implementa esto

def ver_portafolio():
    print("Función ver_portafolio A implementar...")
    # La persona 4 implementa esto

def consultar_saldo_y_resumen():
    user_id = input("Ingrese su ID de usuario: ").strip()
    usuario = obtener_usuario(user_id)
    if usuario:
        print(f"\nNombre: {usuario.get('nombre')}")
        print(f"Correo: {usuario.get('correo')}")
        print(f"Saldo actual: Q{usuario.get('saldo', 0):.2f}")
        
        inversiones = obtener_inversiones(user_id)
        if inversiones:
            total_invertido = sum(float(inv['amount']) for inv in inversiones)
            print(f"Total invertido: Q{total_invertido:.2f}")
            print(f"Cantidad de inversiones: {len(inversiones)}")
        else:
            print("No se encontraron inversiones registradas.")
    else:
        print("Usuario no encontrado.")

def mostrar_reporte_general():
    print("\n Reporte General del Sistema ")
    tabla = dynamodb.Table('Usuarios')
    try:
        response = tabla.scan()
        usuarios = response.get('Items', [])
        print(f"Total de usuarios registrados: {len(usuarios)}")
        for u in usuarios:
            print(f"- {u['nombre']} ({u['user_id']}) - Saldo: Q{u.get('saldo', 0):.2f}")
    except ClientError as e:
        print("Error al consultar usuarios:", e)

# Punto de entrada del programa 

if __name__ == "__main__":
    ejecutar_menu()