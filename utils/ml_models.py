from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from typing import Tuple, Any

def train_model(X, y, model_type: str = 'decision_tree') -> Tuple[Any, float]:
    """
    Train a machine learning model
    
    Args:
        X: Features
        y: Target
        model_type: Type of model ('decision_tree' or 'naive_bayes')
    
    Returns:
        Tuple of (trained_model, accuracy_score)
    """
    # Encode categorical target
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42
    )
    
    # Train model
    if model_type == 'decision_tree':
        model = DecisionTreeClassifier(random_state=42)
    else:  # naive_bayes
        model = GaussianNB()
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    return model, accuracy
