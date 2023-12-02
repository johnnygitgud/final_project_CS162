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
        # Pass the selected file to the EncryptionHandler for further processing

class EncryptionHandler:
    def encrypt_file(self, file_path):
        """Fernet key encryption generates a key"""
        key = Fernet.generate_key()
        #using file_io to write key to file
        with open('filekey.key', 'wb') as filekey:
            filekey.write(key)
        # opening the key
        with open('filekey.key', 'rb') as filekey:
            key = filekey.read()

        # using the generated key
        fernet = Fernet(key)

        # opening the original file to encrypt
        with open(file_path, 'rb') as file:
            original = file.read()
            
        # encrypting the file
        encrypted = fernet.encrypt(original)

        # opening the file in write mode and 
        # writing the encrypted data
        with open(file_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

        print(f"Encrypting file: {file_path}")

        # For illustration, you might want to save the encrypted file

class DecryptionHandler:
    pass

class Application(BaseWindow):
    def __init__(self, root):
        super().__init__(root)
        self.file_explorer = FileExplorer(root)
        self.encryption_handler = EncryptionHandler()

        self.encrypt_button = Button(root, text="Encrypt", command=self.handle_encryption)
        self.encrypt_button.grid(column=1, row=3)

    def handle_encryption(self):
        selected_file = self.file_explorer.file_label.cget("text").replace("File Opened: ", "")
        if selected_file:
            self.encryption_handler.encrypt_file(selected_file)

if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()
