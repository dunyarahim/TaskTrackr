"""TaskTrackr – Developed by Dunya Rahim
This version focuses on the Task class and CRUD logic for task management."""

import json
import os
import argparse

TASKS_FILE = 'tasks.json'


class Task:
    """This class represents a single task with attributes: title, due date, priority, and completion status."""
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

    def from_dict(data):
        return Task(
            data['id'],
            data['title'],
            data['due_date'],
            data['priority'],
            data['completed']
        )

class TaskManager:
    """This class handles the loading, saving, and managing tasks part."""

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

    def add_task(self, title, due_date, priority):
        task_id = len(self.tasks) + 1
        task = Task(task_id, title, due_date, priority)
        self.tasks.append(task)
        self.save_tasks()
        print(f"Task added: {title}")

    def list_tasks(self):
        if not self.tasks:
            print("No tasks found.")
            return
        for task in self.tasks:
            status = "✓" if task.completed else "✗"
            print(f"[{task.id}] {status} {task.title} (Due: {task.due_date}, Priority: {task.priority})")

    def complete_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                self.save_tasks()
                print(f"Task marked as completed: {task.title}")
                return
        print("Task not found.")

    def delete_task(self, task_id):
        original_length = len(self.tasks)
        self.tasks = [x for x in self.tasks if x.id != task_id]
        if len(self.tasks) == original_length:
            print("Task not found.")
            return
        self.save_tasks()
        print(f"Task {task_id} deleted.")

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
                print(f"Task {task_id} updated.")
                return
        print("Task not found.")


def main():
    parser = argparse.ArgumentParser(description="TaskTrackr – Dunya Rahim")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--title", required=True)
    add_parser.add_argument("--due", required=True)
    add_parser.add_argument("--priority", default="Medium")

    list_parser = subparsers.add_parser("list")

    complete_parser = subparsers.add_parser("complete")
    complete_parser.add_argument("--id", type=int, required=True)

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--id", type=int, required=True)

    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--ID", type=int, required=True)
    update_parser.add_argument("--Title")
    update_parser.add_argument("--Due Date")
    update_parser.add_argument("--Priority Level")

    args = parser.parse_args()
    manager = TaskManager()

    if args.command == "add":
        manager.add_task(args.title, args.due, args.priority)
    elif args.command == "list":
        manager.list_tasks()
    elif args.command == "complete":
        manager.complete_task(args.id)
    elif args.command == "delete":
        manager.delete_task(args.id)
    elif args.command == "update":
        manager.update_task(args.id, args.title, args.due, args.priority)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
