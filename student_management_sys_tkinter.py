
import customtkinter as ctk
import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox, ttk
import datetime


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class StudentManagementSystem:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Student Management System")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        
        self.subjects = ["Mathematics", "Physics", "Chemistry", "English", "Computer Science"]
        
       
        self.db_connection = None
        self.connect_to_database()
        self.create_tables()
        
       
        self.student_id_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.roll_no_var = tk.StringVar()
        self.dob_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()
        
        
        self.subject_vars = {}
        for subject in self.subjects:
            self.subject_vars[subject] = tk.StringVar()
        
        self.setup_ui()
        self.load_students()
        
    def connect_to_database(self):
        """Connect to MySQL database"""
        try:
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  
                database="student_management"
            )
            if self.db_connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
           
            try:
                temp_connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password=""
                    
                )
                
                cursor = temp_connection.cursor()
                cursor.execute("CREATE DATABASE IF NOT EXISTS student_management")
                temp_connection.close()
                
               
                self.db_connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="student_management"
                )
                print("Created and connected to student_management database")
            except Error as e:
                print(f"Error creating database: {e}")
                messagebox.showerror("Database Error", "Could not connect to database. Please check MySQL installation.")
    
    def create_tables(self):
        """Create necessary tables if they don't exist"""
        if not self.db_connection:
            return
            
        cursor = self.db_connection.cursor()
        
        
        students_table = """
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            roll_no VARCHAR(20) UNIQUE NOT NULL,
            dob DATE,
            gender VARCHAR(10),
            phone VARCHAR(15),
            email VARCHAR(100),
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        
        subjects_table = """
        CREATE TABLE IF NOT EXISTS subjects (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL UNIQUE
        )
        """
        
        
        marks_table = """
        CREATE TABLE IF NOT EXISTS marks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            subject_id INT,
            marks DECIMAL(5,2),
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
            FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
        )
        """
        
        try:
            cursor.execute(students_table)
            cursor.execute(subjects_table)
            cursor.execute(marks_table)
            
           
            for subject in self.subjects:
                cursor.execute("INSERT IGNORE INTO subjects (name) VALUES (%s)", (subject,))
            
            self.db_connection.commit()
            print("Tables created successfully")
        except Error as e:
            print(f"Error creating tables: {e}")
    
    def setup_ui(self):
        """Setup the user interface"""
       
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        
        title_label = ctk.CTkLabel(main_frame, text="Student Management System", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=10)
        
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, padx=30, pady=10)

        
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=('Arial', 14, 'bold'),padding=[20,10])
        
       
        self.create_student_tab()
        self.create_view_tab()
        self.create_search_tab()
    
    def create_student_tab(self):
        """Create the student entry tab"""
        student_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(student_frame, text="Add/Edit Student")
        
       
        left_frame = ctk.CTkFrame(student_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        
        details_label = ctk.CTkLabel(left_frame, text="Student Details", 
                                   font=ctk.CTkFont(size=18, weight="bold"))
        details_label.pack(pady=10)
        
        # Student details form
        details_form = ctk.CTkFrame(left_frame)
        details_form.pack(fill="both", expand=True, padx=10, pady=10)
        
     
        fields = [
            ("Student ID:", self.student_id_var, "readonly"),
            ("Name:", self.name_var, "normal"),
            ("Roll No:", self.roll_no_var, "normal"),
            ("Date of Birth (YYYY-MM-DD):", self.dob_var, "normal"),
            ("Gender:", self.gender_var, "normal"),
            ("Phone:", self.phone_var, "normal"),
            ("Email:", self.email_var, "normal"),
            ("Address:", self.address_var, "normal")
        ]
        
        for i, (label, var, state) in enumerate(fields):
            row_frame = ctk.CTkFrame(details_form)
            row_frame.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(row_frame, text=label, width=150).pack(side="left", padx=5)
            if state == "readonly":
                ctk.CTkEntry(row_frame, textvariable=var, state="readonly").pack(side="left", fill="x", expand=True, padx=5)
            else:
                ctk.CTkEntry(row_frame, textvariable=var).pack(side="left", fill="x", expand=True, padx=5)
        
        # Right frame for marks
        right_frame = ctk.CTkFrame(student_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Marks section
        marks_label = ctk.CTkLabel(right_frame, text="Subject Marks", 
                                 font=ctk.CTkFont(size=18, weight="bold"))
        marks_label.pack(pady=10)
        
        marks_form = ctk.CTkFrame(right_frame)
        marks_form.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Subject marks fields
        for subject in self.subjects:
            row_frame = ctk.CTkFrame(marks_form)
            row_frame.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(row_frame, text=f"{subject}:", width=150).pack(side="left", padx=5)
            ctk.CTkEntry(row_frame, textvariable=self.subject_vars[subject]).pack(side="left", fill="x", expand=True, padx=5)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(student_frame)
        buttons_frame.pack(side="bottom", fill="y", padx=10, pady=10)
        
        
        ctk.CTkButton(buttons_frame, text="Add Student", command=self.add_student).pack(pady=40)
        ctk.CTkButton(buttons_frame, text="Update Student", command=self.update_student).pack(pady=40)
        ctk.CTkButton(buttons_frame, text="Clear Form", command=self.clear_form).pack(pady=40)
        ctk.CTkButton(buttons_frame, text="Delete Student", command=self.delete_student).pack(pady=40)
    
    def create_view_tab(self):
        """Create the view students tab"""
        view_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(view_frame, text="View Students")#adds view students tab
        
        # Treeview for displaying students
        tree_frame = ctk.CTkFrame(view_frame)#holds student list
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create Treeview
        columns = ("ID", "Name", "Roll No", "DOB", "Gender", "Phone", "Email")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Scrollbar to handle large record sets
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind double-click event
        self.tree.bind("<Double-1>", self.on_student_select)
        
        # Refresh button
        refresh_btn = ctk.CTkButton(view_frame, text="Refresh", command=self.load_students)
        refresh_btn.pack(pady=10)
    
    def create_search_tab(self):
        """Create the search tab"""
        search_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(search_frame, text="Search Students")
        
        # Search frame where we will input values to see
        search_input_frame = ctk.CTkFrame(search_frame)
        search_input_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(search_input_frame, text="Search by Name or Roll No:").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(search_input_frame, textvariable=self.search_var, width=300)
        search_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(search_input_frame, text="Search", command=self.search_students).pack(side="left", padx=5)
        ctk.CTkButton(search_input_frame, text="Clear", command=self.clear_search).pack(side="left", padx=5)
        
        # Results frame holds the searched results
        results_frame = ctk.CTkFrame(search_frame)
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Results treeview=spreedsheet type table,columns defines datafields,show="headings"->hides the default blank first column.
        columns = ("ID", "Name", "Roll No", "DOB", "Gender", "Phone", "Email", "Average Marks")
        self.search_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=30)

        # Configure style for larger font
        style = ttk.Style()
        style.configure("Treeview", font=('Arial', 12))
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
        
        for col in columns:
            self.search_tree.heading(col, text=col)
            self.search_tree.column(col, width=100)
        
        # Scrollbar for search results
        #Creates a vertical scrollbar linked to the table’s y-axis scrolling.
        #yscrollcommand ensures scrolling is synced between table and scrollbar.
        search_scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.search_tree.yview)
        self.search_tree.configure(yscrollcommand=search_scrollbar.set)
        
        self.search_tree.pack(side="left", fill="both", expand=True)
        search_scrollbar.pack(side="right", fill="y")
        
        '''When a user double-clicks a row, self.on_search_student_select() runs.

Typically, this would:

Get the student ID from the clicked row.

Load that student details into the Add/Edit Student form.

 '''
        self.search_tree.bind("<Double-1>", self.on_search_student_select)
    
    def add_student(self):
        """Add a new student to the database"""
        if not self.validate_form():
            return
        
        try:
            cursor = self.db_connection.cursor()#start database operation
            
            # Insert student
            student_query = """
            INSERT INTO students (name, roll_no, dob, gender, phone, email, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            student_data = (
                self.name_var.get(),
                self.roll_no_var.get(),
                self.dob_var.get(),
                self.gender_var.get(),
                self.phone_var.get(),
                self.email_var.get(),
                self.address_var.get()
            )
            
            cursor.execute(student_query, student_data)
            student_id = cursor.lastrowid
            
            # Insert marks
            for subject in self.subjects:
                marks = self.subject_vars[subject].get()
                if marks and marks.strip():
                    try:
                        marks_float = float(marks)
                        if 0 <= marks_float <= 100:
                            # Get subject ID
                            cursor.execute("SELECT id FROM subjects WHERE name = %s", (subject,))
                            subject_id = cursor.fetchone()[0]
                            
                            # Insert marks
                            marks_query = "INSERT INTO marks (student_id, subject_id, marks) VALUES (%s, %s, %s)"
                            cursor.execute(marks_query, (student_id, subject_id, marks_float))
                    except ValueError:
                        messagebox.showwarning("Invalid Marks", f"Invalid marks for {subject}. Please enter a number between 0-100.")
            
            self.db_connection.commit()
            messagebox.showinfo("Success", "Student added successfully!")
            self.clear_form()
            self.load_students()
            
        except Error as e:
            print(f"Error adding student: {e}")
            messagebox.showerror("Error", f"Error adding student: {e}")
    
    def update_student(self):
        """Update existing student details"""
        if not self.student_id_var.get():
            messagebox.showwarning("Warning", "Please select a student to update.")
            return
        
        if not self.validate_form():
            return
        
        try:
            cursor = self.db_connection.cursor()
            
            # Update student details
            update_query = """
            UPDATE students 
            SET name = %s, roll_no = %s, dob = %s, gender = %s, phone = %s, email = %s, address = %s
            WHERE id = %s
            """
            update_data = (
                self.name_var.get(),
                self.roll_no_var.get(),
                self.dob_var.get(),
                self.gender_var.get(),
                self.phone_var.get(),
                self.email_var.get(),
                self.address_var.get(),
                self.student_id_var.get()
            )
            
            cursor.execute(update_query, update_data)
            
            # Update marks
            for subject in self.subjects:
                marks = self.subject_vars[subject].get()
                if marks and marks.strip():
                    try:
                        marks_float = float(marks)
                        if 0 <= marks_float <= 100:
                            # Get subject ID
                            cursor.execute("SELECT id FROM subjects WHERE name = %s", (subject,))
                            subject_id = cursor.fetchone()[0]
                            
                            # Check if marks exist
                            cursor.execute("SELECT id FROM marks WHERE student_id = %s AND subject_id = %s", 
                                         (self.student_id_var.get(), subject_id))
                            existing_mark = cursor.fetchone()
                            
                            if existing_mark:
                                # Update existing marks
                                cursor.execute("UPDATE marks SET marks = %s WHERE student_id = %s AND subject_id = %s",
                                             (marks_float, self.student_id_var.get(), subject_id))
                            else:
                                # Insert new marks
                                cursor.execute("INSERT INTO marks (student_id, subject_id, marks) VALUES (%s, %s, %s)",
                                             (self.student_id_var.get(), subject_id, marks_float))
                    except ValueError:
                        messagebox.showwarning("Invalid Marks", f"Invalid marks for {subject}. Please enter a number between 0-100.")
            
            self.db_connection.commit()
            messagebox.showinfo("Success", "Student updated successfully!")
            self.clear_form()
            self.load_students()
            
        except Error as e:
            print(f"Error updating student: {e}")
            messagebox.showerror("Error", f"Error updating student: {e}")
    
    def delete_student(self):
        """Delete a student from the database"""
        if not self.student_id_var.get():#Ensures that the user has selected a student in the UI before trying to delete.


            messagebox.showwarning("Warning", "Please select a student to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?"):
            try:
                cursor = self.db_connection.cursor()
                cursor.execute("DELETE FROM students WHERE id = %s", (self.student_id_var.get(),))
                self.db_connection.commit()
                messagebox.showinfo("Success", "Student deleted successfully!")
                self.clear_form()
                self.load_students()
            except Error as e:
                print(f"Error deleting student: {e}")
                messagebox.showerror("Error", f"Error deleting student: {e}")
    
    def validate_form(self):
        """Validate the form fields"""
        if not self.name_var.get().strip():
            messagebox.showwarning("Validation Error", "Name is required.")
            return False
        
        if not self.roll_no_var.get().strip():
            messagebox.showwarning("Validation Error", "Roll number is required.")
            return False
        
        # Validate email format
        email = self.email_var.get().strip()
        if email and "@" not in email:
            messagebox.showwarning("Validation Error", "Please enter a valid email address.")
            return False
        
        return True
    
    def clear_form(self):
        """Clear all form fields"""
        self.student_id_var.set("")
        self.name_var.set("")
        self.roll_no_var.set("")
        self.dob_var.set("")
        self.gender_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.address_var.set("")
        
        for subject in self.subjects:
            self.subject_vars[subject].set("")
    
    def load_students(self):
        """Load all students into the treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("""
                SELECT id, name, roll_no, dob, gender, phone, email 
                FROM students 
                ORDER BY name
            """)
            
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
                
        except Error as e:
            print(f"Error loading students: {e}")
            messagebox.showerror("Error", f"Error loading students: {e}")
    
    def on_student_select(self, event):
        """Handle student selection from treeview"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            student_id = item['values'][0]
            self.load_student_details(student_id)
    
    def load_student_details(self, student_id):
        """Load student details into the form"""
        try:
            cursor = self.db_connection.cursor()
            
            # Get student details
            cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
            student = cursor.fetchone()
            
            if student:
                self.student_id_var.set(student[0])
                self.name_var.set(student[1])
                self.roll_no_var.set(student[2])
                self.dob_var.set(str(student[3]) if student[3] else "")
                self.gender_var.set(student[4] if student[4] else "")
                self.phone_var.set(student[5] if student[5] else "")
                self.email_var.set(student[6] if student[6] else "")
                self.address_var.set(student[7] if student[7] else "")
                
                # Get marks
                cursor.execute("""
                    SELECT s.name, m.marks 
                    FROM marks m 
                    JOIN subjects s ON m.subject_id = s.id 
                    WHERE m.student_id = %s
                """, (student_id,))
                
                marks_data = cursor.fetchall()
                for subject in self.subjects:
                    self.subject_vars[subject].set("")
                
                for subject_name, marks in marks_data:
                    if subject_name in self.subject_vars:
                        self.subject_vars[subject_name].set(str(marks))
                        
        except Error as e:
            print(f"Error loading student details: {e}")
            messagebox.showerror("Error", f"Error loading student details: {e}")
    
    def search_students(self):
        """Search students by name or roll number"""
        search_term = self.search_var.get().strip()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term.")
            return
        
        # Clear existing items
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
        
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("""
                SELECT s.id, s.name, s.roll_no, s.dob, s.gender, s.phone, s.email,
                       COALESCE(AVG(m.marks), 0) as avg_marks
                FROM students s
                LEFT JOIN marks m ON s.id = m.student_id
                WHERE s.name LIKE %s OR s.roll_no LIKE %s
                GROUP BY s.id, s.name, s.roll_no, s.dob, s.gender, s.phone, s.email
                ORDER BY s.name
            """, (f"%{search_term}%", f"%{search_term}%"))
            
            for row in cursor.fetchall():
                # Format average marks to 2 decimal places
                formatted_row = list(row)
                formatted_row[7] = f"{formatted_row[7]:.2f}"
                self.search_tree.insert("", "end", values=formatted_row)
                
        except Error as e:
            print(f"Error searching students: {e}")
            messagebox.showerror("Error", f"Error searching students: {e}")
    
    def clear_search(self):
        """Clear search results"""
        self.search_var.set("")
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
    
    def on_search_student_select(self, event):
        """Handle student selection from search results"""
        selection = self.search_tree.selection()
        if selection:
            item = self.search_tree.item(selection[0])
            student_id = item['values'][0]
            self.load_student_details(student_id)
            # Switch to student tab
            self.notebook.select(0)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()
    
    def __del__(self):
        """Cleanup database connection"""
        if self.db_connection and self.db_connection.is_connected():
            self.db_connection.close()

if __name__ == "__main__":
    app = StudentManagementSystem()
    app.run()