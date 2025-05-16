import unittest
from unittest.mock import patch, mock_open
from datetime import datetime, timedelta
import json
import os

from your_module import TaskManager  # Replace with the actual module name (e.g. task_manager)

class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.manager = TaskManager()

    def test_add_task(self):
        self.manager.add_task("Test Task", "12/31/2025")
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(self.manager.tasks[0]["description"], "Test Task")
        self.assertEqual(self.manager.tasks[0]["status"], "incomplete")
        self.assertEqual(self.manager.tasks[0]["due_date"], "12/31/2025")

    @patch("builtins.open", new_callable=mock_open, read_data='[{"description": "Test", "status": "incomplete", "due_date": "N/A"}]')
    def test_load_tasks_valid_file(self, mock_file):
        self.manager.load_tasks()
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(self.manager.tasks[0]["description"], "Test")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_tasks_file_not_found(self, mock_file):
        with patch("builtins.input", side_effect=["done"]):
            self.manager.load_tasks()
        self.assertEqual(self.manager.tasks, [])

    @patch("builtins.open", new_callable=mock_open)
    def test_save_tasks(self, mock_file):
        self.manager.add_task("Sample")
        self.manager.save_tasks()
        mock_file().write.assert_called()

    def test_organize_and_display_tasks(self):
        today = datetime.today().strftime("%m/%d/%Y")
        overdue = (datetime.today() - timedelta(days=1)).strftime("%m/%d/%Y")
        upcoming = (datetime.today() + timedelta(days=3)).strftime("%m/%d/%Y")
        later = (datetime.today() + timedelta(days=10)).strftime("%m/%d/%Y")

        self.manager.tasks = [
            {"description": "Overdue", "status": "incomplete", "due_date": overdue},
            {"description": "Today", "status": "incomplete", "due_date": today},
            {"description": "Soon", "status": "incomplete", "due_date": upcoming},
            {"description": "Later", "status": "incomplete", "due_date": later},
            {"description": "None", "status": "incomplete", "due_date": "N/A"},
            {"description": "Invalid", "status": "incomplete", "due_date": "32/13/9999"},
        ]

        with patch("builtins.print") as mock_print:
            self.manager.organize_and_display_tasks()
            calls = [str(call) for call in mock_print.call_args_list]
            self.assertTrue(any("Overdue" in c[0] for c in calls))
            self.assertTrue(any("Due Today" in c[0] for c in calls))
            self.assertTrue(any("Due This Week" in c[0] for c in calls))
            self.assertTrue(any("Due Later" in c[0] for c in calls))
            self.assertTrue(any("No Due Date" in c[0] for c in calls))
            self.assertTrue(any("Invalid Dates" in c[0] for c in calls))

    @patch("builtins.input", side_effect=["yes"])
    def test_progress_tracker_complete(self, mock_input):
        self.manager.tasks = [{"description": "Test Task", "status": "incomplete", "due_date": "N/A"}]
        with patch.object(self.manager, 'save_tasks') as mock_save:
            self.manager.progress_tracker(0)
            self.assertEqual(self.manager.tasks[0]["status"], "complete")
            mock_save.assert_called_once()

    @patch("builtins.input", side_effect=["no"])
    def test_progress_tracker_incomplete(self, mock_input):
        self.manager.tasks = [{"description": "Test Task", "status": "incomplete", "due_date": "N/A"}]
        with patch.object(self.manager, 'save_tasks') as mock_save:
            self.manager.progress_tracker(0)
            self.assertEqual(self.manager.tasks[0]["status"], "incomplete")
            mock_save.assert_called_once()

    @patch("builtins.input", side_effect=["12-31-2025"])
    def test_deadline_manager_valid(self, mock_input):
        self.manager.tasks = [{"description": "Test Task", "status": "incomplete", "due_date": "N/A"}]
        with patch("builtins.print") as mock_print:
            self.manager.deadline_manager(0)
            self.assertIn(self.manager.tasks[0], self.manager.deadlines)
            mock_print.assert_called()

    @patch("builtins.input", side_effect=["invalid-date"])
    def test_deadline_manager_invalid(self, mock_input):
        self.manager.tasks = [{"description": "Test Task", "status": "incomplete", "due_date": "N/A"}]
        with patch("builtins.print") as mock_print:
            self.manager.deadline_manager(0)
            self.assertFalse(hasattr(self.manager, "deadlines"))
            mock_print.assert_called()


if __name__ == "__main__":
    unittest.main()
