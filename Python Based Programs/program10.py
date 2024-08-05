# “Seraphim Surveyor”    : Design a survey application with a Tkinter GUI for collecting responses and storing 
# them in a MySQL database, with options for file-based backup and retrieval.

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
import json
import os

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="prog10_db"
    )

def init_db():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE responses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            feedback TEXT
        )
    ''')
    connection.commit()
    cursor.close()
    connection.close()

# Save response to the database
def save_response(name, email, feedback):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO responses (name, email, feedback)
        VALUES (%s, %s, %s)
    ''', (name, email, feedback))
    connection.commit()
    cursor.close()
    connection.close()

# Fetch all responses from the database
def fetch_responses():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id, name, email, feedback FROM responses
    ''')
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

# Backup responses to a file
def backup_responses(filename):
    responses = fetch_responses()
    with open(filename, 'w') as file:
        json.dump(responses, file)
    messagebox.showinfo("Backup", "Responses backed up successfully!")

# Load responses from a file
def load_responses(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            responses = json.load(file)
        connection = connect_db()
        cursor = connection.cursor()
        for response in responses:
            cursor.execute('''
                INSERT INTO responses (id, name, email, feedback)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                name = VALUES(name), email = VALUES(email), feedback = VALUES(feedback)
            ''', response)
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Load", "Responses loaded successfully!")
    else:
        messagebox.showerror("Error", "Backup file not found!")

class SeraphimSurveyor:
    def __init__(self, root):
        self.root = root
        self.root.title("Seraphim Surveyor")
        self.create_widgets()

    def create_widgets(self):
        self.name_label = tk.Label(self.root, text="Name:")
        self.name_label.pack(pady=5)
        self.name_entry = tk.Entry(self.root, width=50)
        self.name_entry.pack(pady=5)

        self.email_label = tk.Label(self.root, text="Email:")
        self.email_label.pack(pady=5)
        self.email_entry = tk.Entry(self.root, width=50)
        self.email_entry.pack(pady=5)

        self.feedback_label = tk.Label(self.root, text="Feedback:")
        self.feedback_label.pack(pady=5)
        self.feedback_text = tk.Text(self.root, width=50, height=10)
        self.feedback_text.pack(pady=5)

        self.save_button = tk.Button(self.root, text="Submit Response", command=self.save_response)
        self.save_button.pack(pady=10)

        self.backup_button = tk.Button(self.root, text="Backup Responses", command=self.backup_responses)
        self.backup_button.pack(pady=10)

        self.load_button = tk.Button(self.root, text="Load Responses", command=self.load_responses)
        self.load_button.pack(pady=10)

        self.responses_tree = ttk.Treeview(self.root, columns=("ID", "Name", "Email", "Feedback"), show="headings")
        self.responses_tree.heading("ID", text="ID")
        self.responses_tree.heading("Name", text="Name")
        self.responses_tree.heading("Email", text="Email")
        self.responses_tree.heading("Feedback", text="Feedback")
        self.responses_tree.pack(fill=tk.BOTH, expand=True)

        self.load_responses_from_db()

    def save_response(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        feedback = self.feedback_text.get("1.0", tk.END).strip()
        if name and email and feedback:
            try:
                save_response(name, email, feedback)
                self.load_responses_from_db()
                messagebox.showinfo("Success", "Response submitted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to submit response: {e}")
        else:
            messagebox.showwarning("Input Error", "All fields are required!")

    def backup_responses(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            backup_responses(filename)

    def load_responses(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            load_responses(filename)
            self.load_responses_from_db()

    def load_responses_from_db(self):
        responses = fetch_responses()
        for row in self.responses_tree.get_children():
            self.responses_tree.delete(row)
        for response in responses:
            self.responses_tree.insert("", tk.END, values=response)

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = SeraphimSurveyor(root)
    root.mainloop()
