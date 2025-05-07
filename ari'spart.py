"""TaskTrackr: A command-line task manager that allows you to add, view, complete, 
   and delete tasks using simple terminal commands."""

import argparse
import json
import os

TASKS_FILE = 'tasks.json'

def __init__(self):
        self.tasks = []

def load_tasks():
    """Loads tasks from the JSON file."""
    pass  #TODO: implement the logic for loading 


def save_tasks(tasks):
    """Save the tasks to the JSON file."""
    pass  # TODO: implement saving logic
   
def organize_task(self):
            categorized_tasks = {
                'ClassType A': [],
                'ClassType B': [],
                'ClassType C': [],
                'Other': []
            }
            

            for task in self.tasks:
                if task[0] == 'A':
                    categorized_tasks['ClassType A'].append(task)
                elif task[0] == 'B':
                    categorized_tasks['ClassType B'].append(task)
                elif task[0] == 'C':
                    categorized_tasks['ClassType C'].append(task)
                else:
                    categorized_tasks['Other'].append(task)
                
            return categorized_tasks
                




def add_task(self, description):
            self.tasks.append(description)


def list_tasks(status=None):
    """Lists all tasks, optionally filtered by status."""
    for i,task in enumerate(self.tasks):
                print(f"{i + 1}.task")  # TODO: implement list logic

def progress_tracker(self,task,prompt_status = True):
            progress_prompt = input(f"Have you finished the task {task}?  Enter Yes or No: ").strip().lower()
            if(progress_prompt == "yes"):
                prompt_status = True
                print(f"✅ Task '{task}' is 100% done.")

            elif(progress_prompt == "no"):
                prompt_status = False
                print(f"⏳ Task '{task}' is still in progress.")
            else:
                print("Invalid input")
                return None
            
            return prompt_status

def complete_task(task_id):
    """Marks a task as completed."""
    pass  # TODO: implement mark-complete logic


def delete_task(task_id):
    """Deletes a task based on its ID."""
    pass  # TODO: implement delete logic


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
