import sys
from PyQt5.QtWidgets import QApplication
from database.db_operations import initialize_database
from ui.login_window import LoginWindow

def main():
    # Initialize the database
    initialize_database()
    
    # Create and run the application
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern UI style
    
    # Show login window
    login_window = LoginWindow()
    login_window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() # main.py
