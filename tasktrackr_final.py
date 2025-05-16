import json
import os
import argparse
import re
from datetime import datetime, timedelta

TASKS_FILE = 'tasks.json'

class Task:
    def __init__(self, task_id, title, due_date, priority, completed=False):
        self.id = task_id
        self.title = title
        self.due_date = due_date
        self.priority = priority
        self.completed = completed

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date,
            "priority": self.priority,
            "completed": self.completed
        }

    @staticmethod
    def from_dict(data):
        return Task(
            data['id'],
            data['title'],
            data['due_date'],
            data['priority'],
            data['completed']
        )

class TaskManager:
    def __init__(self):
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if not os.path.exists(TASKS_FILE):
            return []
        with open(TASKS_FILE, 'r') as f:
            data = json.load(f)
            return [Task.from_dict(d) for d in data]

    def save_tasks(self):
        with open(TASKS_FILE, 'w') as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=4)

    def generate_task_id(self):
        if not self.tasks:
            return 1
        else:
            return max(task.id for task in self.tasks) + 1
    
    def add_task(self, title, due_date, priority):
        task_id = self.generate_task_id()
        task = Task(task_id, title, due_date, priority)
        self.tasks.append(task)
        self.save_tasks()
        print(f"✅ Task added: {title}")

    def list_tasks(self, status_filter=None):
        if not self.tasks:
            print("No tasks found.")
            return
        for task in self.tasks:
            if status_filter == "pending" and task.completed:
                continue
            if status_filter == "completed" and not task.completed:
                continue
            status = "✓" if task.completed else "✗"
            print(f"[{task.id}] {status} {task.title} (Due: {task.due_date}, Priority: {task.priority})")

    def complete_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                self.save_tasks()
                return
        print("Task not found.")

    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t.id != task_id]
        self.save_tasks()

    def update_task(self, task_id, title=None, due_date=None, priority=None):
        for task in self.tasks:
            if task.id == task_id:
                if title:
                    task.title = title
                if due_date:
                    task.due_date = due_date
                if priority:
                    task.priority = priority
                self.save_tasks()
                return
        print("Task not found.")

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
            due_string = task.due_date.strip()

            try:
                if due_string.upper() != 'N/A':
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
                categorized_tasks['Invalid Dates'].append(task)

        return categorized_tasks

    def progress_tracker(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                response = input(f"Have you finished '{task.title}'? Yes/No: ").strip().lower()
                if response == "yes":
                    task.completed = True
                elif response == "no":
                    task.completed = False
                self.save_tasks()
                return
        print("Task not found.")

    def deadline_manager(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                deadline_prompt = input(f"When is '{task.title}' due? (MM/DD/YYYY or MM-DD-YYYY): ")
                if re.match(r"^\d{2}[-/]\d{2}[-/]\d{4}$", deadline_prompt):
                    try:
                        parsed_date = datetime.strptime(deadline_prompt.replace("-", "/"), "%m/%d/%Y")
                        task.due_date = parsed_date.strftime("%m/%d/%Y")
                        self.save_tasks()
                        return
                    except ValueError:
                        pass
        print("❌ Invalid input or task not found.")

def main():
    parser = argparse.ArgumentParser(description="TaskTrackr")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--title", required=True)
    add_parser.add_argument("--due", required=True)
    add_parser.add_argument("--priority", default="Medium")

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--status", choices=["pending", "completed"])

    complete_parser = subparsers.add_parser("complete")
    complete_parser.add_argument("--id", type=int, required=True)

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--id", type=int, required=True)

    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--id", type=int, required=True)
    update_parser.add_argument("--title")
    update_parser.add_argument("--due")
    update_parser.add_argument("--priority")

    progress_parser = subparsers.add_parser("progress")
    progress_parser.add_argument("--id", type=int, required=True)

    deadline_parser = subparsers.add_parser("deadline")
    deadline_parser.add_argument("--id", type=int, required=True)

    organize_parser = subparsers.add_parser("organize")

    args = parser.parse_args()
    manager = TaskManager()

    if args.command == "add":
        manager.add_task(args.title, args.due, args.priority)
    elif args.command == "list":
        manager.list_tasks(status_filter=args.status)
    elif args.command == "complete":
        manager.complete_task(args.id)
    elif args.command == "delete":
        manager.delete_task(args.id)
    elif args.command == "update":
        manager.update_task(args.id, args.title, args.due, args.priority)
    elif args.command == "progress":
        manager.progress_tracker(args.id)
    elif args.command == "deadline":
        manager.deadline_manager(args.id)
    elif args.command == "organize":
        organized = manager.organize_tasks()
        for category, tasks in organized.items():
            print(f"\n{category}:")
            for task in tasks:
                status = "✓" if task.completed else "✗"
                print(f"{status} {task.title} (Due: {task.due_date})")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
