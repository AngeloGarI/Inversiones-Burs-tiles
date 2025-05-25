import os
import sys
import json
from decimal import Decimal
from datetime import datetime
from dotenv import load_dotenv
from app.AWSConnections import AWSConnections
from app.stock_api import getCurrentPrice

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
    # Verificar si ya existe
    respuesta = tabla.get_item(Key={'email': email})
    if 'Item' in respuesta:
        print("Ya existe un usuario con ese correo.")
        return None
    
    nuevo = {
        'email': email,
        'Nombre': nombre,
        'Saldo': Decimal('1000'),
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
        print(f"Precio actual de {simbolo}: ${precio:.2f}")

def invertir(usuario):
    simbolo = input("Símbolo de la acción: ").strip().upper()
    cantidad = int(input("Cantidad a invertir (en dólares): "))
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
    # Guardar en tabla
    tabla.put_item(Item=usuario)
    print(f"Inversión realizada: {acciones_compradas} acciones de {simbolo} a ${precio:.2f}")

def mostrar_portafolio(usuario):
    print("\n--- Portafolio ---")
    portafolio = usuario.get('Portafolio', {})
    if not portafolio:
        print("No hay acciones en el portafolio.")
    for simbolo, cantidad in portafolio.items():
        print(f"{simbolo}: {cantidad} acciones")

def consultar_saldo(usuario):
    print(f"Saldo actual: ${usuario['Saldo']}")

def resumen_inversiones(usuario):
    print("\n--- Resumen de Inversiones ---")
    for inv in usuario.get('Inversiones ', []):
        print(f"{inv['fecha']} - {inv['simbolo']}: ${inv['cantidad']} por {inv['acciones']} acciones a ${inv['precio']}")

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
