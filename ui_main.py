# ui_main.py
from PyQt5 import QtWidgets
import sqlite3
from model import fetch_student_data, preprocess_data, train_model, predict_student_performance

class StudentEntryForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Data Entry")

        # Form layout
        layout = QtWidgets.QFormLayout()

        self.name = QtWidgets.QLineEdit()
        self.department = QtWidgets.QLineEdit()
        self.semester = QtWidgets.QSpinBox()
        self.semester.setMinimum(1)
        self.marks = QtWidgets.QDoubleSpinBox()
        self.marks.setMaximum(100)
        self.attendance = QtWidgets.QDoubleSpinBox()
        self.attendance.setMaximum(100)
        self.participation = QtWidgets.QDoubleSpinBox()
        self.participation.setMaximum(100)

        layout.addRow("Name", self.name)
        layout.addRow("Department", self.department)
        layout.addRow("Semester", self.semester)
        layout.addRow("Marks", self.marks)
        layout.addRow("Attendance (%)", self.attendance)
        layout.addRow("Participation (%)", self.participation)

        self.submit_btn = QtWidgets.QPushButton("Add Student")
        self.submit_btn.clicked.connect(self.add_student)
        layout.addRow(self.submit_btn)

        self.predict_btn = QtWidgets.QPushButton("Predict Performance")
        self.predict_btn.clicked.connect(self.predict_now)
        layout.addRow(self.predict_btn)

        self.setLayout(layout)

    def add_student(self):
        conn = sqlite3.connect("data/database.db")
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO Students (name, department, semester, marks, attendance, participation)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            self.name.text(),
            self.department.text(),
            self.semester.value(),
            self.marks.value(),
            self.attendance.value(),
            self.participation.value()
        ))

        conn.commit()
        conn.close()
        QtWidgets.QMessageBox.information(self, "Success", "Student added successfully")
        self.clear_fields()

    def clear_fields(self):
        self.name.clear()
        self.department.clear()
        self.semester.setValue(1)
        self.marks.setValue(0.0)
        self.attendance.setValue(0.0)
        self.participation.setValue(0.0)
    
    def predict_now(self):
        try:
            df = fetch_student_data()
            X, y = preprocess_data(df)
            model = train_model(X, y)
            # Take current form input
            features = [
                self.marks.value(),
                self.attendance.value(),
                self.participation.value()
            ]
            prediction = predict_student_performance(model, features)
            QtWidgets.QMessageBox.information(self, "Prediction", f"Predicted Performance: {prediction}")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", str(e))

