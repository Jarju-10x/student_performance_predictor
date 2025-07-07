# main.py
from PyQt5 import QtWidgets
import sys
from ui_main import StudentEntryForm

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = StudentEntryForm()
    window.show()
    sys.exit(app.exec_())
