class Task:
    def __init__(self, title, due_date=None, priority=None, tags=None):
        self.title = title
        self.due_date = due_date
        self.priority = priority
        self.tags = tags or []
        self.done = False