#“Chronos Code Repository”    : Create a version control system for source code with a Tkinter front-end, 
# using file handling to track changes and MySQL for metadata.

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import mysql.connector
import hashlib
import os
import datetime

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="prog6_db"
    )

def init_db():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE files (
            id INT AUTO_INCREMENT PRIMARY KEY,
            filename VARCHAR(255),
            version INT,
            hash VARCHAR(64),
            timestamp DATETIME,
            content LONGBLOB
        )
    ''')
    connection.commit()
    cursor.close()
    connection.close()

# Get the hash of a file's content
def get_file_hash(content):
    return hashlib.sha256(content).hexdigest()

# Save a file version to the database
def save_file_version(filename, content):
    connection = connect_to_db()
    cursor = connection.cursor()
    file_hash = get_file_hash(content)
    cursor.execute('''
        SELECT version FROM files WHERE filename = %s ORDER BY version DESC LIMIT 1
    ''', (filename,))
    row = cursor.fetchone()
    version = 1 if row is None else row[0] + 1
    timestamp = datetime.datetime.now()
    cursor.execute('''
        INSERT INTO files (filename, version, hash, timestamp, content)
        VALUES (%s, %s, %s, %s, %s)
    ''', (filename, version, file_hash, timestamp, content))
    connection.commit()
    cursor.close()
    connection.close()

# Fetch all versions of a file
def fetch_file_versions(filename):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT version, hash, timestamp FROM files WHERE filename = %s ORDER BY version DESC
    ''', (filename,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

# Fetch a specific version of a file
def fetch_file_version(filename, version):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT content FROM files WHERE filename = %s AND version = %s
    ''', (filename, version))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[0] if result else None

class ChronosCodeRepository:
    def __init__(self, root):
        self.root = root
        self.root.title("Chronos Code Repository")
        self.create_widgets()

    def create_widgets(self):
        self.file_label = tk.Label(self.root, text="File:")
        self.file_label.pack(pady=5)

        self.file_entry = tk.Entry(self.root, width=50)
        self.file_entry.pack(pady=5)

        self.browse_button = tk.Button(self.root, text="Browse", command=self.browse_file)
        self.browse_button.pack(pady=5)

        self.save_button = tk.Button(self.root, text="Save Version", command=self.save_version)
        self.save_button.pack(pady=5)

        self.version_label = tk.Label(self.root, text="Versions:")
        self.version_label.pack(pady=5)

        self.versions_listbox = tk.Listbox(self.root, height=10, width=50)
        self.versions_listbox.pack(pady=5)

        self.load_button = tk.Button(self.root, text="Load Version", command=self.load_version)
        self.load_button.pack(pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
            self.load_versions(file_path)

    def save_version(self):
        file_path = self.file_entry.get()
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    content = file.read()
                save_file_version(file_path, content)
                self.load_versions(file_path)
                messagebox.showinfo("Success", "File version saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file version: {e}")

    def load_versions(self, filename):
        self.versions_listbox.delete(0, tk.END)
        versions = fetch_file_versions(filename)
        for version in versions:
            version_info = f"Version {version[0]} - {version[1]} - {version[2]}"
            self.versions_listbox.insert(tk.END, version_info)

    def load_version(self):
        file_path = self.file_entry.get()
        selected_index = self.versions_listbox.curselection()
        if file_path and selected_index:
            version_info = self.versions_listbox.get(selected_index[0])
            version_number = int(version_info.split()[1])
            content = fetch_file_version(file_path, version_number)
            if content:
                save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
                if save_path:
                    with open(save_path, 'wb') as file:
                        file.write(content)
                    messagebox.showinfo("Success", "File version loaded successfully!")
            else:
                messagebox.showerror("Error", "Failed to load file version.")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = ChronosCodeRepository(root)
    root.mainloop()
