# “Enigma File Vault: Design a secure file encryption and decryption tool with a Tkinter interface, 
# using Python’s file handling capabilities.

import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet

# Encryption --------------------------------------------------------------------
# Generate and save the key
def generate_key():
    key = Fernet.generate_key()
    with open("program3secret.key", "wb") as key_file:
        key_file.write(key)
    return key

# Load the key from the file
def load_key():
    return open("secret.key", "rb").read()

# Encrypt a file
def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        file_data = file.read()
    encrypted_data = fernet.encrypt(file_data)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)

#Decryption ----------------------------------------------------------
# Decrypt a file
def decrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(file_path, "wb") as file:
        file.write(decrypted_data)

class EnigmaFileVault:
    def __init__(self, root):
        self.root = root
        self.root.title("Enigma File Vault")
        
        self.key = load_key() if self.key_exists() else generate_key()
        
        self.create_widgets()

    def create_widgets(self):
        self.encrypt_button = tk.Button(self.root, text="Encrypt File", command=self.encrypt_file)
        self.encrypt_button.pack(pady=10)

        self.decrypt_button = tk.Button(self.root, text="Decrypt File", command=self.decrypt_file)
        self.decrypt_button.pack(pady=10)

    def key_exists(self):
        try:
            with open("secret.key", "rb"):
                return True
        except FileNotFoundError:
            return False

    def encrypt_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                encrypt_file(file_path, self.key)
                messagebox.showinfo("Success", "File encrypted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to encrypt file: {e}")

    def decrypt_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                decrypt_file(file_path, self.key)
                messagebox.showinfo("Success", "File decrypted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to decrypt file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EnigmaFileVault(root)
    root.mainloop()
