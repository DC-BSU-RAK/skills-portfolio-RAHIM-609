import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk # Import ttk for themed widgets and structured data display
import os
# NOTE on Images: To use common formats (like PNG or JPG) for button backgrounds 
# or images, you MUST install the Pillow library: pip install Pillow.
# Then, you would use 'from PIL import Image, ImageTk' and load the image 
# using ImageTk.PhotoImage(). Tkinter only natively supports GIF format.

# --- Configuration and File Setup ---

FILE_NAME = "studentMarks.txt" 
MAX_CW_MARK = 60    # Total max mark for the 3 Courseworks (3 * 20)
MAX_EXAM_MARK = 100
MAX_TOTAL_MARK = 160 # Overall total possible mark (60 + 100)

# --- Data Processing Functions ---

def calculate_grade(percentage):
    """Calculates the student grade based on overall percentage."""
    if percentage >= 70:
        return 'A'
    elif percentage >= 60:
        return 'B'
    elif percentage >= 50:
        return 'C'
    elif percentage >= 40:
        return 'D'
    else:
        return 'F'

def process_record(parts):
    """
    Processes raw data parts into a fully calculated student dictionary, 
    including total mark, percentage, and grade.
    """
    try:
        # Data Extraction and Conversion
        code = int(parts[0].strip())
        name = parts[1].strip()
        cw_marks = [int(m.strip()) for m in parts[2:5]]
        exam_mark = int(parts[5].strip())

        # Validation (Ensures marks are within defined bounds)
        if not (0 <= exam_mark <= MAX_EXAM_MARK and all(0 <= m <= 20 for m in cw_marks)):
             raise ValueError("Mark out of defined range (CW max 20, Exam max 100).")

        # Core Calculations
        total_coursework = sum(cw_marks)
        total_mark = total_coursework + exam_mark
        percentage = (total_mark / MAX_TOTAL_MARK) * 100
        grade = calculate_grade(percentage)

        return {
            'code': code,
            'name': name,
            'cw1': cw_marks[0],
            'cw2': cw_marks[1],
            'cw3': cw_marks[2],
            'exam': exam_mark,
            'total_coursework': total_coursework,
            'total_mark': total_mark,
            'percentage': round(percentage, 2),
            'grade': grade
        }
    except (ValueError, IndexError) as e:
        print(f"Error processing record: {parts}. Skipping record. Error: {e}")
        return None

# --- Main Application Class ---

class StudentManagerApp:
    def __init__(self, master):
        self.master = master
        
        # --- Enhanced Styling Initialization ---
        self.style = ttk.Style()
        self.style.theme_use('clam') 
        master.configure(bg='#F0F4F8') 

        # Configure custom button style (Blue primary action color)
        self.style.configure('TButton', 
                             font=('Helvetica', 10, 'bold'), 
                             foreground='#FFFFFF',
                             background='#4A90E2',
                             bordercolor='#4A90E2',
                             borderwidth=0,
                             focuscolor='none',
                             padding=10)
        self.style.map('TButton', 
                       background=[('active', '#357ABD'), ('pressed', '#1F4F85')],
                       foreground=[('active', '#FFFFFF')])

        # Configure Treeview style for tabular data
        self.style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'), background="#B0C4DE", foreground="#004D40")
        self.style.configure("Treeview", font=('Consolas', 10), rowheight=25)
        self.style.map('Treeview', background=[('selected', '#A3C1AD')]) 

        master.title("Student Manager (File: studentMarks.txt)")
        master.config(menu=tk.Menu(master, tearoff=0)) 

        self.student_data = []
        self.load_data() 
        
        # --- NEW: Add Heading ---
        self.create_heading_label()

        # UI Setup
        self.create_buttons()
        self.create_treeview_area() 
        
        if not self.student_data:
             self.display_message("Error: Could not load any student data. Check your file format.")
        else:
             self.view_all_records()

    def load_data(self):
        """Loads student data from the file, processes it, and stores it in memory."""
        self.student_data = []
        try:
            with open(FILE_NAME, 'r') as f:
                f.readline() # Read and discard the student count
                
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split(',')
                        record = process_record(parts)
                        if record:
                            self.student_data.append(record)
            return True
        except FileNotFoundError:
            messagebox.showerror("File Error", f"The data file '{FILE_NAME}' was not found. Please ensure it is uploaded.")
            return False
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred while loading data: {e}")
            return False

    def save_data(self):
        """Writes the current in-memory data back to the file, ensuring persistence."""
        try:
            with open(FILE_NAME, 'w') as f:
                # 1. Write the count of students (required file format)
                f.write(f"{len(self.student_data)}\n")
                
                # 2. Write each student record in the original comma-separated format
                for student in self.student_data:
                    line = (
                        f"{student['code']},{student['name']},{student['cw1']},"
                        f"{student['cw2']},{student['cw3']},{student['exam']}\n"
                    )
                    f.write(line)
            return True
        except IOError:
            messagebox.showerror("File Error", f"Could not write to file: {FILE_NAME}. Changes not saved.")
            return False
    
    def create_heading_label(self):
        """Creates the main heading label for the application."""
        heading_label = tk.Label(self.master, 
                                 text="Student Management System", 
                                 font=('Helvetica', 16, 'bold'), 
                                 bg='#3949AB', # Dark blue background
                                 fg='white', 
                                 pady=10)
        heading_label.pack(fill='x', padx=0, pady=(0, 10))
        
    def create_buttons(self):
        """Creates a frame with buttons for all 8 functions, arranged in rows."""
        
        # NOTE on Button Images: 
        # To add a background image to these buttons:
        # 1. You would typically need to install the Pillow library (`pip install Pillow`).
        # 2. Load the image using ImageTk.PhotoImage().
        # 3. Use the `image` argument in the ttk.Button constructor:
        #
        #    self.button_img = ImageTk.PhotoImage(Image.open("your_image.png"))
        #    ttk.Button(row1, text="...", image=self.button_img, compound="left", command=...).pack(...)
        # 
        # Since Pillow might not be available in all environments, we are keeping the 
        # CSS-like styling using ttk.Style for guaranteed compatibility.
        
        button_frame = tk.Frame(self.master, bg='#F0F4F8', padx=20, pady=10)
        button_frame.pack(fill='x', padx=20, pady=(0, 10)) # Adjusted padding

        # --- Row 1: Core Viewing/Analysis Functions (1-4) ---
        row1 = tk.Frame(button_frame, bg='#F0F4F8')
        row1.pack(fill='x', pady=5)
        
        ttk.Button(row1, text="1. View All Records", command=self.view_all_records).pack(side=tk.LEFT, expand=True, fill='x', padx=5)
        ttk.Button(row1, text="2. View Individual Record", command=self.view_individual_record).pack(side=tk.LEFT, expand=True, fill='x', padx=5)
        ttk.Button(row1, text="3. Highest Score", command=lambda: self.show_extreme_mark(highest=True)).pack(side=tk.LEFT, expand=True, fill='x', padx=5)
        ttk.Button(row1, text="4. Lowest Score", command=lambda: self.show_extreme_mark(highest=False)).pack(side=tk.LEFT, expand=True, fill='x', padx=5)

        # --- Row 2: Extension/Modification Functions (5-8) ---
        row2 = tk.Frame(button_frame, bg='#F0F4F8')
        row2.pack(fill='x', pady=5)
        
        ttk.Button(row2, text="5. Sort Records", command=self.sort_records).pack(side=tk.LEFT, expand=True, fill='x', padx=5)
        ttk.Button(row2, text="6. Add Record", command=self.add_record).pack(side=tk.LEFT, expand=True, fill='x', padx=5)
        ttk.Button(row2, text="7. Delete Record", command=self.delete_record).pack(side=tk.LEFT, expand=True, fill='x', padx=5)
        ttk.Button(row2, text="8. Update Record", command=self.update_record).pack(side=tk.LEFT, expand=True, fill='x', padx=5)

        # --- Row 3: Exit Button ---
        row3 = tk.Frame(button_frame, bg='#F0F4F8')
        row3.pack(fill='x', pady=5)
        # Configure a distinctive style for the Exit button (Red)
        self.style.configure('Exit.TButton', background='#D32F2F', bordercolor='#D32F2F')
        self.style.map('Exit.TButton', background=[('active', '#B71C1C'), ('pressed', '#9A0007')])
        ttk.Button(row3, text="Exit Application", command=self.master.quit, style='Exit.TButton').pack(fill='x', padx=5, pady=5)

    def create_treeview_area(self):
        """Creates the ttk.Treeview widget for structured data display."""
        
        data_frame = tk.Frame(self.master, bg='#F0F4F8')
        data_frame.pack(padx=20, pady=(10, 20), fill="both", expand=True)

        # --- Treeview Setup ---
        columns = ('code', 'name', 'cw_total', 'exam', 'percentage', 'grade')
        self.tree = ttk.Treeview(data_frame, columns=columns, show='headings', selectmode='browse')

        # Define Headings and Column properties
        self.tree.heading('code', text='CODE', anchor=tk.W)
        self.tree.heading('name', text='NAME', anchor=tk.W)
        self.tree.heading('cw_total', text='CW TOTAL', anchor=tk.CENTER)
        self.tree.heading('exam', text='EXAM', anchor=tk.CENTER)
        self.tree.heading('percentage', text='PERCENTAGE', anchor=tk.CENTER)
        self.tree.heading('grade', text='GRADE', anchor=tk.CENTER)

        # Set specific widths and stretch property
        self.tree.column('code', width=70, anchor=tk.W, stretch=tk.NO)
        self.tree.column('name', width=200, anchor=tk.W, stretch=tk.YES)
        self.tree.column('cw_total', width=100, anchor=tk.CENTER, stretch=tk.NO)
        self.tree.column('exam', width=70, anchor=tk.CENTER, stretch=tk.NO)
        self.tree.column('percentage', width=120, anchor=tk.CENTER, stretch=tk.NO)
        self.tree.column('grade', width=70, anchor=tk.CENTER, stretch=tk.NO)

        # Add a scrollbar
        yscrollbar = ttk.Scrollbar(data_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscrollbar.set)
        
        # Packing the Treeview and Scrollbar
        yscrollbar.pack(side=tk.RIGHT, fill='y')
        self.tree.pack(fill="both", expand=True)
        
        # --- Summary Area ---
        self.summary_label = tk.Label(data_frame, 
                                     text="Current Status: Initializing...", 
                                     font=('Helvetica', 10, 'italic'), 
                                     bg='#F0F4F8', 
                                     fg='#3949AB', 
                                     pady=5, 
                                     justify=tk.LEFT, 
                                     anchor='w')
        self.summary_label.pack(side=tk.BOTTOM, fill='x')

    def display_data_in_treeview(self, title, records, summary_text=""):
        """Utility to clear the Treeview and display structured data."""
        # 1. Clear existing items in Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 2. Insert new records
        if records:
            for student in records:
                self.tree.insert('', tk.END, values=(
                    student['code'],
                    student['name'],
                    student['total_coursework'],
                    student['exam'],
                    f"{student['percentage']:.2f}",
                    student['grade']
                ))
        
        # 3. Update the summary label
        self.summary_label.config(text=f"Current View: {title}. {summary_text}")
        
    def display_message(self, message):
        """Utility to display non-tabular messages in the summary area."""
        self.display_data_in_treeview("Message/Error", [])
        self.summary_label.config(text=f"Current Status: {message}")


    # --- Menu 1: View all student records ---
    def view_all_records(self):
        """Displays all student records and class summary."""
        if not self.student_data:
            self.display_message("No student data available.")
            return

        total_marks_sum = sum(s['total_mark'] for s in self.student_data)
        num_students = len(self.student_data)
        
        avg_overall_percentage = (total_marks_sum / (num_students * MAX_TOTAL_MARK)) * 100

        summary_text = (
            f"Total Students: {num_students} | "
            f"Average Overall Percentage: {avg_overall_percentage:.2f}%"
        )
        
        self.display_data_in_treeview("All Student Records", self.student_data, summary_text)

    # --- Menu 2: View individual student record ---
    def view_individual_record(self):
        """Finds and displays a single student by code or name."""
        query = simpledialog.askstring("Input", "Enter Student Code or Name:", parent=self.master)
        if not query:
            return

        found_student = None
        
        # 1. Try to find by code first
        try:
            code_query = int(query)
            found_student = next((s for s in self.student_data if s['code'] == code_query), None)
        except ValueError:
            # 2. Search by name (partial and case-insensitive)
            name_query = query.lower()
            found_student = next((s for s in self.student_data if name_query in s['name'].lower()), None)

        if found_student:
            self.display_data_in_treeview(f"Individual Record: {found_student['name']}", [found_student])
        else:
            self.display_message(f"Error: No student found matching '{query}'.")

    # --- Menu 3 & 4: Show extreme mark (Highest/Lowest) ---
    def show_extreme_mark(self, highest=True):
        """Identifies and displays the student with the highest or lowest overall mark."""
        if not self.student_data:
            self.display_message("No student data available to find extremes.")
            return

        key = 'total_mark'
        if highest:
            best_student = max(self.student_data, key=lambda s: s[key])
            title = "Highest Overall Mark"
        else:
            best_student = min(self.student_data, key=lambda s: s[key])
            title = "Lowest Overall Mark"

        summary_text = f"Student: {best_student['name']} | Score: {best_student['total_mark']}"
        self.display_data_in_treeview(title, [best_student], summary_text)

    # --- Menu 5: Sort student records ---
    def sort_records(self):
        """Sorts student records and displays them based on user input."""
        sort_choice = simpledialog.askstring(
            "Sort Records", 
            "Enter 'A' for Ascending or 'D' for Descending order by Overall Mark:", 
            parent=self.master
        )
        if not sort_choice:
            return

        reverse_order = sort_choice.strip().lower() == 'd'
        
        # Use Python's built-in sorting on the total_mark key
        sorted_records = sorted(self.student_data, key=lambda s: s['total_mark'], reverse=reverse_order)
        
        order_text = "Descending" if reverse_order else "Ascending"
        self.display_data_in_treeview(f"Records Sorted ({order_text} by Total Mark)", sorted_records)
        

    # --- Menu 6: Add a student record ---
    def add_record(self):
        """Prompts for and adds a new student record, then saves the file."""
        code = simpledialog.askinteger("Add Student", "Enter new Student Code (1000-9999):", parent=self.master, minvalue=1000, maxvalue=9999)
        if code is None: return

        if any(s['code'] == code for s in self.student_data):
            messagebox.showwarning("Input Error", f"Student code {code} already exists. Please use a unique code.")
            return

        name = simpledialog.askstring("Add Student", "Enter Student Name:", parent=self.master)
        if not name: return

        # Gather marks with max limits
        cw1 = simpledialog.askinteger("Add Student", "Enter Coursework 1 Mark (Max 20):", parent=self.master, minvalue=0, maxvalue=20); 
        if cw1 is None: return
        cw2 = simpledialog.askinteger("Add Student", "Enter Coursework 2 Mark (Max 20):", parent=self.master, minvalue=0, maxvalue=20); 
        if cw2 is None: return
        cw3 = simpledialog.askinteger("Add Student", "Enter Coursework 3 Mark (Max 20):", parent=self.master, minvalue=0, maxvalue=20); 
        if cw3 is None: return
        exam = simpledialog.askinteger("Add Student", "Enter Exam Mark (Max 100):", parent=self.master, minvalue=0, maxvalue=100); 
        if exam is None: return

        # Create the new record and calculate derived fields
        raw_parts = [str(code), name, str(cw1), str(cw2), str(cw3), str(exam)]
        new_record = process_record(raw_parts)

        if new_record:
            self.student_data.append(new_record)
            if self.save_data():
                messagebox.showinfo("Success", f"Student {name} (Code: {code}) added successfully and file updated.")
            self.view_all_records()

    # --- Menu 7: Delete a student record ---
    def delete_record(self):
        """Allows user to select and delete a record, then saves the file."""
        query = simpledialog.askstring("Delete Student", "Enter Student Code or exact Name to DELETE:", parent=self.master)
        if not query:
            return

        initial_count = len(self.student_data)
        
        try:
            # 1. Try to delete by code
            code_query = int(query)
            self.student_data = [s for s in self.student_data if s['code'] != code_query]
            deleted_by = "Code"
        except ValueError:
            # 2. Delete by exact name match
            name_query = query.strip()
            self.student_data = [s for s in self.student_data if s['name'] != name_query]
            deleted_by = "Name"

        final_count = len(self.student_data)
        
        if final_count < initial_count:
            if self.save_data():
                messagebox.showinfo("Success", f"Student record(s) matching '{query}' deleted successfully and file updated.")
            self.view_all_records()
        else:
            self.display_message(f"Not Found: No student found with matching {deleted_by}: '{query}'.")

    # --- Menu 8: Update a student record ---
    def update_record(self):
        """Allows user to select a record and update specific fields, then saves the file."""
        query = simpledialog.askstring("Update Student", "Enter Student Code or Name to UPDATE:", parent=self.master)
        if not query:
            return

        # Find the student record
        student_to_update = None
        try:
            code_query = int(query)
            student_to_update = next((s for s in self.student_data if s['code'] == code_query), None)
        except ValueError:
            name_query = query.lower()
            student_to_update = next((s for s in self.student_data if s['name'].lower() == name_query), None)
            
        if not student_to_update:
            self.display_message(f"Not Found: No student found matching '{query}'.")
            return

        # Prompt for which field to update
        choice = simpledialog.askstring(
            "Update Field",
            f"Update record for {student_to_update['name']}. What to update?\n"
            "Options: 'name', 'cw1', 'cw2', 'cw3', 'exam'",
            parent=self.master
        )
        if not choice: return

        choice = choice.strip().lower()
        new_value = None
        
        # Get new value based on field type
        if choice == 'name':
            new_value = simpledialog.askstring("Update Name", "Enter new Name:", parent=self.master)
        elif choice in ['cw1', 'cw2', 'cw3']:
            new_value = simpledialog.askinteger(f"Update {choice.upper()}", f"Enter new mark (Max 20):", parent=self.master, minvalue=0, maxvalue=20)
        elif choice == 'exam':
            new_value = simpledialog.askinteger("Update Exam", f"Enter new mark (Max 100):", parent=self.master, minvalue=0, maxvalue=100)
        else:
            self.display_message("Invalid Field: Invalid field name entered. Update aborted.")
            return

        if new_value is None: return

        # Apply update to the in-memory dictionary
        student_to_update[choice] = new_value
        
        # If a mark was updated, recalculate all derived fields 
        if choice in ['cw1', 'cw2', 'cw3', 'exam']:
            raw_parts = [
                str(student_to_update['code']), 
                student_to_update['name'], 
                str(student_to_update['cw1']), 
                str(student_to_update['cw2']), 
                str(student_to_update['cw3']), 
                str(student_to_update['exam'])
            ]
            
            updated_record = process_record(raw_parts)
            
            if updated_record:
                index = self.student_data.index(student_to_update)
                self.student_data[index] = updated_record
                student_to_update = updated_record 
            
        if self.save_data():
            messagebox.showinfo("Success", f"Student {student_to_update['name']}'s {choice} updated successfully and file saved.")
        
        self.display_data_in_treeview(f"Updated Record for {student_to_update['name']}", [student_to_update])


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = StudentManagerApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Application failed to start: {e}")