import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
BASE_URL = 'https://api.twelvedata.com/price'

balance = 15000
portfolio = []
history = []

def getCurrentPrice(symbol):
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

def invest():
    global balance
    symbol = input("Ingresa el símbolo de la acción (ej. AAPL): ").upper()
    price = getCurrentPrice(symbol)
    if price is None:
        print("Símbolo no válido o no disponible.")
        return

    try:
        amount = float(input(f"¿Cuánto quieres invertir en {symbol}? $"))
    except ValueError:
        print("Por favor, ingresa un número válido.")
        return

    if amount > balance:
        print("No tienes suficiente saldo.")
        return

    quantity = amount / price
    balance -= amount
    portfolio.append({"symbol": symbol, "quantity": quantity, "purchasePrice": price})
    history.append({"symbol": symbol, "quantity": quantity, "amountInvested": amount})
    print(f"Inversión realizada: {quantity:.2f} acciones de {symbol} a ${price} cada una.")

def showPortfolio():
    totalValue = 0
    print("\n--- Portafolio Actual ---")
    for stock in portfolio:
        symbol = stock["symbol"]
        quantity = stock["quantity"]
        currentPrice = getCurrentPrice(symbol)
        if currentPrice is None:
            currentPrice = stock["purchasePrice"]
        currentValue = quantity * currentPrice
        investedValue = quantity * stock["purchasePrice"]
        profit = currentValue - investedValue
        totalValue += currentValue
        print(f"{symbol}: {quantity:.2f} acciones")
        print(f"  Precio actual: ${currentPrice}")
        print(f"  Valor actual: ${currentValue:.2f}")
        print(f"  Ganancia/Pérdida: ${profit:.2f}\n")

    print(f"Valor total del portafolio: ${totalValue:.2f}")
    print(f"Saldo disponible: ${balance:.2f}")

def showHistory():
    print("\n--- Historial de Inversiones ---")
    for i, inv in enumerate(history, 1):
        print(f"{i}. {inv['symbol']}: {inv['quantity']:.2f} acciones, Monto invertido: ${inv['amountInvested']:.2f}")

def menu():
    while True:
        print("\n1. Invertir")
        print("2. Ver portafolio")
        print("3. Ver historial")
        print("4. Salir")
        option = input("Selecciona una opción: ")

        if option == "1":
            invest()
        elif option == "2":
            showPortfolio()
        elif option == "3":
            showHistory()
        elif option == "4":
            print("Gracias por usar el sistema.")
            break
        else:
            print("Opción no válida.")
menu()