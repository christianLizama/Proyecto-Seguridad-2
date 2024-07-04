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
        passfile = os.environ.get("pf")
        if not passfile:
            print("Error: La variable de entorno 'pf' no está definida.")
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
            with open(file_path, 'r') as file:
                lines = file.readlines()
                
            for line in lines:
                if line.startswith("Encrypted Log:"):
                    encrypted_message = line.split("Encrypted Log:")[1].strip()
                    decrypted_message = self.decrypt_message(encrypted_message.encode())
                    print("Decrypted message:", decrypted_message)
                    return

            print("Error: No se encontró 'Encrypted Log:' en el archivo.")

        except Exception as e:
            print(f"Error al leer o descifrar el archivo: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Descifrar un archivo de texto cifrado usando Fernet.")
    parser.add_argument('--file', type=str, help='Ruta del archivo .txt cifrado a descifrar.')
    parser.add_argument('--message', type=str, help='Mensaje cifrado a descifrar.')
    args = parser.parse_args()

    decryptor = Decryptor()

    if args.file:
        decryptor.decrypt_file(args.file)
    elif args.message:
        decrypted_message = decryptor.decrypt_message(args.message.encode())
        print("Decrypted message:", decrypted_message)
    else:
        print("Error: Debe proporcionar un archivo o un mensaje cifrado.")
