# Inversiones Bursátiles

Este sistema permite a los usuarios registrarse, iniciar sesión, consultar acciones, invertir, ver su portafolio y revisar el historial de inversiones. Utiliza AWS DynamoDB para almacenar datos y una API para consultar precios en tiempo real.

## Requisitos

- Python 3.8 o superior  
- Git  
- AWS CLI configurado con un perfil válido  
- Archivo `.env` con credenciales de AWS  
- API Key para precios de acciones (configurada en `app/stock_api.py`)

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/AngeloGarI/Inversiones-Burs-tiles.git
   cd INVERSIONES
Crear y activar el entorno virtual:

python -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate
Instalar dependencias:

pip install -r requirements.txt
Crear el archivo .env en la raíz del proyecto con el siguiente contenido:

AWS_SHARED_CREDENTIALS_FILE=path/a/credentials
AWS_CONFIG_FILE=path/a/config
AWS_PROFILE=default

    Ejecución
Para iniciar el sistema:
python main.py

Desde ahí podrás:
Registrar o iniciar sesión como usuario
Consultar acciones disponibles
Invertir en acciones disponibles
Ver portafolio con ganancias o pérdidas
Consultar saldo
Ver resumen de inversiones
📂 Estructura del Proyecto


Inversiones/
├── app/
│   ├── AWSConnections.py
│   └── stock_api.py
|── Colaboradore/
│   ├── api.py, Registro(Andres)
│   └── perona4.py , Menú_e_integracion_con_base_de_datos_
├── main.py
├── requirements.txt
└── .env

📌 Notas
El portafolio y las inversiones se almacenan por usuario en DynamoDB.
Las acciones disponibles están predefinidas y se muestran antes de invertir.
Se calcula automáticamente la ganancia o pérdida actual de cada acción en el portafolio.