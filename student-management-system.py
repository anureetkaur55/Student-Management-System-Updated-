import json
from pathlib import Path

DATA_FILE = Path("students.json")


class Student:
    def __init__(self, student_id, name, age, marks):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.marks = marks

    def to_dict(self):
        return vars(self)

    @classmethod
    def from_dict(cls, data):
        return cls(data["student_id"], data["name"], data["age"], data["marks"])


class StudentManagementSystem:
    def __init__(self):
        self.students = []
        self.load_students()

    def add_student(self):
        self.heading("Add New Student")
        student_id = input("Student ID: ").strip()

        if not student_id:
            print("Student ID cannot be empty.")
            return
        if self.find_student(student_id):
            print("A student with this ID already exists.")
            return

        name = input("Student Name: ").strip()
        if not name:
            print("Student name cannot be empty.")
            return

        age = self.get_int("Age: ", 1)
        marks = self.get_float("Marks: ", 0, 100)

        self.students.append(Student(student_id, name, age, marks))
        self.save_students()
        print("Student added successfully.")

    def view_students(self):
        self.heading("All Students")
        if not self.students:
            print("No student records found.")
            return
        self.table(self.students)

    def search_student(self):
        self.heading("Search Student")
        student = self.find_student(input("Enter Student ID: ").strip())
        self.table([student]) if student else print("Student not found.")

    def update_marks(self):
        self.heading("Update Marks")
        student = self.find_student(input("Enter Student ID: ").strip())
        if not student:
            print("Student not found.")
            return

        print(f"Current marks for {student.name}: {student.marks}")
        student.marks = self.get_float("New Marks: ", 0, 100)
        self.save_students()
        print("Marks updated successfully.")

    def delete_student(self):
        self.heading("Delete Student")
        student = self.find_student(input("Enter Student ID: ").strip())
        if not student:
            print("Student not found.")
            return

        confirm = input(f"Delete {student.name}'s record? (y/n): ").lower()
        if confirm == "y":
            self.students.remove(student)
            self.save_students()
            print("Student record deleted successfully.")
        else:
            print("Delete cancelled.")

    def highest_marks_student(self):
        self.heading("Highest Marks")
        if not self.students:
            print("No student records found.")
            return
        self.table([max(self.students, key=lambda student: student.marks)])

    def find_student(self, student_id):
        for student in self.students:
            if student.student_id.lower() == student_id.lower():
                return student
        return None

    def save_students(self):
        with DATA_FILE.open("w") as file:
            json.dump([student.to_dict() for student in self.students], file, indent=4)

    def load_students(self):
        if DATA_FILE.exists():
            with DATA_FILE.open("r") as file:
                self.students = [Student.from_dict(item) for item in json.load(file)]

    @staticmethod
    def heading(title):
        print("\n" + "=" * 58)
        print(title.center(58))
        print("=" * 58)

    @staticmethod
    def table(students):
        print("+------------+----------------------+-----+--------+")
        print("| Student ID | Name                 | Age | Marks  |")
        print("+------------+----------------------+-----+--------+")
        for s in students:
            print(f"| {s.student_id:<10} | {s.name:<20} | {s.age:<3} | {s.marks:<6.2f} |")
        print("+------------+----------------------+-----+--------+")

    @staticmethod
    def get_int(prompt, minimum):
        while True:
            try:
                value = int(input(prompt))
                if value >= minimum:
                    return value
                print(f"Value must be at least {minimum}.")
            except ValueError:
                print("Please enter a valid whole number.")

    @staticmethod
    def get_float(prompt, minimum, maximum):
        while True:
            try:
                value = float(input(prompt))
                if minimum <= value <= maximum:
                    return value
                print(f"Value must be between {minimum} and {maximum}.")
            except ValueError:
                print("Please enter a valid number.")


def menu():
    print("\n" + "*" * 58)
    print(" STUDENT MANAGEMENT SYSTEM ".center(58, "*"))
    print("*" * 58)
    print("1. Add new student")
    print("2. View all students")
    print("3. Search student by ID")
    print("4. Update marks")
    print("5. Delete student")
    print("6. Show highest marks")
    print("7. Exit")


def main():
    system = StudentManagementSystem()

    while True:
        menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            system.add_student()
        elif choice == "2":
            system.view_students()
        elif choice == "3":
            system.search_student()
        elif choice == "4":
            system.update_marks()
        elif choice == "5":
            system.delete_student()
        elif choice == "6":
            system.highest_marks_student()
        elif choice == "7":
            print("Thank you for using the Student Management System.")
            break
        else:
            print("Invalid choice. Please select 1 to 7.")


if __name__ == "__main__":
    main()