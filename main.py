import os
import sys
import json
from decimal import Decimal
from datetime import datetime
from dotenv import load_dotenv
from app.AWSConnections import AWSConnections
from app.stock_api import getCurrentPrice


ACCIONES_DISPONIBLES = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

load_dotenv()
os.environ["AWS_SHARED_CREDENTIALS_FILE"] = os.getenv("AWS_SHARED_CREDENTIALS_FILE")
os.environ["AWS_CONFIG_FILE"] = os.getenv("AWS_CONFIG_FILE")
os.environ["AWS_PROFILE"] = os.getenv("AWS_PROFILE")

aws = AWSConnections()
dynamodb = aws.getSession().resource('dynamodb')
tabla = dynamodb.Table('Usuarios')

def registrar_usuario():
    print("\n--- Registro de Usuario ---")
    email = input("Correo electrónico: ").strip()
    nombre = input("Nombre: ").strip()
    respuesta = tabla.get_item(Key={'email': email})
    if 'Item' in respuesta:
        print("Ya existe un usuario con ese correo.")
        return None

    nuevo = {
        'email': email,
        'Nombre': nombre,
        'Saldo': Decimal('15000'),
        'Portafolio': {},
        'Inversiones ': []
    }
    tabla.put_item(Item=nuevo)
    print("Usuario registrado con éxito.")
    return nuevo

def iniciar_sesion():
    print("\n--- Iniciar Sesión ---")
    email = input("Correo electrónico: ").strip()
    respuesta = tabla.get_item(Key={'email': email})
    if 'Item' in respuesta:
        print(f"Bienvenido {respuesta['Item']['Nombre']}")
        return respuesta['Item']
    else:
        print("Usuario no encontrado.")
        return None

def consultar_accion():
    simbolo = input("Ingrese símbolo de acción (ej. AAPL, MSFT): ").strip().upper()
    precio = getCurrentPrice(simbolo)
    if precio:
        print(f"Precio actual de {simbolo}: Q{precio:.2f}")

def invertir(usuario):
    print("\nSímbolos disponibles para invertir:", ', '.join(ACCIONES_DISPONIBLES))
    simbolo = input("Símbolo de la acción: ").strip().upper()
    if simbolo not in ACCIONES_DISPONIBLES:
        print("Símbolo no disponible. Intente con uno de la lista.")
        return

    cantidad = int(input("Cantidad a invertir (en Quetzales): "))
    precio = getCurrentPrice(simbolo)
    if precio is None:
        print("No se pudo obtener el precio.")
        return
    if usuario['Saldo'] < cantidad:
        print("Saldo insuficiente.")
        return
    acciones_compradas = round(cantidad / precio, 4)

    portafolio = usuario.get('Portafolio', {})
    if simbolo in portafolio:
        portafolio[simbolo] += Decimal(str(acciones_compradas))
    else:
        portafolio[simbolo] = Decimal(str(acciones_compradas))
    usuario['Portafolio'] = portafolio

    usuario['Saldo'] -= Decimal(str(cantidad))

    usuario['Inversiones '].append({
        'simbolo': simbolo,
        'precio': Decimal(str(precio)),
        'cantidad': Decimal(str(cantidad)),
        'acciones': Decimal(str(acciones_compradas)),
        'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

    tabla.put_item(Item=usuario)
    print(f"Inversión realizada: {acciones_compradas} acciones de {simbolo} a Q{precio:.2f}")

def mostrar_portafolio(usuario):
    print("\n--- Portafolio ---")
    portafolio = usuario.get('Portafolio', {})
    inversiones = usuario.get('Inversiones ', [])

    if not portafolio:
        print("No hay acciones en el portafolio.")
        return

    resumen = {}
    for inv in inversiones:
        simbolo = inv['simbolo']
        if simbolo not in resumen:
            resumen[simbolo] = {'total_invertido': Decimal('0'), 'acciones': Decimal('0')}
        resumen[simbolo]['total_invertido'] += Decimal(str(inv['cantidad']))
        resumen[simbolo]['acciones'] += Decimal(str(inv['acciones']))

    for simbolo, cantidad in portafolio.items():
        precio_actual = getCurrentPrice(simbolo)
        if precio_actual is None:
            print(f"{simbolo}: Error al obtener precio actual.")
            continue

        acciones = resumen[simbolo]['acciones']
        invertido = resumen[simbolo]['total_invertido']
        precio_promedio = invertido / acciones if acciones > 0 else Decimal('0')
        valor_actual = precio_actual * float(cantidad)
        ganancia = valor_actual - float(invertido)

        print(f"{simbolo}:")
        print(f"  Acciones: {cantidad}")
        print(f"  Precio Promedio Compra: Q{precio_promedio:.2f}")
        print(f"  Precio Actual: Q{precio_actual:.2f}")
        print(f"  Valor Actual: Q{valor_actual:.2f}")
        print(f"  Ganancia/Pérdida: Q{ganancia:.2f}")

def consultar_saldo(usuario):
    print(f"Saldo actual: Q{usuario['Saldo']}")

def resumen_inversiones(usuario):
    print("\n--- Resumen de Inversiones ---")
    for inv in usuario.get('Inversiones ', []):
        print(f"{inv['fecha']} - {inv['simbolo']}: Q{inv['cantidad']} por {inv['acciones']} acciones a Q{inv['precio']}")

def menu_usuario(usuario):
    while True:
        print("""
\n--- MENÚ PRINCIPAL ---
1. Consultar acciones disponibles
2. Invertir en acciones
3. Ver portafolio
4. Consultar saldo
5. Ver resumen de inversiones
6. Salir
""")
        op = input("Seleccione una opción: ")
        if op == '1':
            consultar_accion()
        elif op == '2':
            invertir(usuario)
        elif op == '3':
            mostrar_portafolio(usuario)
        elif op == '4':
            consultar_saldo(usuario)
        elif op == '5':
            resumen_inversiones(usuario)
        elif op == '6':
            print("Sesión finalizada.")
            break
        else:
            print("Opción inválida.")

def menu_inicio():
    while True:
        print("""
--- MENÚ DE INICIO ---
1. Iniciar sesión
2. Registrarse
3. Salir
""")
        op = input("Seleccione una opción: ")
        if op == '1':
            user = iniciar_sesion()
            if user:
                menu_usuario(user)
        elif op == '2':
            user = registrar_usuario()
            if user:
                menu_usuario(user)
        elif op == '3':
            print("Gracias por usar el sistema.")
            break
        else:
            print("Opción inválida.")

if __name__ == '__main__':
    menu_inicio()
