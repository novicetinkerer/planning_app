from datetime import date
from data.models import Task

class TaskManager:
    def __init__(self):
        self.tasks: list[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def get_tasks_for_date(self, query_date: date):
        return [t for t in self.tasks if t.due_date == query_date]

    def get_all_tasks(self):
        return self.tasks

    def mark_done(self, task: Task):
        task.mark_done()

    def delete_task(self, task: Task):
        self.tasks.remove(task)
