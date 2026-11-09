#!/usr/bin/env python3
import sys
import os
from hashlib import pbkdf2_hmac
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

def encrypt(password, text):
    salt = os.urandom(8)
    key_iv = pbkdf2_hmac('sha256', password.encode(), salt, 10000, dklen=32)
    key = key_iv[:16]
    iv = key_iv[16:]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(text, AES.block_size)
    ciphertext = cipher.encrypt(padded)
    return b"Salted__" + salt + ciphertext

def decrypt(password, data):
    if data[:8] != b"Salted__":
        raise ValueError("Encabezado inválido (falta 'Salted__')")

    salt = data[8:16]
    ciphertext = data[16:]
    key_iv = pbkdf2_hmac('sha256', password.encode(), salt, 10000, dklen=32)
    key = key_iv[:16]
    iv = key_iv[16:]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = cipher.decrypt(ciphertext)
    return unpad(padded, AES.block_size)



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: xaes.py [-e|-d] <contraseña>")
        sys.exit(1)

    operation = sys.argv[1]
    password = sys.argv[2]
    data = sys.stdin.buffer.read()

    if operation == '-e':
        try:
            encrypted_data = encrypt(password, data)
            sys.stdout.buffer.write(encrypted_data)
        except ValueError as e:
            print(f"Error durante el cifrado: {e}")
            sys.exit(1)
    elif operation == '-d':
        try:
            decrypted_data = decrypt(password, data)
            sys.stdout.buffer.write(decrypted_data)
        except ValueError as e:
            print(f"Error durante el descifrado: {e}")
            sys.exit(1)

    else:
        print("Operación no válida. Use -e para cifrar o -d para descifrar.")
        sys.exit(1)