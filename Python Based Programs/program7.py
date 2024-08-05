# “Phantom File Finder”    : Build a Tkinter-based file management system that helps users locate and organize files, 
# with metadata stored in a MySQL database.

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import mysql.connector
import hashlib

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="prog7_db"
    )

def init_db():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE files (
            id INT AUTO_INCREMENT PRIMARY KEY,
            path VARCHAR(255),
            name VARCHAR(255),
            size BIGINT,
            hash VARCHAR(64),
            category VARCHAR(255)
        )
    ''')
    connection.commit()
    cursor.close()
    connection.close()

# Get the hash of a file's content
def get_file_hash(file_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()
    return hashlib.sha256(file_data).hexdigest()

# Save file metadata to the database
def save_file_metadata(file_path, category):
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    file_hash = get_file_hash(file_path)
    
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO files (path, name, size, hash, category)
        VALUES (%s, %s, %s, %s, %s)
    ''', (file_path, file_name, file_size, file_hash, category))
    connection.commit()
    cursor.close()
    connection.close()

# Fetch files based on category
def fetch_files_by_category(category):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT path, name, size, hash FROM files WHERE category = %s
    ''', (category,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

class PhantomFileFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("Phantom File Finder")
        self.create_widgets()

    def create_widgets(self):
        self.path_label = tk.Label(self.root, text="File Path:")
        self.path_label.pack(pady=5)

        self.path_entry = tk.Entry(self.root, width=50)
        self.path_entry.pack(pady=5)

        self.browse_button = tk.Button(self.root, text="Browse", command=self.browse_file)
        self.browse_button.pack(pady=5)

        self.category_label = tk.Label(self.root, text="Category:")
        self.category_label.pack(pady=5)

        self.category_entry = tk.Entry(self.root, width=50)
        self.category_entry.pack(pady=5)

        self.save_button = tk.Button(self.root, text="Save Metadata", command=self.save_metadata)
        self.save_button.pack(pady=5)

        self.search_label = tk.Label(self.root, text="Search by Category:")
        self.search_label.pack(pady=5)

        self.search_entry = tk.Entry(self.root, width=50)
        self.search_entry.pack(pady=5)

        self.search_button = tk.Button(self.root, text="Search", command=self.search_files)
        self.search_button.pack(pady=5)

        self.results_tree = ttk.Treeview(self.root, columns=("Path", "Name", "Size", "Hash"), show="headings")
        self.results_tree.heading("Path", text="Path")
        self.results_tree.heading("Name", text="Name")
        self.results_tree.heading("Size", text="Size")
        self.results_tree.heading("Hash", text="Hash")
        self.results_tree.pack(fill=tk.BOTH, expand=True)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, file_path)

    def save_metadata(self):
        file_path = self.path_entry.get()
        category = self.category_entry.get()
        if file_path and category:
            try:
                save_file_metadata(file_path, category)
                messagebox.showinfo("Success", "File metadata saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file metadata: {e}")

    def search_files(self):
        category = self.search_entry.get()
        if category:
            try:
                results = fetch_files_by_category(category)
                self.display_results(results)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to fetch files: {e}")

    def display_results(self, results):
        for row in self.results_tree.get_children():
            self.results_tree.delete(row)
        for row in results:
            self.results_tree.insert("", tk.END, values=row)

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = PhantomFileFinder(root)
    root.mainloop()
