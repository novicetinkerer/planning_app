from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QDateEdit,
    QComboBox, QPushButton, QLabel, QWidget, QListWidget, QInputDialog,
    QHBoxLayout, QSpinBox, QMessageBox, QTableWidget, QTableWidgetItem)
from core.task_manager import TaskManager
from data.models import Task
from datetime import date

class CalendarView(QWidget):
    def __init__(self, task_manager: TaskManager):
        super().__init__()
        self.task_manager = task_manager
        self.setWindowTitle("Planning App")

        # 🔒 Prevent resizing window
        self.setFixedSize(700, 400)

        # Layouts
        self.layout = QHBoxLayout()
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(4)
        self.task_table.setHorizontalHeaderLabels(["Title", "Due Date", "Estimate", "Priority"])
        self.task_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.task_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.task_table.setSortingEnabled(True)
        self.task_table.setAlternatingRowColors(True)

        self.date_list_widget = QListWidget()
        self.date_list_widget.setFixedWidth(150)  # 🔒 fixed sidebar width

        self.main_vbox = QVBoxLayout()
        self.side_date_box = QVBoxLayout()
        self.add_task_button = QPushButton("Add Task")
        self.add_task_button.clicked.connect(self.add_task)

        # Right side (tasks)
        self.main_vbox.addWidget(self.task_table)
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
        if dialog.exec():
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
        tasks = self.task_manager.get_tasks_for_date(date.today())
        self.task_table.setRowCount(len(tasks))

        for row, task in enumerate(tasks):
            title = QTableWidgetItem(task.title)
            due_date = QTableWidgetItem(task.due_date.isoformat())
            estimate_days = QTableWidgetItem(str(task.estimate_days))
            priority = QTableWidgetItem(task.priority)

            self.task_table.setItem(row, 0, title)
            self.task_table.setItem(row, 1, due_date)
            self.task_table.setItem(row, 2, estimate_days)
            self.task_table.setItem(row, 3, priority)


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
        self.add_button.clicked.connect(self.validate_and_accept)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def validate_and_accept(self):
        if not self.title_input.text().strip():
            QMessageBox.warning(
                self,
                "Missing Data",
                "Please enter a task title."
            )
            return

        if not int(self.estimate_days.value()):
            QMessageBox.warning(
                self,
                "Missing Data",
                "Please enter a valid number of days."
            )
            return

        # ✅ everything fine → close dialog
        self.accept()

    def get_task_data(self):
        return {
            "title": self.title_input.text(),
            "due_date": self.date_input.date().toPython(),
            "estimate_days": int(self.estimate_days.value()),
            "priority": self.priority_input.currentText()
        }