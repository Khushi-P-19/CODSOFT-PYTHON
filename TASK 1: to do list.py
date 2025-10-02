import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets

class TodoModel(QtCore.QAbstractListModel):
    def __init__(self, *args, todos=None, **kwargs):
        super(TodoModel, self).__init__(*args, **kwargs)
        self.todos = todos or []
        self.filtered_todos = self.todos  # For search filtering

    def data(self, index, role):
        row = index.row()
        status, text = self.filtered_todos[row]

        if role == QtCore.Qt.DisplayRole:
            return text

        if role == QtCore.Qt.FontRole:
            font = QtGui.QFont()
            if status:
                font.setStrikeOut(True)
            return font

        if role == QtCore.Qt.ForegroundRole:
            if status:
                return QtGui.QBrush(QtGui.QColor('gray'))

    def rowCount(self, index):
        return len(self.filtered_todos)

    def filter(self, query):
        self.filtered_todos = [todo for todo in self.todos if query.lower() in todo[1].lower()]
        self.layoutChanged.emit()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Advanced To-Do List App")
        self.setGeometry(100, 100, 400, 400)
        self.is_dark_mode = False

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Search bar
        self.searchEdit = QtWidgets.QLineEdit()
        self.searchEdit.setPlaceholderText("Search tasks...")
        self.searchEdit.textChanged.connect(self.search)
        self.layout.addWidget(self.searchEdit)

        # Todo list view
        self.todoView = QtWidgets.QListView()
        self.todoView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.layout.addWidget(self.todoView)

        # Input layout
        self.input_layout = QtWidgets.QHBoxLayout()
        self.todoEdit = QtWidgets.QLineEdit()
        self.todoEdit.setPlaceholderText("Enter new task...")
        self.input_layout.addWidget(self.todoEdit)

        self.addButton = QtWidgets.QPushButton("Add")
        self.addButton.clicked.connect(self.add)
        self.input_layout.addWidget(self.addButton)

        self.layout.addLayout(self.input_layout)

        # Action buttons
        self.button_layout = QtWidgets.QHBoxLayout()
        self.editButton = QtWidgets.QPushButton("Edit")
        self.editButton.clicked.connect(self.edit)
        self.button_layout.addWidget(self.editButton)

        self.deleteButton = QtWidgets.QPushButton("Delete")
        self.deleteButton.clicked.connect(self.delete)
        self.button_layout.addWidget(self.deleteButton)

        self.completeButton = QtWidgets.QPushButton("Complete")
        self.completeButton.clicked.connect(self.complete)
        self.button_layout.addWidget(self.completeButton)

        self.themeButton = QtWidgets.QPushButton("Toggle Theme")
        self.themeButton.clicked.connect(self.toggle_theme)
        self.button_layout.addWidget(self.themeButton)

        self.layout.addLayout(self.button_layout)

        # Model setup
        self.model = TodoModel()
        self.load()
        self.todoView.setModel(self.model)

    def add(self):
        text = self.todoEdit.text()
        if text:
            self.model.todos.append((False, text))
            self.model.filter(self.searchEdit.text())  # Refresh filter
            self.todoEdit.setText("")
            self.save()

    def edit(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            status, text = self.model.filtered_todos[row]  # Use filtered for accuracy
            new_text, ok = QtWidgets.QInputDialog.getText(self, "Edit Task", "New text:", QtWidgets.QLineEdit.Normal, text)
            if ok and new_text:
                # Update in original todos
                original_row = self.model.todos.index(self.model.filtered_todos[row])
                self.model.todos[original_row] = (status, new_text)
                self.model.filter(self.searchEdit.text())
                self.save()

    def delete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            # Remove from original todos
            del self.model.todos[self.model.todos.index(self.model.filtered_todos[row])]
            self.model.filter(self.searchEdit.text())
            self.todoView.clearSelection()
            self.save()

    def complete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            status, text = self.model.filtered_todos[row]
            # Update in original
            original_row = self.model.todos.index(self.model.filtered_todos[row])
            self.model.todos[original_row] = (not status, text)  # Toggle complete
            self.model.filter(self.searchEdit.text())
            self.todoView.clearSelection()
            self.save()

    def search(self, text):
        self.model.filter(text)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            self.setStyleSheet("""
                QWidget { background-color: #2E2E2E; color: #FFFFFF; }
                QLineEdit, QListView { background-color: #3C3C3C; border: 1px solid #555555; }
                QPushButton { background-color: #4A4A4A; border: 1px solid #666666; }
            """)
        else:
            self.setStyleSheet("")

    def load(self):
        try:
            with open('todos.json', 'r') as f:
                self.model.todos = json.load(f)
            self.model.filter("")
        except Exception:
            pass

    def save(self):
        with open('todos.json', 'w') as f:
            json.dump(self.model.todos, f)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
