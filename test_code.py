from cryptography.fernet import Fernet
import csv
"""These are test functions for the fernet crytpography. The orginal test file is nba.csv
	New files are created. One with encrypted data from nba.csv and one that has been decrypted
    The following code was"""
def generate_key():
    key = Fernet.generate_key()
    with open('filekey.key', 'wb') as filekey:
        filekey.write(key)

def encrypt_file(input_filename, key):
    fernet = Fernet(key)
    with open(input_filename, 'r') as file:
        original = file.read()
    encrypted = fernet.encrypt(original.encode())
    with open('encrypted_file.enc', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

def decrypt_file(output_filename, key):
    fernet = Fernet(key)
    with open('encrypted_file.enc', 'rb') as enc_file:
        encrypted = enc_file.read()
    decrypted = fernet.decrypt(encrypted).decode()
    with open(output_filename, 'w') as dec_file:
        dec_file.write(decrypted)

if __name__ == "__main__":
    # Generate and save a key
    generate_key()

    # Using the saved key for encryption and decryption
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()

    # Encrypt the original CSV file
    encrypt_file('nba.csv', key)

    # Decrypt the encrypted file
    decrypt_file('decrypted_file.csv', key)

# from tkinter import *
# from tkinter import filedialog
# from cryptography.fernet import Fernet


"""The commented out encrypt_file method under this docstring is working. 
        However it is not as good as the similar function in test_code.py.
        The main issue with this method is that I had a hard time trying to get access to the key to decrypt
        when using another method or another class for decryption.
        That version generates new files for the encrypted version and decrypted version while preserving the original"""
        # def encrypt_file(self, file_path):
            
        
        #     key = Fernet.generate_key()
        #     #using file_io to write key to file
        #     with open('filekey.key', 'wb') as filekey:
        #         filekey.write(key)
        #     # opening the key
        #     with open('filekey.key', 'rb') as filekey:
        #         key = filekey.read()

        #     # using the generated key
        #     fernet = Fernet(key)

        #     # opening the original file to encrypt
        #     with open(file_path, 'rb') as file:
        #         original = file.read()
                
        #     # encrypting the file
        #     encrypted = fernet.encrypt(original)

        #     # opening the file in write mode and 
        #     # writing the encrypted data
        #     with open(file_path, 'wb') as encrypted_file:
        #         encrypted_file.write(encrypted)

        #     print(f"Encrypting file: {file_path}")
