# Encryption key generator
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = open("encryption_key.txt", 'wb')
f.write(key)
f.close()