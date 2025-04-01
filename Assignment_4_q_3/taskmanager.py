import sqlite3
import os

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                done INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def add_task(self, name, description):
        self.cursor.execute("INSERT INTO tasks (name, description, done) VALUES (?, ?, 0)", (name, description))
        self.conn.commit()

    def complete_task(self, name):
        self.cursor.execute("UPDATE tasks SET done = 1 WHERE name = ?", (name,))
        self.conn.commit()

    def remove_task(self, name):
        self.cursor.execute("DELETE FROM tasks WHERE name = ?", (name,))
        self.conn.commit()

    def edit_task(self, name, new_name=None, new_description=None, new_status=None):
        if new_name:
            self.cursor.execute("UPDATE tasks SET name = ? WHERE name = ?", (new_name, name))
        if new_description:
            self.cursor.execute("UPDATE tasks SET description = ? WHERE name = ?", (new_description, name))
        if new_status is not None:
            self.cursor.execute("UPDATE tasks SET done = ? WHERE name = ?", (int(new_status), name))
        self.conn.commit()

    def display_tasks(self, status=None):
        query = "SELECT name, description, done FROM tasks"
        params = ()
        if status == "cmp":
            query += " WHERE done = 1"
        elif status == "incmp":
            query += " WHERE done = 0"
        
        self.cursor.execute(query, params)
        tasks = self.cursor.fetchall()
        for i, (name, desc, done) in enumerate(tasks, 1):
            print(f" > Task {i} : \n   Name = {name}\n   Description = {desc}\n   Status = {'Done' if done else 'Not Done'}\n")

    def close(self):
        self.conn.close()

class TaskManager:
    def __init__(self):
        self.db = Database()

    def run(self):
        print(" // Type 'help' to see command list")
        while True:
            command = input().strip()
            if not command:
                continue
            if command.lower() == "q":
                break
            elif command.lower() == "help":
                self.show_help()
            else:
                self.process_command(command)
        self.db.close()

    def show_help(self):
        print(" > Commands are: ")
        print(" > add <task>       ----- adds a task to the list")
        print(" > edt <task>       ----- edits specified task in the list")
        print(" > cpt <task>       ----- completes the specified task")
        print(" > rem <task>       ----- removes the specified task")
        print(" > dis incmp        ----- displays only the incomplete tasks")
        print(" > dis cmp          ----- displays only the complete tasks")
        print(" > dis              ----- displays the task list fully")
        print(" > q                ----- quit")

    def process_command(self, command):
        parts = command.split(" ", 1)
        cmd = parts[0].lower()
        name = parts[1] if len(parts) > 1 else ""
        
        if cmd == "dis":
            if name:
                self.db.display_tasks(name)
            else:
                self.db.display_tasks()
        elif cmd == "add":
            description = input(" >>> Enter Description: ")
            self.db.add_task(name, description)
            print(" >>> Task added successfully\n")
        elif cmd == "edt":
            self.edit_task(name)
        elif cmd == "rem":
            self.db.remove_task(name)
            print(" >>> Task successfully removed\n")
        elif cmd == "cpt":
            self.db.complete_task(name)
            print(" >>> Task marked as complete\n")
        else:
            print(" >> Invalid command\n")

    def edit_task(self, name):
        print(" >> Enter 1 to edit name")
        print(" >> Enter 2 to edit Description")
        print(" >> Enter 3 to edit status")
        
        choice = input(" >> Your choice: ")
        if choice == "1":
            new_name = input(" >> Enter new Name: ")
            self.db.edit_task(name, new_name=new_name)
        elif choice == "2":
            new_desc = input(" >> Enter new Description: ")
            self.db.edit_task(name, new_description=new_desc)
        elif choice == "3":
            new_status = input(" >> Enter new Status (true for done, false for not done): ").lower() in ['true', '1']
            self.db.edit_task(name, new_status=new_status)
        else:
            print(" >> Invalid choice")

if __name__ == "__main__":
    TaskManager().run()
