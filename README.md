# TaskTrackr
TaskTrackr is a command-line task tracker and to-do list manager written in Python.  
It allows you to add, view, complete, and delete tasks using simple terminal commands.

# Key Features
- Add tasks with a title, due date, and priority level
- View all tasks or filter by completed/pending
- Mark tasks as completed
- Delete tasks
- Data is saved locally in a 'tasks.json' file

# How to Run
First, make sure you have Python installed.

# Add a Task
python tasktrackr.py add --title "Finish project" --due "2025-04-27" --priority High

# List Tasks
python tasktrackr.py list
python tasktrackr.py list --status pending
python tasktrackr.py list --status completed

# Mark Task as Complete 
python tasktrackr.py complete --id 1

# Delete a Task 
python tasktrackr.py delete --id 1

# Run Unit Tests
python test_tasktrackr.py


