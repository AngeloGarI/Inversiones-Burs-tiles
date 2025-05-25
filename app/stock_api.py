import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
BASE_URL = 'https://api.twelvedata.com/price'

def getCurrentPrice(symbol):
    """
    Consulta el precio actual de la acción usando la API de Twelve Data.
    """
    params = {
        'symbol': symbol,
        'apikey': API_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        if 'price' in data:
            return float(data['price'])
        elif 'message' in data:
            print(f"Error de API: {data['message']}")
        else:
            print("Error desconocido en la respuesta de la API.")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
    return None
