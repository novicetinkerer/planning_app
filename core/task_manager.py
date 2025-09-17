from datetime import date
from data.models import Task

class TaskManager:
    def __init__(self):
        self.tasks: list[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)
        print(len(self.tasks))

    def get_tasks_for_date(self, query_date: date):
        return self.tasks
        # Temporarily returning all tasks cuz I have no idea how to deal
        # with returning current days
        #return [t for t in self.tasks if t.due_date == query_date]

    def get_all_tasks(self):
        return self.tasks

    def mark_done(self, task: Task):
        task.mark_done()

    def delete_task(self, task: Task):
        self.tasks.remove(task)
