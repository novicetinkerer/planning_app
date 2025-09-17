from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QDateEdit,
    QComboBox, QPushButton, QLabel, QWidget, QListWidget, QInputDialog,
    QHBoxLayout, QSpinBox, QMessageBox)
from core.task_manager import TaskManager
from data.models import Task
from datetime import date

class CalendarView(QWidget):
    def __init__(self, task_manager: TaskManager):
        super().__init__()
        self.task_manager = task_manager
        self.setWindowTitle("Planning App")

        # 🔒 Prevent resizing window
        self.setFixedSize(600, 400)

        # Layouts
        self.layout = QHBoxLayout()
        self.task_list_widget = QListWidget()
        self.date_list_widget = QListWidget()
        self.date_list_widget.setFixedWidth(150)  # 🔒 fixed sidebar width

        self.main_vbox = QVBoxLayout()
        self.side_date_box = QVBoxLayout()
        self.add_task_button = QPushButton("Add Task")
        self.add_task_button.clicked.connect(self.add_task)

        # Right side (tasks)
        self.main_vbox.addWidget(self.task_list_widget)
        self.main_vbox.addWidget(self.add_task_button)

        # Left side (dates)
        self.side_date_box.addWidget(QLabel("Dates"))
        self.side_date_box.addWidget(self.date_list_widget)

        # Sidebar container (needed to apply fixed width cleanly)
        sidebar_container = QWidget()
        sidebar_container.setLayout(self.side_date_box)
        sidebar_container.setFixedWidth(150)  # 🔒 sidebar always 150px

        # Add to main layout
        self.layout.addWidget(sidebar_container)
        self.layout.addLayout(self.main_vbox)
        self.setLayout(self.layout)

        self.refresh_task_list()

    def add_task(self):
        dialog = AddTaskDialog()
        if dialog.exec():  # if user pressed "Add Task"
            data = dialog.get_task_data()
            task = Task(
                title = data["title"],
                due_date = data["due_date"],
                estimate_days = data["estimate_days"],
                priority = data["priority"]
            )
            self.task_manager.add_task(task)
            self.refresh_task_list()

    def refresh_task_list(self):
        self.task_list_widget.clear()
        for task in self.task_manager.get_tasks_for_date(date.today()):
            status = "[Done]" if task.done else "[ ]"
            self.task_list_widget.addItem(f"{status} {task.title}")


class AddTaskDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Task")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        # Title input
        layout.addWidget(QLabel("Task Title:"))
        self.title_input = QLineEdit()
        layout.addWidget(self.title_input)

        # Due date input
        layout.addWidget(QLabel("Due Date:"))
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(date.today())
        layout.addWidget(self.date_input)

        # Estimated days input
        layout.addWidget(QLabel("Estimated Days:"))
        self.estimate_days = QSpinBox()
        layout.addWidget(self.estimate_days)

        # Priority input
        layout.addWidget(QLabel("Priority:"))
        self.priority_input = QComboBox()
        self.priority_input.addItems(["Low", "Medium", "High"])
        layout.addWidget(self.priority_input)

        # Confirm button
        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.validate_and_accept)  # closes dialog with accept()
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def validate_and_accept(self):
        if not self.title_input.text().strip():  # title is required
            QMessageBox.warning(self, "Missing Data", "Please enter a task title.")
            return  # don’t close dialog

        # ✅ everything fine → close dialog
        self.accept()

    def get_task_data(self):
        return {
            "title": self.title_input.text(),
            "due_date": self.date_input.date().toPython(),
            "estimate_days": int(self.estimate_days.value()),
            "priority": self.priority_input.currentText()
        }