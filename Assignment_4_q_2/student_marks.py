import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('student_marks.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    roll_number INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS subjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_name TEXT NOT NULL,
    teacher_name TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS marks (
    roll_number INTEGER,
    subject_id INTEGER,
    marks INTEGER,
    PRIMARY KEY (roll_number, subject_id),
    FOREIGN KEY (roll_number) REFERENCES students (roll_number),
    FOREIGN KEY (subject_id) REFERENCES subjects (subject_id)
)
''')

conn.commit()

# Function to add a new student
def add_student(roll_number, name):
    cursor.execute('''
    INSERT INTO students (roll_number, name)
    VALUES (?, ?)
    ''', (roll_number, name))
    conn.commit()
    print(f"Student '{name}' added successfully!")

# Function to add a new subject
def add_subject(subject_name, teacher_name):
    cursor.execute('''
    INSERT INTO subjects (subject_name, teacher_name)
    VALUES (?, ?)
    ''', (subject_name, teacher_name))
    conn.commit()
    print(f"Subject '{subject_name}' added successfully!")

# Function to update marks for a subject
def update_marks(roll_number, subject_id, marks):
    cursor.execute('''
    INSERT OR REPLACE INTO marks (roll_number, subject_id, marks)
    VALUES (?, ?, ?)
    ''', (roll_number, subject_id, marks))
    conn.commit()
    print(f"Marks updated for Roll Number {roll_number} in Subject ID {subject_id}!")

# Function to view students and their roll numbers
def view_students():
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    for student in students:
        print(f"Roll Number: {student[0]}, Name: {student[1]}")

# Function to view marks for a specific subject
def view_marks(subject_id):
    cursor.execute('''
    SELECT students.roll_number, students.name, marks.marks
    FROM marks
    JOIN students ON marks.roll_number = students.roll_number
    WHERE marks.subject_id = ?
    ''', (subject_id,))
    marks = cursor.fetchall()
    for mark in marks:
        print(f"Roll Number: {mark[0]}, Name: {mark[1]}, Marks: {mark[2]}")

# Function to calculate and sort students by total marks
def sort_by_total_marks():
    cursor.execute('''
    SELECT students.roll_number, students.name, SUM(marks.marks) AS total_marks
    FROM marks
    JOIN students ON marks.roll_number = students.roll_number
    GROUP BY students.roll_number
    ORDER BY total_marks DESC
    ''')
    results = cursor.fetchall()
    for result in results:
        print(f"Roll Number: {result[0]}, Name: {result[1]}, Total Marks: {result[2]}")

# Main menu
def main():
    while True:
        print("\nStudent Marks Management System")
        print("1. Add Student")
        print("2. Add Subject")
        print("3. Update Marks")
        print("4. View Students")
        print("5. View Marks for a Subject")
        print("6. Sort Students by Total Marks")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            roll_number = int(input("Enter Roll Number: "))
            name = input("Enter Student Name: ")
            add_student(roll_number, name)
        elif choice == '2':
            subject_name = input("Enter Subject Name: ")
            teacher_name = input("Enter Teacher Name: ")
            add_subject(subject_name, teacher_name)
        elif choice == '3':
            roll_number = int(input("Enter Roll Number: "))
            subject_id = int(input("Enter Subject ID: "))
            marks = int(input("Enter Marks: "))
            update_marks(roll_number, subject_id, marks)
        elif choice == '4':
            view_students()
        elif choice == '5':
            subject_id = int(input("Enter Subject ID: "))
            view_marks(subject_id)
        elif choice == '6':
            sort_by_total_marks()
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

# Close the database connection when done
conn.close()