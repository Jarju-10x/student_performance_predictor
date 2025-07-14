from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QPushButton, QTableWidget, QTableWidgetItem, 
                            QComboBox, QMessageBox, QFileDialog, QSizePolicy)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import sqlite3
from database.db_operations import get_all_students
from utils.data_processor import preprocess_data, calculate_performance
from utils.ml_models import train_model

class MainWindow(QMainWindow):
    def __init__(self, user_id, role):
        super().__init__()
        self.user_id = user_id
        self.role = role
        self.current_model = None
        self.setWindowTitle("Student Performance Prediction System")
        self.setMinimumSize(1000, 700)  # Set a reasonable minimum size
        
        self._setup_ui()
    
    def _setup_ui(self):
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Header with user info
        header = QLabel(f"Welcome, {self.role.capitalize()} | Student Performance Prediction System")
        header.setFont(QFont('Arial', 12, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("padding: 10px; background-color: #5c90c4;")
        main_layout.addWidget(header)
        
        # Tab widget for different features
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabBar::tab { height: 30px; width: 120px; }")
        main_layout.addWidget(self.tabs)
        
        # Initialize all tabs
        self._init_student_tab()
        self._init_preprocessing_tab()
        self._init_analysis_tab()
        self._init_visualization_tab()
        self._init_reports_tab()
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def _init_student_tab(self):
        """Student Data Management Tab"""
        tab = QWidget()
        self.tabs.addTab(tab, "Student Data")
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Student table
        self.student_table = QTableWidget()
        self.student_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.student_table.setColumnCount(6)  # Simplified for example
        self.student_table.setHorizontalHeaderLabels([
            "ID", "Name", "Score", "Performance", "Study Time", "Absences"
        ])
        layout.addWidget(self.student_table)
        
        # Button row
        button_layout = QHBoxLayout()
        
        self.import_btn = QPushButton("Import CSV")
        self.import_btn.setFixedSize(120, 30)
        self.import_btn.clicked.connect(self._import_csv)
        button_layout.addWidget(self.import_btn)
        
        self.add_btn = QPushButton("Add Student")
        self.add_btn.setFixedSize(120, 30)
        self.add_btn.clicked.connect(self._add_student)
        button_layout.addWidget(self.add_btn)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setFixedSize(120, 30)
        self.refresh_btn.clicked.connect(self._load_student_data)
        button_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(button_layout)
        
        # Load initial data
        self._load_student_data()
    
    def _init_preprocessing_tab(self):
        """Data Preprocessing Tab"""
        tab = QWidget()
        self.tabs.addTab(tab, "Preprocessing")
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Missing values handling
        missing_layout = QHBoxLayout()
        missing_layout.addWidget(QLabel("Handle Missing Values:"))
        
        self.missing_combo = QComboBox()
        self.missing_combo.addItems(["Drop rows", "Fill with mean", "Fill with median"])
        self.missing_combo.setFixedWidth(200)
        missing_layout.addWidget(self.missing_combo)
        layout.addLayout(missing_layout)
        
        # Normalization
        norm_layout = QHBoxLayout()
        norm_layout.addWidget(QLabel("Normalization:"))
        
        self.norm_combo = QComboBox()
        self.norm_combo.addItems(["None", "Min-Max Scaling", "Standard Scaling"])
        self.norm_combo.setFixedWidth(200)
        norm_layout.addWidget(self.norm_combo)
        layout.addLayout(norm_layout)
        
        # Preprocess button
        self.preprocess_btn = QPushButton("Preprocess Data")
        self.preprocess_btn.setFixedSize(200, 40)
        self.preprocess_btn.clicked.connect(self._preprocess_data)
        layout.addWidget(self.preprocess_btn, alignment=Qt.AlignCenter)
        
        # Status label
        self.preprocess_status = QLabel("Ready to preprocess data")
        layout.addWidget(self.preprocess_status, alignment=Qt.AlignCenter)
        
        layout.addStretch()
    
    def _init_analysis_tab(self):
        """Data Analysis Tab"""
        tab = QWidget()
        self.tabs.addTab(tab, "Analysis")
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Algorithm selection
        algo_layout = QHBoxLayout()
        algo_layout.addWidget(QLabel("Algorithm:"))
        
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["Decision Tree", "Naive Bayes"])
        self.algo_combo.setFixedWidth(200)
        algo_layout.addWidget(self.algo_combo)
        layout.addLayout(algo_layout)
        
        # Run analysis button
        self.analyze_btn = QPushButton("Run Analysis")
        self.analyze_btn.setFixedSize(200, 40)
        self.analyze_btn.clicked.connect(self._run_analysis)
        layout.addWidget(self.analyze_btn, alignment=Qt.AlignCenter)
        
        # Results display
        self.results_label = QLabel("Results will appear here")
        self.results_label.setWordWrap(True)
        self.results_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.results_label)
        
        # Accuracy display
        self.accuracy_label = QLabel()
        self.accuracy_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2E8B57;")
        layout.addWidget(self.accuracy_label, alignment=Qt.AlignCenter)
        
        layout.addStretch()
    
    def _init_visualization_tab(self):
        """Data Visualization Tab"""
        tab = QWidget()
        self.tabs.addTab(tab, "Visualization")
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Chart selection
        chart_layout = QHBoxLayout()
        chart_layout.addWidget(QLabel("Chart Type:"))
        
        self.chart_combo = QComboBox()
        self.chart_combo.addItems([
            "Performance Distribution", 
            "Score by Gender", 
            "Absences vs Score"
        ])
        self.chart_combo.setFixedWidth(200)
        chart_layout.addWidget(self.chart_combo)
        layout.addLayout(chart_layout)
        
        # Generate chart button
        self.chart_btn = QPushButton("Generate Chart")
        self.chart_btn.setFixedSize(200, 40)
        self.chart_btn.clicked.connect(self._generate_chart)
        layout.addWidget(self.chart_btn, alignment=Qt.AlignCenter)
        
        # Matplotlib figure
        self.figure = Figure(figsize=(8, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.canvas)
        
        # Initial empty chart
        self._generate_chart()
    
    def _init_reports_tab(self):
        """Reports Tab"""
        tab = QWidget()
        self.tabs.addTab(tab, "Reports")
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Report type selection
        report_layout = QHBoxLayout()
        report_layout.addWidget(QLabel("Report Type:"))
        
        self.report_combo = QComboBox()
        self.report_combo.addItems([
            "Performance Summary", 
            "Student Statistics", 
            "Model Analysis"
        ])
        self.report_combo.setFixedWidth(200)
        report_layout.addWidget(self.report_combo)
        layout.addLayout(report_layout)
        
        # Export format
        export_layout = QHBoxLayout()
        export_layout.addWidget(QLabel("Export Format:"))
        
        self.export_combo = QComboBox()
        self.export_combo.addItems(["PDF", "Excel", "CSV"])
        self.export_combo.setFixedWidth(200)
        export_layout.addWidget(self.export_combo)
        layout.addLayout(export_layout)
        
        # Generate button
        self.report_btn = QPushButton("Generate Report")
        self.report_btn.setFixedSize(200, 40)
        self.report_btn.clicked.connect(self._generate_report)
        layout.addWidget(self.report_btn, alignment=Qt.AlignCenter)
        
        # Preview area
        self.report_preview = QLabel("Report preview will appear here")
        self.report_preview.setWordWrap(True)
        self.report_preview.setStyleSheet("border: 1px solid #ccc; padding: 10px;")
        layout.addWidget(self.report_preview)
        
        layout.addStretch()
    
    def _load_student_data(self):
        """Load student data into the table"""
        try:
            students = get_all_students()
            self.student_table.setRowCount(len(students))
            
            for row, student in enumerate(students):
                self.student_table.setItem(row, 0, QTableWidgetItem(str(student.student_id)))
                self.student_table.setItem(row, 1, QTableWidgetItem(student.name))
                self.student_table.setItem(row, 2, QTableWidgetItem(str(student.score)))
                self.student_table.setItem(row, 3, QTableWidgetItem(student.performance_category))
                self.student_table.setItem(row, 4, QTableWidgetItem(str(student.studytime)))
                self.student_table.setItem(row, 5, QTableWidgetItem(str(student.absences)))
            
            self.statusBar().showMessage(f"Loaded {len(students)} students", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load student data: {str(e)}")
    
    def _import_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        
        if file_path:
            try:
                df = pd.read_csv(file_path)
                
                # Connect to database
                conn = sqlite3.connect('student_performance.db')
                cursor = conn.cursor()
                
                # Clear existing data
                cursor.execute("DELETE FROM students")
                
                # Insert new data
                for _, row in df.iterrows():
                    # Calculate performance category based on score
                    score = row['Score']
                    if score >= 45:
                        performance = "Excellent"
                    elif score >= 35:
                        performance = "Good"
                    elif score >= 25:
                        performance = "Average"
                    else:
                        performance = "Poor"
                    
                    cursor.execute('''
                    INSERT INTO students VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                    ''', (
                        row['S/N'], row['Name'] if 'Name' in row else 'Unknown', 
                        row['Gender'], row['Age'], row['Location'], row['famsize'], 
                        row['Pstatus'], row['Medu'], row['Fedu'], row['traveltime'], 
                        row['studytime'], row['failures'], row['schoolsup'], 
                        row['famsup'], row['paid'], row['activities'], 
                        row['nursery'], row['higher'], row['internet'], 
                        row['famrel'], row['freetime'], row['health'], 
                        row['absences'], row['Score'], performance
                    ))
                
                conn.commit()
                QMessageBox.information(self, "Success", "Data imported successfully")
                self.load_student_data()
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import data: {str(e)}")
            finally:
                conn.close() 


    def _add_student(self):
        """Add a new student (placeholder implementation)"""
        QMessageBox.information(self, "Info", "Add student dialog would open here")
    
    def _preprocess_data(self):
        """Handle data preprocessing"""
        missing_method = self.missing_combo.currentText().lower().replace(" ", "_")
        norm_method = self.norm_combo.currentText().lower().replace(" ", "_")
        
        try:
            # Get data and preprocess
            students = get_all_students()
            df = pd.DataFrame([s.__dict__ for s in students])
            
            # Preprocess
            df = preprocess_data(df, missing_method, norm_method != "none")
            
            # Update UI
            self.preprocess_status.setText("Data preprocessing completed successfully")
            QMessageBox.information(self, "Success", "Data preprocessing completed")
            
        except Exception as e:
            self.preprocess_status.setText(f"Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Preprocessing failed: {str(e)}")
    
    def _run_analysis(self):
        """Run selected analysis algorithm"""
        algorithm = self.algo_combo.currentText().lower().replace(" ", "_")
        
        try:
            # Get data
            students = get_all_students()
            df = pd.DataFrame([s.__dict__ for s in students])
            
            # Prepare features and target
            features = df[['studytime', 'absences', 'failures', 'famrel']]
            target = df['performance_category']
            
            # Train model
            model, accuracy = train_model(features, target, algorithm)
            self.current_model = model
            
            # Update UI
            self.results_label.setText(
                f"Analysis completed using {self.algo_combo.currentText()}\n\n"
                f"Model trained on {len(features)} samples\n"
                f"Key features: Study Time, Absences, Failures, Family Relationship"
            )
            
            self.accuracy_label.setText(f"Model Accuracy: {accuracy:.2%}")
            self.statusBar().showMessage("Analysis completed successfully", 3000)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Analysis failed: {str(e)}")
    
    def _generate_chart(self):
        """Generate the selected chart type"""
        chart_type = self.chart_combo.currentText()
        
        try:
            # Get data
            students = get_all_students()
            df = pd.DataFrame([s.__dict__ for s in students])
            
            # Clear previous figure
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            if chart_type == "Performance Distribution":
                # Pie chart
                counts = df['performance_category'].value_counts()
                ax.pie(counts, labels=counts.index, autopct='%1.1f%%')
                ax.set_title("Performance Category Distribution")
            
            elif chart_type == "Score by Gender":
                # Bar chart
                avg_scores = df.groupby('gender')['score'].mean()
                ax.bar(avg_scores.index, avg_scores)
                ax.set_title("Average Score by Gender")
                ax.set_ylabel("Average Score")
            
            elif chart_type == "Absences vs Score":
                # Scatter plot
                ax.scatter(df['absences'], df['score'])
                ax.set_title("Absences vs Score")
                ax.set_xlabel("Absences")
                ax.set_ylabel("Score")
            
            # Refresh canvas
            self.canvas.draw()
            self.statusBar().showMessage(f"Generated {chart_type} chart", 3000)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate chart: {str(e)}")
    
    def _generate_report(self):
        """Generate the selected report (placeholder implementation)"""
        report_type = self.report_combo.currentText()
        export_format = self.export_combo.currentText()
        
        self.report_preview.setText(
            f"Report Type: {report_type}\n"
            f"Export Format: {export_format}\n\n"
            "This is a preview of what the report would look like. "
            "In a full implementation, this would show actual report content."
        )
        self.statusBar().showMessage(f"Prepared {report_type} report", 3000)
