from tkinter import *
from tkinter import filedialog

class BaseWindow:
    def __init__(self, root):
        self.root = root
        self.root.title('File Explorer')
        self.root.geometry("500x500")
        self.root.config(background="white")

class FileExplorer(BaseWindow):
    def __init__(self, root):
        super().__init__(root)
        self.label_file_explorer = Label(root, text="File Explorer using Tkinter", width=100, height=4, fg="blue")
        self.label_file_explorer.grid(column=1, row=1)

        self.button_explore = Button(root, text="Browse Files", command=self.browse_files)
        self.button_explore.grid(column=1, row=2)

    def browse_files(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                               filetypes=(("All files", "*.*"),))
        self.label_file_explorer.configure(text="File Opened: " + filename)
        # Pass the selected file to the EncryptionHandler for further processing

class EncryptionHandler:
    def encrypt_file(self, file_path):
        # Implement your encryption logic here
        print(f"Encrypting file: {file_path}")

        # For illustration, you might want to save the encrypted file

class Application(BaseWindow):
    def __init__(self, root):
        super().__init__(root)
        self.file_explorer = FileExplorer(root)
        self.encryption_handler = EncryptionHandler()

        self.encrypt_button = Button(root, text="Encrypt", command=self.handle_encryption)
        self.encrypt_button.grid(column=1, row=3)

    def handle_encryption(self):
        selected_file = self.file_explorer.label_file_explorer.cget("text").replace("File Opened: ", "")
        if selected_file:
            self.encryption_handler.encrypt_file(selected_file)

if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()
