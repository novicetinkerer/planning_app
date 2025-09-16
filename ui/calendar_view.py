from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QInputDialog
from core.task_manager import TaskManager
from data.models import Task

class CalendarView(QWidget):
    def __init__(self, task_manager: TaskManager):
        super().__init__()
        self.task_manager = task_manager
        self.setWindowTitle("Planning App")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QVBoxLayout()
        self.task_list_widget = QListWidget()
        self.add_task_button = QPushButton("Add Task")
        self.add_task_button.clicked.connect(self.add_task)

        self.layout.addWidget(self.task_list_widget)
        self.layout.addWidget(self.add_task_button)
        self.setLayout(self.layout)

        self.refresh_task_list()

    def add_task(self):
        title, ok = QInputDialog.getText(self, "Add Task", "Task Title:")
        if ok and title:
            task = Task(title)
            self.task_manager.add_task(task)
            self.refresh_task_list()

    def refresh_task_list(self):
        self.task_list_widget.clear()
        for task in self.task_manager.get_all_tasks():
            status = "[Done]" if task.done else "[ ]"
            self.task_list_widget.addItem(f"{status} {task.title}")
