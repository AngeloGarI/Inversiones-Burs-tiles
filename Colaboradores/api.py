import requests

from dotenv import api_key 
URL = 'https://twelvedata.com/marketsgit {api_key} '

def obtener_precio_accion(simbolo):

    params = {
        'symbol': simbolo,
        'apikey': api_key
    }

    try:
        response = requests.get(URL, params=params)
        data = response.json()

        if 'price' in data:
            print(f"Símbolo: {simbolo} - Precio: ${data['price']}")
        elif 'message' in data:
            print(f"Error de API: {data['message']}")
        else:
            print("Error desconocido en la respuesta de la API.")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
    except ValueError:
        print("Error al procesar los datos (respuesta no es JSON válido).")

# Ejemplo de uso
acciones = ['AAPL', 'TSLA', 'FERRARI80']

for simbolo in acciones:
    obtener_precio_accion(simbolo)
