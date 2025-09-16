from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDateEdit, QComboBox, QPushButton, QLabel, QWidget, \
    QListWidget, QInputDialog, QHBoxLayout
from core.task_manager import TaskManager
from data.models import Task
from datetime import date

class CalendarView(QWidget):
    def __init__(self, task_manager: TaskManager):
        super().__init__()
        self.task_manager = task_manager
        self.setWindowTitle("Planning App")
        self.setFixedSize(1400, 700)

        self.layout = QHBoxLayout()
        self.task_list_widget = QListWidget()
        self.date_list_widget = QListWidget()
        self.main_vbox = QVBoxLayout()
        self.side_date_box = QVBoxLayout()
        self.add_task_button = QPushButton("Add Task")
        self.add_task_button.clicked.connect(self.add_task)

        self.main_vbox.addWidget(self.task_list_widget)
        self.main_vbox.addWidget(self.add_task_button)

        self.side_date_box.addWidget(self.date_list_widget)

        self.layout.addLayout(self.side_date_box)
        self.layout.addLayout(self.main_vbox)
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
        for task in self.task_manager.get_tasks_for_date(date.today()):
            status = "[Done]" if task.done else "[ ]"
            self.task_list_widget.addItem(f"{status} {task.title}")
