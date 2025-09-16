import sys
from PySide6.QtWidgets import QApplication
from core.task_manager import TaskManager
from ui.calendar_view import CalendarView

def main():
    task_manager = TaskManager()

    app = QApplication(sys.argv)
    window = CalendarView(task_manager)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
