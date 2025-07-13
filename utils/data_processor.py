import pandas as pd
from typing import Tuple
from database.models import Student

def preprocess_data(df: pd.DataFrame, missing_strategy: str = 'drop', 
                   normalize: bool = False) -> pd.DataFrame:
    """
    Preprocess student data
    
    Args:
        df: Raw student data
        missing_strategy: How to handle missing values ('drop', 'mean', 'median')
        normalize: Whether to normalize numeric features
    
    Returns:
        Preprocessed DataFrame
    """
    # Handle missing values
    if missing_strategy == 'drop':
        df = df.dropna()
    elif missing_strategy == 'mean':
        df = df.fillna(df.mean(numeric_only=True))
    elif missing_strategy == 'median':
        df = df.fillna(df.median(numeric_only=True))
    
    # Normalization
    if normalize:
        numeric_cols = df.select_dtypes(include=['number']).columns
        df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std()
    
    return df

def calculate_performance(score: int) -> str:
    """Categorize student performance based on score"""
    if score >= 45:
        return "Excellent"
    elif score >= 35:
        return "Good"
    elif score >= 25:
        return "Average"
    else:
        return "Poor"
