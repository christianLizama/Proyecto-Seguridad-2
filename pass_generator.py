"""
Este script genera una clave secreta y la guarda en un archivo
"""

from cryptography.fernet import Fernet

# Generar y guardar una clave
key = Fernet.generate_key()
with open('secret.key', 'wb') as key_file:
    key_file.write(key)
