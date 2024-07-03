"""
Este script genera una clave secreta y la guarda en un archivo
"""
import os
import sys

from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

# Verificar si la variable de entorno 'passfile' está definida
passfile = os.environ.get("passfile")
if not passfile:
    print("Error: La variable de entorno 'passfile' no está definida.")
    sys.exit(1)

# Generar y guardar una clave
key = Fernet.generate_key()
try:
    with open(passfile, 'wb') as key_file:
        key_file.write(key)
    # Mostrar un mensaje cuando se crea la clave
    print("La clave secreta se ha generado y guardado correctamente.")
except Exception as e:
    print(f"Error al guardar la clave en el archivo: {e}")
    sys.exit(1)
