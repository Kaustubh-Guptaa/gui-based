# Celestial Dashboard: A dashboard that interact with the database and contains information about stars or planets

import tkinter as tk
from tkinter import ttk
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def connect_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="prog1_db"
    )
    return connection

def fetch_data():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM celestial_data")
    results = cursor.fetchall()
    connection.close()
    return results

def insert_data(name, type, distance, magnitude):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO celestial_data (name, type, distance, magnitude) VALUES (%s, %s, %s, %s)", (name, type, distance, magnitude))
    connection.commit()
    connection.close()

class CelestialDataDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Celestial Data Dashboard")

        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Type", "Distance", "Magnitude"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Distance", text="Distance")
        self.tree.heading("Magnitude", text="Magnitude")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.load_data_button = tk.Button(self.root, text="Load Data", command=self.load_data)
        self.load_data_button.pack()

        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()
        self.type_entry = tk.Entry(self.root)
        self.type_entry.pack()
        self.distance_entry = tk.Entry(self.root)
        self.distance_entry.pack()
        self.magnitude_entry = tk.Entry(self.root)
        self.magnitude_entry.pack()

        self.add_data_button = tk.Button(self.root, text="Add Data", command=self.add_data)
        self.add_data_button.pack()

        self.plot_button = tk.Button(self.root, text="Plot Data", command=self.plot_data)
        self.plot_button.pack()

    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        for row in fetch_data():
            self.tree.insert("", tk.END, values=row)

    def add_data(self):
        name = self.name_entry.get()
        type = self.type_entry.get()
        distance = float(self.distance_entry.get())
        magnitude = float(self.magnitude_entry.get())
        insert_data(name, type, distance, magnitude)
        self.load_data()

    def plot_data(self):
        data = fetch_data()
        distances = [row[3] for row in data]
        magnitudes = [row[4] for row in data]

        fig, ax = plt.subplots()
        ax.scatter(distances, magnitudes)
        ax.set_xlabel('Distance')
        ax.set_ylabel('Magnitude')
        ax.set_title('Distance vs Magnitude')

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.get_tk_widget().pack()
        canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = CelestialDataDashboard(root)
    root.mainloop()
