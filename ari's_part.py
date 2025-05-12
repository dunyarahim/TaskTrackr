"""TaskTrackr: A command-line task manager that allows you to add, view, complete, 
   and delete tasks using simple terminal commands."""

import re
from datetime import datetime
import json
import os

class TaskManager:

    TASKS_FILE = 'tasks.json'

   """
        Initializes the TaskManager instance.
        Loads tasks from a JSON file if it exists.
        Initializes an empty list of tasks and deadlines.
        """

    def __init__(self):
        self.tasks = []
        self.deadlines = {}
        self.load_tasks()

   #Loads tasks from JSON file and to a json file to process user tasks
        """
        Loads tasks from the JSON file.
        If the file exists and is properly formatted, tasks are loaded into memory.
        If not, it either initializes with an empty list or prints an error.
        """

    def load_tasks(self):
        if os.path.exists(self.TASKS_FILE):
            try:
                with open(self.TASKS_FILE, 'r') as file:
                    self.tasks = json.load(file)
                    print("✅ Loaded tasks from file:")
                    print(json.dumps(self.tasks, indent=4))
            except json.JSONDecodeError:
                print(f"❌ Error: Invalid JSON format in {self.TASKS_FILE}")
                self.tasks = []
        else:
            print(f"⚠️ No existing task file found at {self.TASKS_FILE}. Starting with empty task list.")

   #saves user tasks in a file to later display
"""
        Saves the current list of tasks to the JSON file.
        Writes tasks in a pretty-printed JSON format.
        """
    def save_tasks(self):
        try:
            with open(self.TASKS_FILE, 'w') as file:
                json.dump(self.tasks, file, indent=4)
            print("✅ Tasks saved successfully.")
        except Exception as e:
            print(f"❌ Failed to save tasks: {e}")

"""
        Adds a new task with the given description to the task list.
        Automatically sets the status to 'incomplete' and saves the task list.
        """
    def add_task(self, description):
        task = {
            "description": description,
            "status": "incomplete"
        }
        self.tasks.append(task)
        self.save_tasks()

   #Organizes and adjusts task to prepare for later display
"""
        Organizes tasks into categories based on the first letter of their description.
        Returns a dictionary of categorized task lists.
        """
    def organize_task(self):
        categorized_tasks = {
            'ClassType A': [],
            'ClassType B': [],
            'ClassType C': [],
            'Other': []
        }

        for task in self.tasks:
            desc = task["description"]
            if desc.startswith('A'):
                categorized_tasks['ClassType A'].append(task)
            elif desc.startswith('B'):
                categorized_tasks['ClassType B'].append(task)
            elif desc.startswith('C'):
                categorized_tasks['ClassType C'].append(task)
            else:
                categorized_tasks['Other'].append(task)

        return categorized_tasks

"""
        Displays the current list of tasks with their status.
        Each task is numbered for easy reference.
        may be deleted for alternatives provided by group
        """
    def display_tasks(self):
        for i, task in enumerate(self.tasks):
            print(f"{i + 1}. {task['description']} - {task['status']}")

   #Tracks tasks progress and may not be used as other versions by other members may be used instead
    def progress_tracker(self, task_index):
        if task_index < 0 or task_index >= len(self.tasks):
            print("❌ Invalid task index.")
            return

        task = self.tasks[task_index]
        progress_prompt = input(f"Have you finished the task '{task['description']}'? Enter Yes or No: ").strip().lower()
        if progress_prompt == "yes":
            task["status"] = "complete"
            print(f"✅ Task '{task['description']}' is 100% done.")
        elif progress_prompt == "no":
            task["status"] = "incomplete"
            print(f"⏳ Task '{task['description']}' is still in progress.")
        else:
            print("❌ Invalid input.")
            return

        self.save_tasks()
       
#tracks deadlines and organizes events and tasks by priority via those deadlines 
#May be deleted for alternatives provided by group
    def deadline_manager(self, task_index):
        if task_index < 0 or task_index >= len(self.tasks):
            print("❌ Invalid task index.")
            return

        task = self.tasks[task_index]['description']
        deadline_prompt = input(f"When is the task '{task}' due? Use MM/DD/YYYY or MM-DD-YYYY: ")

        def is_valid_date(date_string):
            return re.match(r"^\d{2}[-/]\d{2}[-/]\d{4}$", date_string) is not None

        if is_valid_date(deadline_prompt):
            try:
                parsed_date = datetime.strptime(deadline_prompt.replace("-", "/"), "%m/%d/%Y")
                self.deadlines[task] = parsed_date.strftime("%Y-%m-%d")
                print(f"📅 Deadline set for '{task}' on {parsed_date.strftime('%B %d, %Y')}")
            except ValueError:
                print("❌ Could not parse the date.")
        else:
            print("❌ Invalid date format.")




def main():
    """Parses CLI arguments and routes to appropriate functions. """
    #Set up the argument parser
    parser = argparse.ArgumentParser(description="TaskTrackr - Command Line To-Do List")
    subparsers = parser.add_subparsers(dest='command')

    # Add the task command
    add_parser = subparsers.add_parser('add')
    add_parser.add_argument('--title', required=True)
    add_parser.add_argument('--due', required=True)
    add_parser.add_argument('--priority', default='Medium')

    #List the tasks command
    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('--status', choices=['pending', 'completed'])

    #Complete the task command
    complete_parser = subparsers.add_parser('complete')
    complete_parser.add_argument('--id', type=int, required=True)

    #Delete the task command
    delete_parser = subparsers.add_parser('delete')
    delete_parser.add_argument('--id', type=int, required=True)

    #Parse arguments and route commands
    args = parser.parse_args()

    if args.command == 'add':
        add_task(args.title, args.due, args.priority)
    elif args.command == 'list':
        list_tasks(args.status)
    elif args.command == 'complete':
        complete_task(args.id)
    elif args.command == 'delete':
        delete_task(args.id)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
