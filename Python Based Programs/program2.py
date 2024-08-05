# “Mystic Library Ledger”: Create an interactive library management system with Tkinter for borrowing and # returning books, with data persistence in a 
# MySQL database.

import tkinter as tk
from tkinter import ttk
import mysql.connector

def connect_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="program2_db"
    )
    return connection

def fetch_all_books():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books")
    results = cursor.fetchall()
    connection.close()
    return results

def borrow_book(book_id, borrower):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("UPDATE books SET borrowed_by=%s WHERE id=%s", (borrower, book_id))
    connection.commit()
    connection.close()

def return_book(book_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("UPDATE books SET borrowed_by=NULL WHERE id=%s", (book_id,))
    connection.commit()
    connection.close()

class MysticLibraryLedger:
    def __init__(self, root):
        self.root = root
        self.root.title("Mystic Library Ledger")
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.root, columns=("ID", "Title", "Author", "Borrowed By"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Borrowed By", text="Borrowed By")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.load_data_button = tk.Button(self.root, text="Load Books", command=self.load_data)
        self.load_data_button.pack()

        self.book_id_entry = tk.Entry(self.root)
        self.book_id_entry.pack()
        self.borrower_entry = tk.Entry(self.root)
        self.borrower_entry.pack()

        self.borrow_book_button = tk.Button(self.root, text="Borrow Book", command=self.borrow_book)
        self.borrow_book_button.pack()

        self.return_book_button = tk.Button(self.root, text="Return Book", command=self.return_book)
        self.return_book_button.pack()

    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        for row in fetch_all_books():
            self.tree.insert("", tk.END, values=row)

    def borrow_book(self):
        book_id = int(self.book_id_entry.get())
        borrower = self.borrower_entry.get()
        borrow_book(book_id, borrower)
        self.load_data()

    def return_book(self):
        book_id = int(self.book_id_entry.get())
        return_book(book_id)
        self.load_data()

if __name__ == "__main__":
    root = tk.Tk()
    app = MysticLibraryLedger(root)
    root.mainloop()
