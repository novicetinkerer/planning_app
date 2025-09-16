from datetime import date
from data.models import Task

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def get_tasks_for_date(self, query_date: date):
        return [task for task in self.tasks if task.due_date == query_date]
