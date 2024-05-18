from PIL import ImageTk
import string
import random
import hashlib
import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

FONT = 'Ubuntu'
TITLE_SIZE = 20
TEXT_SIZE = 12

server_url = "https://otherturt.pythonanywhere.com/"

def stretch_image(image, image_ratio, canvas, event):
    global resized_tk
    canvas_ratio = int(event.width / event.height)

    if canvas_ratio > image_ratio:
        height = int(event.height)
        width = int(height * image_ratio)
    else:
        width = int(event.width)
        height = int(width / image_ratio)

    resized_image = image.resize((width, height))
    resized_tk = ImageTk.PhotoImage(resized_image)
    canvas.create_image(
        int(event.width / 2), 
        int(event.height / 2), 
        image=resized_tk, 
        anchor = 'center'
    )

def fill_image(image, image_ratio, canvas, event):
    global resized_tk

    canvas_ratio = event.width / event.height

    if canvas_ratio > image_ratio:
        width = int(event.width)
        height = int(width / image_ratio)
    else:
        height = int(event.height)
        width = int(height * image_ratio)

    resized_image = image.resize((width, height))
    resized_tk = ImageTk.PhotoImage(resized_image)
    canvas.create_image(
        int(event.width / 2), 
        int(event.height / 2), 
        image=resized_tk, 
        anchor = 'center'
    )

def generate_password(length):
    symbols = "@$!%*?&"
    password = ''

    while not (any(c in string.ascii_lowercase for c in password) and
               any(c in string.ascii_uppercase for c in password) and
               any(c in string.digits for c in password) and
               any(c in symbols for c in password) and
               len(password) == length):
        password = ''.join(random.choices(string.ascii_letters + string.digits + symbols, k=length))

    return password

def hash_password(password):
    # Append the salt to the password
    password = password.encode('utf-8')

    # Hash the salted password
    m = hashlib.sha256()
    m.update(password)

    # Return the hashed password along with the salt
    return m.hexdigest()

def derive_key(password: str, salt: bytes) -> bytes:
    """Derives a 32-byte key from the password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_aes(password: str, plaintext: str) -> bytes:
    """Encrypts a plaintext string using AES encryption with a password."""
    backend = default_backend()
    salt = os.urandom(16)  # Generate a random salt
    key = derive_key(password, salt)
    
    iv = os.urandom(16)  # Generate a random initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)
    encryptor = cipher.encryptor()
    
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    combined = salt + iv + ciphertext
    return base64.b64encode(combined).decode('utf-8')

def decrypt_aes(password: str, b64_ciphertext: str) -> str:
    """Decrypts a ciphertext string using AES encryption with a password."""
    backend = default_backend()
    ciphertext = base64.b64decode(b64_ciphertext)
    salt = ciphertext[:16]
    iv = ciphertext[16:32]
    actual_ciphertext = ciphertext[32:]
    
    key = derive_key(password, salt)
    
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)
    decryptor = cipher.decryptor()
    
    decrypted_data = decryptor.update(actual_ciphertext) + decryptor.finalize()
    return decrypted_data.decode()