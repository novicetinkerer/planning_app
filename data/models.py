class Task:
    def __init__(self, title, description, due_date=None, priority=None, tags=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.tags = tags or []
        self.done = False