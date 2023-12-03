# tkinter is for the GUI modules. File dialogue gives me access to file explorer
# cryptography.fernet gives me accesss to a crypto class so we can encrypt and decrypt a chosen file
from tkinter import *
from tkinter import filedialog
from cryptography.fernet import Fernet

class BaseWindow:
    """This class will hold roots that will be used to create the GUI window.
    The class will be inherited by File explorer and Application classes."""
    def __init__(self, root):
        self.root = root
        self.root.title('File Explorer')
        self.root.geometry("500x500")
        self.root.config(background="white")

class FileExplorer(BaseWindow):
    """This class has inherited BaseWindow and will create the label for displaying file path.
    It will also creat the button for browsing the filesystem"""
    def __init__(self, root):
        """Generate lablels and button for browsing files"""
        super().__init__(root)#super is used to inherit basewindow 
        self.file_label = Label(root, text="Choose a file", width=100, height=4, fg="blue")
        self.file_label.grid(column=1, row=1)
        
        #Button for viewing files in a GUI very much like file explorer.
        self.button_explore = Button(root, text="Browse Files", command=self.browse_files)
        self.button_explore.grid(column=1, row=2)

        #This function will execute the filedialogue code that allows make it possible to browse the files like file explorer
    def browse_files(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                               filetypes=(("All files", "*.*"),))
        self.file_label.configure(text="File Opened: " + filename)

class CryptoHandler:
    def __init__(self):
        self._key = None
        self.key_file = None
        self.generate_key()

    def generate_key(self):
        """Generate and save a key"""
        self._key = Fernet.generate_key()
        with open('keyfile.key', 'wb') as key_file:
            key_file.write(self._key)

    def get_key(self):
        """Get the key"""
        return self._key

    def encrypt_file(self, filepath):
        """Encrypt the file using the stored key"""
        fernet_object = Fernet(self.get_key())
        with open(filepath, 'rb') as file:
            original_file = file.read()
        encrypted = fernet_object.encrypt(original_file)
        with open(filepath, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

    def decrypt_file(self, filepath):
        """Decrypt the file using the stored key"""
        fernet_object = Fernet(self.get_key())
        with open(filepath, 'rb') as encrypted_file:
            file_2_decrypt = encrypted_file.read()
        decrypt_file = fernet_object.decrypt(file_2_decrypt)
        with open(filepath, 'wb') as decrypted_file:
            decrypted_file.write(decrypt_file)


# class CryptoHandler:
#         """This class will handle the genrating of the key necessary to encrypt/decrypt files.
#         It has methods for getting access to the key and separte methods for encryption/decryption"""
#         def __init__(self):
#             """No data members for the init method because the object for this class is easier to handle
#             without parameters passed to it when the Application class creates the object for CryptoHandler"""
#             # self variables initialized to None for get methods to return actual key/key_file values
#             self._key = None 
#             self.key_file = None

#         def get_key(self):
#             """This method returns they fernet key and can now be accessed by other methods"""
#             self._key = Fernet.generate_key()
#             return self._key
        
#         def get_key_file(self):
#             """This method returns the file of the key"""
#             with open('keyfile.key', 'wb') as self.key_file:
#                 self.key_file.write(self.get_key())
            
#             with open('keyfile.key', 'rb') as self.key_file:
#                 self.key_file = self.key_file.read()
#             return self.key_file

        
#         def encrypt_file(self, filepath):
#             """This method encrypts any file chosen by the user. The filepath member is passed a parameter that is received from the Application class.
#             """
#             fernet_object = Fernet(self.get_key()) # This line creates the Fernet object that is necessary to give this method access to the key.
            
#             # self.get_key_file() # Not necessary to call get_key_file method for encryption method to work
#             #print(self.get_key_file()) #Test print of the key file
#             #print(self.get_key) # Test print of the key
            
#             #file io is used to read the orginal file path to write to that file in the second with statement
#             with open(filepath, 'rb') as file: 
#                 original_file = file.read()
#             encrypted = fernet_object.encrypt(original_file)
#             with open(filepath, 'wb') as encrypted_file:
#                 encrypted_file.write(encrypted)


#         def decrypt_file(self, filepath):
#             fernet_object = Fernet(self.get_key())
#             print(fernet_object)
#             with open(filepath,'rb') as encrypted_file:
#                 file_2_decrypt = encrypted_file.read()
#             decrypt_file = fernet_object.decrypt(file_2_decrypt)
#             with open(filepath, 'wb') as decrypted_file:
#                 decrypted_file.write(decrypt_file)

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

class Application(BaseWindow):
    def __init__(self, root):
        super().__init__(root)
        self.file_explorer = FileExplorer(root)
        self.encryption_handler = CryptoHandler()

        self.encrypt_button = Button(root, text="Encrypt", command=self.handle_encryption)
        self.encrypt_button.grid(column=1, row=3)

        self.decrypt_button = Button(root, text="Decrypt", command=self.handle_decryption)
        self.decrypt_button.grid(column=1, row=5)

    def handle_encryption(self):
        selected_file = self.file_explorer.file_label.cget("text").replace("File Opened: ", "")
        if selected_file:
            self.encryption_handler.encrypt_file(selected_file)
    
    def handle_decryption(self):
        selected_file = self.file_explorer.file_label.cget("text").replace("File Opened: ", "")
        if selected_file:
            self.encryption_handler.decrypt_file(selected_file)

if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()
