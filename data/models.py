from datetime import date

class Task:
    def __init__(self, title: str, due_date: date, estimate_days: int, priority: str = "Medium", done: bool = False):
        self.title = title
        self.due_date = due_date
        self.estimate_days = estimate_days #estimated amount of days required to complete this task
        self.priority = priority
        self.done = done

    def mark_done(self):
        self.done = True

    def to_dict(self):
        return {
            "title": self.title,
            "due_date": self.due_date.isoformat(),
            "estimate_days": self.estimate_days,
            "priority": self.priority,
            "done": self.done
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            due_date=date.fromisoformat(data["due_date"]),
            estimate_days=data["estimate_days"],
            priority=data["priority"],
            done=data["done"]
        )
