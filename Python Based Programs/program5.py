#

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="prog5_db"
    )

def execute_query(query):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query)
    if query.strip().lower().startswith("select"):
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results
    else:
        connection.commit()
        cursor.close()
        connection.close()
        return None

class QuantumQueryQuencher:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Query Quencher")
        self.create_widgets()

    def create_widgets(self):
        self.query_text = tk.Text(self.root, height=10)
        self.query_text.pack(fill=tk.BOTH, expand=True)

        self.execute_button = tk.Button(self.root, text="Execute Query", command=self.execute_query)
        self.execute_button.pack(pady=10)

        self.results_tree = ttk.Treeview(self.root, show="headings")
        self.results_tree.pack(fill=tk.BOTH, expand=True)

    def execute_query(self):
        query = self.query_text.get("1.0", tk.END).strip()
        if query:
            try:
                results = execute_query(query)
                if results is not None:
                    self.display_results(results)
                    messagebox.showinfo("Success", "Query executed successfully!")
                else:
                    messagebox.showinfo("Success", "Query executed successfully (no results to display).")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to execute query: {e}")

    def display_results(self, results):
        for col in self.results_tree.get_children():
            self.results_tree.delete(col)

        if results:
            columns = [desc[0] for desc in results[0]]
            self.results_tree["columns"] = columns
            for col in columns:
                self.results_tree.heading(col, text=col)
                self.results_tree.column(col, anchor=tk.W, width=100)

            for row in results:
                self.results_tree.insert("", tk.END, values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuantumQueryQuencher(root)
    root.mainloop()
