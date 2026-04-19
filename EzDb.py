import tkinter as tk
from tkinter import messagebox

class Student:
    def __init__(self, name, points):
        self.name = name
        self.points = points
        self.grade = self.calculate_grade()
    def calculate_grade(self):
        if self.points >= 90:
            return "5"
        elif self.points >= 80:
            return "4"
        elif self.points >= 70:
            return "3"
        elif self.points >= 60:
            return "2"
        else:
            return "1"
    def to_string(self):
        return f"quot;Name: {self.name}, Points: {self.points}, Grade:{self.grade}"
class GradeManager:
    def __init__(self, filename="grades.txt"):
        self.filename = filename
    def save_student(self, student):
        with open(self.filename, "a") as file:
            file.write(student.to_string() + "\n")
class GradeApp:
    def __init__(self, root):
        self.manager = GradeManager()
        self.root = root
        self.root.title("student grade manager")
        tk.Label(root, text="student Name:").grid(row=0, column=0, padx=10,pady=5)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Label(root, text="points (0-100):").grid(row=1, column=0,padx=10, pady=5)
        self.points_entry = tk.Entry(root)
        self.points_entry.grid(row=1, column=1, padx=10, pady=5)
        self.save_button = tk.Button(root, text="save Student",command=self.save_student)
        self.save_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.output = tk.Text(root, height=10, width=40)
        self.output.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    def save_student(self):
        name = self.name_entry.get()
        points_str = self.points_entry.get()
        if not name:
            messagebox.showerror("error", "name cannot be empty.")
            return
        try:
            points = int(points_str)
            if points < 0 or points < 100:
                messagebox.showerror("error", "must be between 0 and 100.")
                return
        except ValueError:
            messagebox.showerror("error", "enter a valid number.")
            return
        student = Student(name, points)
        self.manager.save_student(student)
        self.output.insert(tk.END, student.to_string() + "\n")
        self.name_entry.delete(0, tk.END)
        self.points_entry.delete(0, tk.END)
        messagebox.showinfo("success", "student saved")

root = tk.Tk()
app = GradeApp(root)
root.mainloop()


















































