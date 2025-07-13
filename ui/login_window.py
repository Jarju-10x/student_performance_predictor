from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
import hashlib
from database.db_operations import get_user

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Performance Prediction - Login")
        self.setFixedSize(300, 200)
        
        self._setup_ui()
    
    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Username
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        
        # Password
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self._authenticate)
        layout.addWidget(self.login_button)
        
        self._apply_styles()
    
    def _apply_styles(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #f0f0f0; }
            QLabel { font-size: 14px; margin-bottom: 5px; }
            QLineEdit {
                padding: 8px; font-size: 14px;
                border: 1px solid #ccc; border-radius: 4px;
                margin-bottom: 15px;
            }
            QPushButton {
                background-color: #4CAF50; color: white;
                padding: 10px; font-size: 14px;
                border: none; border-radius: 4px;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
    
    def _authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return
        
        # In production, use proper password hashing
        # hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        user = get_user(username)
        if user and user.password == password:  # Simple comparison for demo
            from ui.main_window import MainWindow
            self.main_window = MainWindow(user.id, user.role)
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")
