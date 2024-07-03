"""
    Código para descifrar mensajes usando Fernet.
"""
import os

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
        return open(os.environ.get("passfile"), 'rb').read()

    def decrypt_message(self, encrypted_message: bytes) -> str:
        """
        Descifra un mensaje cifrado.

        :param encrypted_message: Mensaje cifrado en bytes
        :return: Mensaje descifrado en texto
        """
        decrypted_message = self.cipher_suite.decrypt(encrypted_message)
        return decrypted_message.decode()

if __name__ == "__main__":
    ENCRYPTED_MESAGGE = b"gAAAAABmff1B5UKvmpVMGqui6F3Cbenq5V0SQuJhltMwFFN181rM3e9mA0r1XEH_ywXROG6IcISw650HvTD8O8K1qj8dvGhNr4iG2tb000BzLOFOZ9YMK_K_vutbce292hPxFmpcs3eLUXZr07eTKJMwlFEMjmVwXbRlEKMn7ZbwuQrzewl5AUuQWCZkpgRI2aLv4FvRnY27IpC0NscOq_q-YxVaWNf9wTx5cCHnWhl89yry3h3m58IWwKN6rhKlPFvHrtT-aOHbYUpoItVd3d1Vs3c8P10vuQ=="
    decryptor = Decryptor()
    print("Encrypted message:", ENCRYPTED_MESAGGE)
    decrypted_message_result = decryptor.decrypt_message(ENCRYPTED_MESAGGE)
    print("Decrypted message:", decrypted_message_result)
