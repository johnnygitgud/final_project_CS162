# tkinter is for the GUI modules. File dialogue gives me access to file explorer
# cryptography.fernet gives me accesss to a crypto class so we can encrypt and decrypt a chosen file
# Sample code from https://www.geeksforgeeks.org/encrypt-and-decrypt-files-using-python/ was used to createthe encryption and decryption code
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
    """This class with handle all the crypto taks including:
    generating key, creating key file, encrypting and decrypting a file chose by the user."""
    def __init__(self):
        """init method sets data members for key, key file, and genrating_().
        They are set to none so that other getter methods can have access and assign new values.\
            generate.key() is in the init because we only need one key generated at a time.
            THIS FIXES THE 'bug' WHERE MULTIPE KEY OBJECTS WERE GENERATED THAT CRASHED DECRYPTION BECAUSE KEYS DIDN'T MATCH"""
        self._key = None
        self.key_file = None
        self.generate_key()

    def generate_key(self):
        """Generate and save a key"""
        # This the basic syntax for creating the key
        self._key = Fernet.generate_key() #This calls to line 45 only once at a time preventing multiple key objects
        
        #file io writes the key to a new file.
        with open('keyfile.key', 'wb') as key_file:
            key_file.write(self._key)

    def get_key(self):
        """Getter method for the key"""
        return self._key

    def encrypt_file(self, filepath):
        """Encrypt the file using the stored key and filepath data member passed file destination chosen by user.
        First File explorer class gives the filepath to the label. Application class creates FileExplorer object.
        Application has method for calling to encrypt_file and passing the file path
        May need potential warning for users since original file chosen will not be preserved not until it is decrypted. Potential loss of data"""
        #create the fernet object and store it in the variable fernet_object which will be used for encryption later.
        fernet_object = Fernet(self.get_key())
        
        #file io for reading contents of chosen file
        with open(filepath, 'rb') as file:
            original_file = file.read()
        
        #syntax for fernet encryption; the object has the key. This encrypts the argument that is passed to encrypt() which is the file that was chosen 
        encrypted = fernet_object.encrypt(original_file)

        #file io is used to write the encrypted file. The orginal file becomes encrypted and overwritten.
        with open(filepath, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

    def decrypt_file(self, filepath):
        """Decrypt the file using the stored key"""
        #create the fernet object and store it in the variable fernet_object which will be used for decryption later.
        fernet_object = Fernet(self.get_key())

        #file_io will ready the contents of the file path chosen by user and assign it to a variable to be used later for decryption
        with open(filepath, 'rb') as encrypted_file:
            file_2_decrypt = encrypted_file.read()

        #syntax for fernet decryption; the object has the key. This decrypts the argument that is passed to encrypt() which is the file that was chosen 
        decrypt_file = fernet_object.decrypt(file_2_decrypt)

        #file io is used to rewrite the encrypted file and decrypt it. The orginal file will have the original contents restored
        # the variable decrypt_file is passed as an argument to do clear the jargon.
        with open(filepath, 'wb') as decrypted_file:
            decrypted_file.write(decrypt_file)

class Application(BaseWindow):
    """This class has inherited the BaseWindow class and has access to the roots necessary for tk.
    This class will also create objects needed for generating the tk window, enabling file explorer,
     enabling the cryptography, and creating the buttons for encrypt/decrypt and their method calls/commands."""
    def __init__(self, root):
        super().__init__(root)
        """super is used to get access to inerited object"""
        #object for FileExplorer class
        self.file_explorer = FileExplorer(root)
        
        #object for CryptoHandler class
        self.encryption_handler = CryptoHandler()

        # create encrypt button
        self.encrypt_button = Button(root, text="Encrypt", command=self.handle_encryption)
        self.encrypt_button.grid(column=1, row=3)

        #create decrypt button
        self.decrypt_button = Button(root, text="Decrypt", command=self.handle_decryption)
        self.decrypt_button.grid(column=1, row=5)

    def handle_encryption(self):
        """This method updates the label to show the chosen file path and calls the encrypt_file method from CryptoHandler
        and passes the file the user chose."""
        selected_file = self.file_explorer.file_label.cget("text").replace("File Opened: ", "")
        if selected_file:
            self.encryption_handler.encrypt_file(selected_file)
    
    def handle_decryption(self):
        """This method updates the label to show the chosen file path and calls the decrypt_file method from CryptoHandler
        and passes the file the user chose."""
        selected_file = self.file_explorer.file_label.cget("text").replace("File Opened: ", "")
        if selected_file:
            self.encryption_handler.decrypt_file(selected_file)

# script for referencing the code above and running it.
# Tk, Application objects are created and mainloop is ran to generate the GUI
if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()
