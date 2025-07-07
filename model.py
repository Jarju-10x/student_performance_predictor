# model.py
import sqlite3
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

# Labels for output
LABELS = ['Poor', 'Average', 'Good', 'Excellent']

def fetch_student_data():
    conn = sqlite3.connect("data/database.db")
    df = pd.read_sql_query("SELECT * FROM Students", conn)
    conn.close()
    return df

def preprocess_data(df):
    # Handle missing values
    df = df.fillna(0)

    # Features and target placeholder
    X = df[['marks', 'attendance', 'participation']]

    # For MVP, we'll simulate labels: you can replace this with real data
    def assign_label(row):
        score = (row['marks'] * 0.6 + row['attendance'] * 0.3 + row['participation'] * 0.1)
        if score >= 85:
            return 3  # Excellent
        elif score >= 70:
            return 2  # Good
        elif score >= 50:
            return 1  # Average
        else:
            return 0  # Poor

    df['label'] = df.apply(assign_label, axis=1)

    # Normalize features
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, df['label']

def train_model(X, y):
    model = DecisionTreeClassifier()
    model.fit(X, y)
    return model

def predict_student_performance(model, student_features):
    # Expects list: [marks, attendance, participation]
    scaler = MinMaxScaler()
    student_scaled = scaler.fit_transform([student_features])
    prediction = model.predict(student_scaled)
    return LABELS[prediction[0]]

