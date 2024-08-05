# “Glimmer Grid Generator”    : Create a Tkinter tool to design and manage grid layouts for data visualization, 
#  with configurations saved in a MySQL database.

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="prog9_db"
    )
    
def init_db():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE grids (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            rows INT,
            columns INT,
            configuration TEXT
        )
    ''')
    connection.commit()
    cursor.close()
    connection.close()

def save_grid(name, rows, columns, configuration):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO grids (name, rows, columns, configuration)
        VALUES (%s, %s, %s, %s)
    ''', (name, rows, columns, configuration))
    connection.commit()
    cursor.close()
    connection.close()

# Fetch all grid layouts from the database
def fetch_grids():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id, name, rows, columns, configuration FROM grids
    ''')
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results


class GlimmerGridGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Glimmer Grid Generator")
        self.create_widgets()

    def create_widgets(self):
        # Form fields
        self.name_label = tk.Label(self.root, text="Grid Name:")
        self.name_label.pack(pady=5)
        self.name_entry = tk.Entry(self.root, width=50)
        self.name_entry.pack(pady=5)

        self.rows_label = tk.Label(self.root, text="Rows:")
        self.rows_label.pack(pady=5)
        self.rows_entry = tk.Entry(self.root, width=50)
        self.rows_entry.pack(pady=5)

        self.columns_label = tk.Label(self.root, text="Columns:")
        self.columns_label.pack(pady=5)
        self.columns_entry = tk.Entry(self.root, width=50)
        self.columns_entry.pack(pady=5)

        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(pady=10)

        self.generate_button = tk.Button(self.root, text="Generate Grid", command=self.generate_grid)
        self.generate_button.pack(pady=10)

        self.save_button = tk.Button(self.root, text="Save Grid Layout", command=self.save_grid)
        self.save_button.pack(pady=10)

        # Grid list
        self.grids_tree = ttk.Treeview(self.root, columns=("ID", "Name", "Rows", "Columns", "Configuration"), show="headings")
        self.grids_tree.heading("ID", text="ID")
        self.grids_tree.heading("Name", text="Name")
        self.grids_tree.heading("Rows", text="Rows")
        self.grids_tree.heading("Columns", text="Columns")
        self.grids_tree.heading("Configuration", text="Configuration")
        self.grids_tree.pack(fill=tk.BOTH, expand=True)

        # Load grids
        self.load_grids()

    def generate_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        rows = int(self.rows_entry.get())
        columns = int(self.columns_entry.get())
        self.grid_widgets = []
        for r in range(rows):
            row_widgets = []
            for c in range(columns):
                entry = tk.Entry(self.grid_frame, width=10)
                entry.grid(row=r, column=c, padx=5, pady=5)
                row_widgets.append(entry)
            self.grid_widgets.append(row_widgets)

    def save_grid(self):
        name = self.name_entry.get()
        rows = int(self.rows_entry.get())
        columns = int(self.columns_entry.get())
        configuration = []
        for row in self.grid_widgets:
            row_data = [widget.get() for widget in row]
            configuration.append(row_data)
        configuration_str = str(configuration)
        if name and rows and columns:
            try:
                save_grid(name, rows, columns, configuration_str)
                self.load_grids()
                messagebox.showinfo("Success", "Grid layout saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save grid layout: {e}")
        else:
            messagebox.showwarning("Input Error", "All fields are required!")

    def load_grids(self):
        grids = fetch_grids()
        for row in self.grids_tree.get_children():
            self.grids_tree.delete(row)
        for grid in grids:
            self.grids_tree.insert("", tk.END, values=grid)

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = GlimmerGridGenerator(root)
    root.mainloop()
