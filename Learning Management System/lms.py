# Learning Management System

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="lms_db"
)

class LMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Learning Management System [LMS]")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        self.create_frames()

    def create_frames(self):        
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(pady=20)

        self.middle_frame = tk.Frame(self.root)
        self.middle_frame.pack(pady=10)

        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(pady=10)

        self.app_title()
        self.add_data()
        self.view_data()

    def app_title(self):
        tk.Label(self.top_frame, text="Learning Management System", font=("Times New Roman", 20, 'bold')).pack()

    def add_data(self):
        tk.Button(self.middle_frame, text="Add Course", command=self.add_course).grid(row=0, column=0, padx=15)
        tk.Button(self.middle_frame, text="Add Student", command=self.add_student).grid(row=0, column=1, padx=15)
        tk.Button(self.middle_frame, text="Add Instructor", command=self.add_instructor).grid(row=0, column=2, padx=15)
        tk.Button(self.middle_frame, text="Delete Record", command=self.delete_record).grid(row=0, column=3, padx=10)

    def view_data(self):
        tk.Button(self.bottom_frame, text="View Courses", command=self.view_courses).grid(row=0, column=0, padx=10)
        tk.Button(self.bottom_frame, text="View Students", command=self.view_students).grid(row=0, column=1, padx=10)
        tk.Button(self.bottom_frame, text="View Instructors", command=self.view_instructors).grid(row=0, column=2, padx=10)
  
    def input_student(self, title,  save_callback):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("300x300")
        tk.Label(popup, text="Student Name: ").pack(pady=10)
        std_name = tk.Entry(popup)
        std_name.pack(pady=10)
        tk.Label(popup, text="Enrollment Number: ").pack(pady=10)
        enroll = tk.Entry(popup)
        enroll.pack(pady=10)
        tk.Button(popup, text="Save", command=lambda: self.save_input([std_name.get(), enroll.get()], save_callback, popup)).pack(pady=10)
        
    def input_instructor(self, title,  save_callback):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("300x300")
        tk.Label(popup, text="Faculty Name: ").pack(pady=10)
        faculty_name = tk.Entry(popup)
        faculty_name.pack(pady=10)
        tk.Label(popup, text="Faculty ID: ").pack(pady=10)
        faculty_id = tk.Entry(popup)
        faculty_id.pack(pady=10)
        tk.Button(popup, text="Save", command=lambda: self.save_input([faculty_name.get(), faculty_id.get()], save_callback, popup)).pack(pady=10)
        
    def input_course(self, title,  save_callback):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("300x300")
        tk.Label(popup, text="Course Name: ").pack(pady=10)
        course_name = tk.Entry(popup)
        course_name.pack(pady=10)
        tk.Label(popup, text="Course ID: ").pack(pady=10)
        course_id = tk.Entry(popup)
        course_id.pack(pady=10)
        tk.Button(popup, text="Save", command=lambda: self.save_input([course_name.get(), course_id.get()], save_callback, popup)).pack(pady=10)
    
    def add_course(self):
        self.input_course("Add Course", self.save_course)

    def add_student(self):
        self.input_student("Add Student", self.save_student)

    def add_instructor(self):
        self.input_instructor("Add Instructor", self.save_instructor)


    def save_input(self, input_value, save_callback, popup):
        if input_value:
            save_callback(input_value)
            popup.destroy()
        else:
            messagebox.showerror("Input Error", "Input cannot be empty")

    def save_course(self, detail):
        cursor = db.cursor()
        cursor.execute("INSERT INTO courses (name, course_id) VALUES (%s,%s)", (detail[0], detail[1]))
        db.commit()
        cursor.close()
        messagebox.showinfo("Success", f"Course '{detail[0]}' added successfully")

    def save_student(self, detail):
        cursor = db.cursor()
        cursor.execute("INSERT INTO students (name, enrollment_no) VALUES (%s, %s)", (detail[0], detail[1]))
        db.commit()
        cursor.close()
        messagebox.showinfo("Success", f"Student '{detail[0]}' added successfully")

    def save_instructor(self, detail):
        cursor = db.cursor()
        cursor.execute("INSERT INTO instructors (name, faculty_id) VALUES (%s, %s)", (detail[0], detail[1]))
        db.commit()
        cursor.close()
        messagebox.showinfo("Success", f"Instructor '{detail[0]}' added successfully")

    def view_courses(self):
        self.create_view_popup("Courses", "SELECT * FROM courses")

    def view_students(self):
        self.create_view_popup("Students", "SELECT * FROM students")

    def view_instructors(self):
        self.create_view_popup("Instructors", "SELECT * FROM instructors")

    def create_view_popup(self, title, query):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("500x300")

        cursor = db.cursor()
        cursor.execute(query)
        items = cursor.fetchall()
        cursor.close()
        
        tk.Label(popup, text=f"#", font=('Times New Roman', 14, 'underline' )).grid(row=0, column=0, padx=15)
        tk.Label(popup, text=f"ID", font=('Times New Roman', 14, 'bold', 'underline' )).grid(row=0, column=1, padx=15)
        
        for i, item in enumerate(items):
            tk.Label(popup, text=f"{item[0]}", font=('Times New Roman',)).grid(row=i+1, column=0, padx=15)
            tk.Label(popup, text=f"{item[1]}", font=('Times New Roman', 14, 'bold' )).grid(row=i+1, column=1, padx=15)
            tk.Label(popup, text=f"{item[2]}", font=('Times New Roman', 14, 'italic')).grid(row=i+1, column=2, padx=15)
            
    def input_delete(self, save_callback):
        popup = tk.Toplevel(self.root)
        popup.title("Delete Record")
        popup.geometry("300x300")

        tk.Label(popup, text="From table? (courses/students/instructors):").pack(pady=10)
        table_name = tk.Entry(popup)
        table_name.pack(pady=10)
        
        tk.Label(popup, text="id").pack(pady=10)
        id = tk.Entry(popup)
        id.pack(pady=10)
        tk.Button(popup, text="Delete", command=lambda: self.save_input([table_name.get(), id.get()], save_callback, popup)).pack(pady=10)
    
    def delete_record(self):
        self.input_delete(self.delete_record_by_id)

    def delete_record_by_id(self, detail):
        cursor = db.cursor()
        cursor.execute("DELETE FROM table_name = %s WHERE id = %s", (detail[0], detail[1]))
        db.commit()
        cursor.close()
        messagebox.showinfo("Success", f"Record with ID '{detail[1]}' deleted successfully")

if __name__ == "__main__":
    window = tk.Tk()
    app = LMS(window)
    window.mainloop()
