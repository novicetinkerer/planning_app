from data.models import Task

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def get_all_tasks(self):
        return self.tasks