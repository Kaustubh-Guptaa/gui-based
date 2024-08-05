# Aether Address Atlas”    : Develop a contact management application with a Tkinter interface, integrating MySQL
# for storing and retrieving contact information.

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="prog8_db"
    )

def init_db():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE contacts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            email VARCHAR(255),
            phone VARCHAR(255)
        )
    ''')
    connection.commit()
    cursor.close()
    connection.close()

# Save contact to the database
def save_contact(first_name, last_name, email, phone):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO contacts (first_name, last_name, email, phone)
        VALUES (%s, %s, %s, %s)
    ''', (first_name, last_name, email, phone))
    connection.commit()
    cursor.close()
    connection.close()

# Fetch all contacts from the database
def fetch_contacts():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id, first_name, last_name, email, phone FROM contacts
    ''')
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

class AetherAddressAtlas:
    def __init__(self, root):
        self.root = root
        self.root.title("Aether Address Atlas")
        self.create_widgets()

    def create_widgets(self):
        # Form fields
        self.first_name_label = tk.Label(self.root, text="First Name:")
        self.first_name_label.pack(pady=5)
        self.first_name_entry = tk.Entry(self.root, width=50)
        self.first_name_entry.pack(pady=5)

        self.last_name_label = tk.Label(self.root, text="Last Name:")
        self.last_name_label.pack(pady=5)
        self.last_name_entry = tk.Entry(self.root, width=50)
        self.last_name_entry.pack(pady=5)

        self.email_label = tk.Label(self.root, text="Email:")
        self.email_label.pack(pady=5)
        self.email_entry = tk.Entry(self.root, width=50)
        self.email_entry.pack(pady=5)

        self.phone_label = tk.Label(self.root, text="Phone:")
        self.phone_label.pack(pady=5)
        self.phone_entry = tk.Entry(self.root, width=50)
        self.phone_entry.pack(pady=5)

        # Save button
        self.save_button = tk.Button(self.root, text="Save Contact", command=self.save_contact)
        self.save_button.pack(pady=10)

        # Contact list
        self.contacts_tree = ttk.Treeview(self.root, columns=("ID", "First Name", "Last Name", "Email", "Phone"), show="headings")
        self.contacts_tree.heading("ID", text="ID")
        self.contacts_tree.heading("First Name", text="First Name")
        self.contacts_tree.heading("Last Name", text="Last Name")
        self.contacts_tree.heading("Email", text="Email")
        self.contacts_tree.heading("Phone", text="Phone")
        self.contacts_tree.pack(fill=tk.BOTH, expand=True)

        # Load contacts
        self.load_contacts()

    def save_contact(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        if first_name and last_name and email and phone:
            try:
                save_contact(first_name, last_name, email, phone)
                self.load_contacts()
                messagebox.showinfo("Success", "Contact saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save contact: {e}")
        else:
            messagebox.showwarning("Input Error", "All fields are required!")

    def load_contacts(self):
        contacts = fetch_contacts()
        for row in self.contacts_tree.get_children():
            self.contacts_tree.delete(row)
        for contact in contacts:
            self.contacts_tree.insert("", tk.END, values=contact)

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = AetherAddressAtlas(root)
    root.mainloop()
