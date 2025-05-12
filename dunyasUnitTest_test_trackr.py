import unittest
import os
from tasktrackr import TaskManager, TASKS_FILE


class TestTaskManager(unittest.TestCase):#To remove the existing tasks file before every test
    def setUp(self):
        if os.path.exists(TASKS_FILE):
            os.remove(TASKS_FILE)
        self.manager = TaskManager()

    def tearDown(self):
        if os.path.exists(TASKS_FILE):
            os.remove(TASKS_FILE)

    def test_add_task(self): #Example of task being ran
        self.manager.add_task("finish quiz", "2025-05-01", "medium")
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(self.manager.tasks[0].title, "finish quiz")

    def test_complete_task(self):
        self.manager.add_task("Review Python notes", "2025-05-02", "High")
        self.manager.complete_task(1)
        self.assertTrue(self.manager.tasks[0].completed)

    def test_delete_task(self):
        self.manager.add_task("Delete old math homework", "2025-04-29", "Low")
        self.manager.delete_task(1)
        self.assertEqual(len(self.manager.tasks), 0)

    def test_update_task(self):
        self.manager.add_task("Draft project summary", "2025-05-04", "medium")
        self.manager.update_task(1, title="Finalize project summary", priority="High")
        task = self.manager.tasks[0]
        self.assertEqual(task.title, "finalize project summary")
        self.assertEqual(task.priority, "High")

    def test_list_tasks(self):
        self.manager.add_task("Study for INST326", "2025-05-05", "High")
        self.manager.add_task("Submit resume edits", "2025-05-06", "Medium")
        self.assertEqual(len(self.manager.tasks), 2)


if __name__ == "__main__":
    unittest.main()
