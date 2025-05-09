"""Task Tracker This section adds support for filtering tasks by status (pending or completed) 
in the list command, along with unit tests to ensure the filtering works correctly."""

def test_filter_pending_tasks(self):
  self.manager.add_task("Pending Task 1", "High")
  self.manager.add_task("Pending Task 2", "Low")
  self.manager.complete_task(self.manager.tasks[1].id)

  pending_tasks = [t for t in self.manager.tasks if not t.completed]
  self.assertEqual(len(pending_tasks), 1)
  self.assertEqual(pending_tasks[0].title, "Pending Task 1")

def test_filter_completed_tasks(self):
  self.manager.add_task("Completed Task 1", "2025-05-12", "Medium")
  self.manager.complete_task(self.manager.tasks[0].id)

  completed_tasks = [t for t in self.manager.tasks if t.completed]
  self.assertEqual(len(completed_tasks), 1)
  self.assertEqual(completed_tasks[0].title, "Completed Task 1")
