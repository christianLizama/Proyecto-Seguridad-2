"""
Código para descifrar mensajes usando Fernet.
"""

import os
import argparse
import sys

from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

class Decryptor:
    """
    Clase para descifrar mensajes cifrados usando Fernet.
    """

    def __init__(self):
        """
        Inicializa el descifrador con la clave de cifrado.
        """
        self.key = self.load_key()
        self.cipher_suite = Fernet(self.key)

    def load_key(self) -> bytes:
        """
        Carga la clave de cifrado desde un archivo.

        :return: Clave de cifrado en bytes
        """
        passfile = os.environ.get("passfile")
        if not passfile:
            print("Error: La variable de entorno 'passfile' no está definida.")
            sys.exit(1)
        return open(passfile, 'rb').read()

    def decrypt_message(self, encrypted_message: bytes) -> str:
        """
        Descifra un mensaje cifrado.

        :param encrypted_message: Mensaje cifrado en bytes
        :return: Mensaje descifrado en texto
        """
        decrypted_message = self.cipher_suite.decrypt(encrypted_message)
        return decrypted_message.decode()

    def decrypt_file(self, file_path: str):
        """
        Descifra un archivo de texto cifrado.

        :param file_path: Ruta del archivo cifrado
        """
        if not file_path.endswith('.txt'):
            print("Error: El archivo proporcionado no es un archivo .txt")
            return

        try:
            with open(file_path, 'rb') as file:
                encrypted_message = file.read()
            decrypted_message = self.decrypt_message(encrypted_message)
            print("Decrypted message:", decrypted_message)
        except Exception as e:
            print(f"Error al leer o descifrar el archivo: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Descifrar un archivo de texto cifrado usando Fernet.")
    parser.add_argument('file', type=str, help='Ruta del archivo .txt cifrado a descifrar.')
    args = parser.parse_args()

    decryptor = Decryptor()
    decryptor.decrypt_file(args.file)
