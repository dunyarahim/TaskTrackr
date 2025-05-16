"""TaskTrackr: A command-line task manager that allows you to add, view, complete, 
   and delete tasks using simple terminal commands."""

import re
from datetime import datetime,timedelta
import json
import argparse
import os

class TaskManager:

    TASKS_FILE = 'tasks.json'
    def __init__(self):
        self.tasks = []



    def load_tasks(self):
        try:
            with open(self.TASKS_FILE, 'r') as file:
                self.tasks = json.load(file)
                print("✅ Tasks loaded from file:")
                print(json.dumps(self.tasks, indent=4))
        except FileNotFoundError:
            print(f"⚠️ File not found: {self.TASKS_FILE}")
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON format in {self.TASKS_FILE}")

        # Prompt if no tasks loaded
        if not self.tasks:
            self.tasks = []
            print("\n📥 Enter your tasks one by one. Type 'done' when you're finished.")
            while True:
                desc = input("Enter task description: ").strip()
                if desc.lower() == 'done':
                    break
                if not desc:
                    print("❌ Description can't be empty.")
                    continue
                due_date = input("Enter due date (MM/DD/YYYY or leave blank): ").strip()
                self.tasks.append({
                    "description": desc,
                    "status": "incomplete",
                    "due_date": due_date if due_date else "N/A"
                })
            
            # 🔄 Save tasks immediately
            self.save_tasks()


    def save_tasks(self):
        try:
            with open(self.TASKS_FILE, 'w') as file:
                json.dump(self.tasks, file, indent=4)
            print("💾 Tasks saved successfully.")
        except Exception as e:
            print(f"❌ Failed to save tasks: {e}")



    """Adds task to current list of tasks displayed in terminal
    Needs to be adjusted to perhaps display in tuple form or a list of tasks
    """
    def add_task(self, description, due_date=None):
        task = {
            "description": description,
            "status": "incomplete",
            "due_date": due_date if due_date else "N/A"
        }
        self.tasks.append(task)

    """Sets the criteria for tasks to be grouped in and moves each tasks to said criteria
    then returns the organized tasks under established categories in cetrian format
    """
    def organize_and_display_tasks(self):
        categorized_tasks = {
            'Overdue': [],
            'Due Today': [],
            'Due This Week': [],
            'Due Later': [],
            'No Due Date': [],
            'Invalid Dates': []
        }

        today = datetime.today()
        end_of_week = today + timedelta(days=(6 - today.weekday()))

        for task in self.tasks:
            due_string = task.get('due_date', '').strip()

            try:
                if due_string and due_string.upper() != 'N/A':
                    parsed_date = datetime.strptime(due_string.replace('-', '/'), '%m/%d/%Y')

                    if parsed_date.date() < today.date():
                        categorized_tasks['Overdue'].append(task)
                    elif parsed_date.date() == today.date():
                        categorized_tasks['Due Today'].append(task)
                    elif today.date() < parsed_date.date() <= end_of_week.date():
                        categorized_tasks['Due This Week'].append(task)
                    else:
                        categorized_tasks['Due Later'].append(task)
                else:
                    categorized_tasks['No Due Date'].append(task)
            except ValueError:
                print(f"⚠️ Warning: Task with invalid date gets skipped: {due_string}")
                categorized_tasks['Invalid Dates'].append(task)

        # Display the categorized tasks
        print("\n📋 Task Overview by Category:\n" + "-" * 40)
        for category, tasks in categorized_tasks.items():
            print(f"\n🗂️ {category} ({len(tasks)} task{'s' if len(tasks) != 1 else ''}):")
            if tasks:
                for i, task in enumerate(tasks, 1):
                    title = task.get('description')
                    due = task.get('due_date', 'N/A')
                    print(f"  {i}. {title} (Due: {due})")
            else:
                print("  No tasks in this category.")


                                
                

    """ Displays the list of tasks and their completion levels
    Might be updated so the application file is cleaner and more concise while manager file handles the backend work"""

    def display_tasks(self):
        for i, task in enumerate(self.tasks):
            print(f"{i + 1}. {task['description']} - Status: {task['status']}, Due: {task.get('due_date', 'N/A')}")


    """Dipslays the progress of the task in organized groups.
    Specifically whether the task is done or not. Might be adjusted for other percentages depending on 
    use case"""

    def progress_tracker(self,idx):
            task = self.tasks[idx]
            progress_prompt = input(f"Have you finished the task {task}?  Enter Yes or No: ").strip().lower()
            if(progress_prompt == "yes"):
                task["status"] = "complete"
                print(f"✅ Task '{task['description']}' is 100% done and marked as complete.")
                

            elif(progress_prompt == "no"):
                print(f"⏳ Task '{task}' is still in progress.")
            else:
                print("Invalid input")
                return None
            
            return self.save_tasks()


    def deadline_manager(self, idx):
        task = self.tasks[idx]
        deadline_prompt = input(f"When is the task '{task}' due? Insert in form MM/DD/YYYY or MM-DD-YYYY: ")

        def is_valid_date(date_string):
            # Accepts both MM/DD/YYYY and MM-DD-YYYY
            date_pattern = re.compile(r"^\d{2}[-/]\d{2}[-/]\d{4}$")
            return bool(date_pattern.match(date_string))

        if is_valid_date(deadline_prompt):
            try:
                parsed_date = datetime.strptime(deadline_prompt.replace("-", "/"), "%m/%d/%Y")
                # Store deadline in a dictionary (e.g., self.deadlines = {})
                if not hasattr(self, 'deadlines'):
                    self.deadlines = {}
                self.deadlines[task] = parsed_date
                print(f"Deadline set for '{task}' on {parsed_date.strftime('%B %d, %Y')}")
            except ValueError:
                print("❌ Could not parse the date. Please try again.")
        else:
            print("❌ Invalid date format. Please use MM/DD/YYYY or MM-DD-YYYY.")


def main():
    manager = TaskManager()
    manager.load_tasks()

    while True:
        cmd = input("\nChoose an action - add/show/organize/progress/deadline/exit: ").strip().lower()
        
        if cmd == 'add':
            desc = input("Enter the task: ").strip()
            manager.add_task(desc)
        
        elif cmd == 'show':
            manager.display_tasks()
        
        elif cmd == 'organize':
            manager.organize_and_display_tasks()
            print("Organized by date and priority")
        
        elif cmd == 'progress':
            manager.display_tasks()
            try:
                idx = int(input("Select task number to update: ")) - 1
                manager.progress_tracker(idx)
            except (IndexError, ValueError):
                print("❌ Invalid selection.")
        
        elif cmd == 'deadline':
            manager.display_tasks()
            try:
                idx = int(input("Select task number for deadline: ")) - 1
                manager.deadline_manager(idx)
            except (IndexError, ValueError):
                print("❌ Invalid selection.")
        
        elif cmd == 'exit':
            manager.save_tasks()
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Unknown command. Try again.")



if __name__ == "__main__":
    main()


