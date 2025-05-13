import re
from datetime import datetime, timedelta
import json

class TaskManager:
    TASKS_FILE = 'tasks.json'

    def __init__(self):
        self.tasks = []

    def load_tasks(self):
        try:
            with open(self.TASKS_FILE, 'r') as file:
                self.tasks = json.load(file)
                if self.tasks:
                    print(f"✅ {len(self.tasks)} tasks loaded from {self.TASKS_FILE}:")
                    print(json.dumps(self.tasks, indent=4))
                    return  
        except FileNotFoundError:
            print(f"⚠️ File not found: {self.TASKS_FILE}")
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON format in {self.TASKS_FILE}")

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
        self.save_tasks()
        

    def save_tasks(self):
        try:
            with open(self.TASKS_FILE, 'w') as file:
                json.dump(self.tasks, file, indent=4)
            print("💾 Tasks saved successfully.")
        except Exception as e:
            print(f"❌ Failed to save tasks: {e}")

    def add_task(self, description, due_date=None):
        task = {
            "description": description,
            "status": "incomplete",
            "due_date": due_date if due_date else "N/A"
        }
        self.tasks.append(task)

    def organize_tasks(self):
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
                print(f"⚠️ Warning: Task with invalid date skipped: {due_string}")
                categorized_tasks['Invalid Dates'].append(task)

        return categorized_tasks

    def display_tasks(self):
        for i, task in enumerate(self.tasks):
            print(f"{i + 1}. {task['description']} - Status: {task['status']}, Due: {task.get('due_date', 'N/A')}")

    def progress_tracker(self, idx):
        task = self.tasks[idx]
        progress_prompt = input(f"Have you finished the task '{task['description']}'? Enter Yes or No: ").strip().lower()
        if progress_prompt == "yes":
            task['status'] = "complete"
            print(f"✅ Task '{task['description']}' is 100% done.")
        elif progress_prompt == "no":
            task['status'] = "incomplete"
            print(f"⏳ Task '{task['description']}' is still in progress.")
        else:
            print("Invalid input")
            return None
        return task['status']

    def deadline_manager(self, idx):
        task = self.tasks[idx]
        deadline_prompt = input(f"When is the task '{task['description']}' due? (MM/DD/YYYY or MM-DD-YYYY): ")

        def is_valid_date(date_string):
            date_pattern = re.compile(r"^\d{2}[-/]\d{2}[-/]\d{4}$")
            return bool(date_pattern.match(date_string))

        if is_valid_date(deadline_prompt):
            try:
                parsed_date = datetime.strptime(deadline_prompt.replace("-", "/"), "%m/%d/%Y")
                task['due_date'] = parsed_date.strftime("%m/%d/%Y")
                print(f"📅 Deadline set for '{task['description']}' on {task['due_date']}")
            except ValueError:
                print("❌ Could not parse the date. Please try again.")
        else:
            print("❌ Invalid date format. Please use MM/DD/YYYY or MM-DD-YYYY.")


def main():
    manager = TaskManager()
    manager.load_tasks()

    while True:
        cmd = input("\nChoose an action - add/show/organize/progress/deadline/summary/exit: ").strip().lower()

        if cmd == 'add':
            desc = input("Enter the task: ").strip()
            due = input("Enter due date (MM/DD/YYYY or leave blank): ").strip()
            manager.add_task(desc, due)

        elif cmd == 'show':
            manager.display_tasks()

        elif cmd == 'organize':
            organized = manager.organize_tasks()
            for category, tasks in organized.items():
                print(f"\n📂 {category}:")
                for task in tasks:
                    print(f"  - {task['description']} (Due: {task.get('due_date', 'N/A')}, Status: {task['status']})")

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

        elif cmd == 'summary':
            organized = manager.organize_tasks()
            print("\n📋 Task Summary:")
            for category, tasks in organized.items():
                print(f"\n{category}:")
                for task in tasks:
                    status = task["status"]
                    icon = "✅" if status == "complete" else "⏳"
                    print(f"{icon} - {task['description']}")

        elif cmd == 'exit':
            manager.save_tasks()
            print("👋 Goodbye!")
            break

        else:
            print("❌ Unknown command. Try again.")


if __name__ == "__main__":
    main()
